from random import random
from bisect import bisect

import spade
import time
import globals


class Ant(spade.Agent.Agent):
    class ForwardState(spade.Behaviour.OneShotBehaviour):
        def __init__(self):
            super(Ant.ForwardState, self).__init__()
            self.alpha = 0.2

        def onStart(self):
            print 'Ant #{} is now in Forward state.'.format(self.myAgent.id)

        def _process(self):
            self.chooseNextNode()

            if self.myAgent.isDestinationNode(self.myAgent.currNode):
                self._exitcode = self.myAgent.TRANSITION_TO_BACKWARD
            else:
                self._exitcode = self.myAgent.TRANSITION_DEFAULT

            time.sleep(globals.TICK_PERIOD)

        def chooseNextNode(self):
            # (Link, Probability=0) initial state
            probableLink = []

            # Check for direct connection to destination node
            for link in self.myAgent.currNode.links:
                nextNode = link[0]

                if nextNode.id == self.myAgent.destination:
                    self.setNextNode(self.weighted_choice([self.calculateProbabilities(link)]))
                    return

            # Take all links that haven't been visited yet
            for link in self.myAgent.currNode.links:
                if link[0].id not in self.myAgent.visitedNodes:
                    probableLink.append(self.calculateProbabilities(link))

            # TODO Cycle detected, delete known data for cycle nodes and append them all as probable links
            if len(probableLink) == 0:
                for link in self.myAgent.currNode.links:
                    probableLink.append(self.calculateProbabilities(link))

            # Debug purposes
            print '\nCurrent Node ({})'.format(self.myAgent.currNode.id + 1)
            print 'Possible nodes:'

            for el in probableLink:
                print '\tNode ({}) - Goodness: {}%'.format(el[0][0].id + 1, el[1])

            print '\n'

            # Randomize next node
            self.setNextNode(self.weighted_choice(probableLink))

            return

        def calculateProbabilities(self, link):
            linkWeight = link[1]
            tau = 0

            for entry in self.myAgent.currNode.pheromoneTable.get(self.myAgent.destination):
                if entry.link[0].id == link[0].id:
                    tau = entry.probability

            # Goodness formula
            probability = (tau + self.alpha * (1 - 1 / linkWeight)) / (1 + self.alpha * (linkWeight - 1))

            return link, probability

        def setNextNode(self, entry):
            self.myAgent.visitedNodes.append(entry[0][0].id)
            self.myAgent.path.append(entry)
            self.myAgent.currNode = entry[0][0]

        # Credit to: http://stackoverflow.com/a/4322940
        # Returns 'link' and its 'goodness'
        def weighted_choice(self, choices):
            values, weights = zip(*choices)
            total = 0
            cum_weights = []

            for w in weights:
                total += w
                cum_weights.append(total)

            x = random() * total
            i = bisect(cum_weights, x)

            # Weights == goodness P'ijd
            return values[i], weights[i]

    class BackwardState(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            if self.myAgent.path[-1][0][0].id == self.myAgent.destination:
                # Save path to results
                route = ''

                for i in xrange(len(self.myAgent.path)):
                    route += str(self.myAgent.path[i][0][0].id + 1)

                    if i < len(self.myAgent.path) - 1:
                        route += ' -> '

                self.myAgent.results.updateRoutes(route)

            print 'Ant #{} is now in Backward state.'.format(self.myAgent.id)
            self.myAgent.direction = globals.AntDirection.BACKWARD_ANT

        def _process(self):
            # Debug purposes
            # print 'Ant #{} path size: ({})'.format(self.myAgent.id, len(self.myAgent.path))
            #
            # for pathElem in self.myAgent.path:
            #     print '({}, {})'.format(pathElem[0][0].id + 1, pathElem[1]),
            #
            #     if pathElem[0][0].id != self.myAgent.path[-1][0][0].id:
            #         print '->',
            #
            # print '\n'

            if len(self.myAgent.path) > 1:
                # The increment will be a function of the trip time experienced by the forward ant going from node k
                # to destination node i
                link, goodness = self.myAgent.path.pop()

                self.myAgent.currNode = self.myAgent.path[-1][0][0]
                self.myAgent.currNode.updatePheromoneTable(link[0].id, self.myAgent.destination, goodness)
                self.myAgent.graph.update(self.myAgent.currNode)

                self._exitcode = self.myAgent.TRANSITION_DEFAULT
            else:
                self._exitcode = self.myAgent.TRANSITION_TO_DEATH

            time.sleep(globals.TICK_PERIOD)

    class DieState(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            # Display new pheromone table status
            # self.myAgent.graph.printPheromoneStatus(self.myAgent.destination)

            print 'Ant #{} dies.'.format(self.myAgent.id)
            print self.myAgent.results.printRoutes()

        def _process(self):
            self.myAgent._kill()

    def isDestinationNode(self, node):
        return node.id == self.graph.nodes[self.destination].id

    def isSourceNode(self, node):
        return node.id == self.graph.nodes[self.source].id

    def __init__(self, agentjid, password, id, graph, direction, source, destination, results,resource="spade", port=5222, debug=[], p2p=False):
        super(Ant, self).__init__(agentjid, password, resource, port, debug, p2p)

        self.id = id

        # Graph instance containing nodes in the network
        # This instance is shared between all ants
        self.graph = graph

        # Forward or Backward ant
        self.direction = direction

        # Source & Destination node index (label)
        self.source = source
        self.destination = destination

        # Current node instance
        self.currNode = graph.nodes[source]

        # Used during algorithm steps to avoid visiting already visited nodes
        self.visitedNodes = [source]

        # Path from source - destination and its cost & goodness in every step
        self.path = [((graph.nodes[source], 0), 0.00)]  # Initial goodness set to 0.00 (inf)

        self.results = results

    def _setup(self):
        self.STATE_BACKWARD_CODE = 0
        self.STATE_FORWARD_CODE = 1
        self.STATE_DIE_CODE = 2

        self.TRANSITION_DEFAULT = 0
        self.TRANSITION_TO_BACKWARD = 10
        self.TRANSITION_TO_DEATH = 20

        b = spade.Behaviour.FSMBehaviour()
        b.registerFirstState(self.ForwardState(), self.STATE_FORWARD_CODE)
        b.registerState(self.BackwardState(), self.STATE_BACKWARD_CODE)
        b.registerLastState(self.DieState(), self.STATE_DIE_CODE)

        b.registerTransition(self.STATE_FORWARD_CODE, self.STATE_FORWARD_CODE, self.TRANSITION_DEFAULT)
        b.registerTransition(self.STATE_FORWARD_CODE, self.STATE_BACKWARD_CODE, self.TRANSITION_TO_BACKWARD)
        b.registerTransition(self.STATE_BACKWARD_CODE, self.STATE_BACKWARD_CODE, self.TRANSITION_DEFAULT)
        b.registerTransition(self.STATE_BACKWARD_CODE, self.STATE_DIE_CODE, self.TRANSITION_TO_DEATH)

        self.addBehaviour(b, None)