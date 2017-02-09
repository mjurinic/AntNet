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
            # print 'Current node: {}'.format(self.myAgent.currNode.id + 1)

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
                    self.setNextNode(link)
                    # if self.myAgent.nextNode.connectAnt(self.myAgent):
                    #     self.myAgent.visitedNodes.append(nextNode)
                    #     self.myAgent.path.append(link)
                    #     self.myAgent.currNode = nextNode
                    #     self.setNextNode(link)

                    # TODO else count failed attempts MAX_TIMES and drop him if MAX_TIMES is hit

                    return

            # Take all links that haven't been visited yet
            for link in self.myAgent.currNode.links:
                if link[0].id not in self.myAgent.visitedNodes:
                    probableLink.append((link, 0))

            # If every node is visited, take everything
            if len(probableLink) == 0:
                for link in self.myAgent.currNode.links:
                    probableLink.append((link, 0))

            # Calc probability and randomize next node
            for i in xrange(len(probableLink)):
                linkWeight = probableLink[i][0][1]
                probability = (100 + self.alpha * (1 - 1 / linkWeight)) / (1 + self.alpha * (linkWeight - 1))
                probableLink[i] = (probableLink[i][0], probability)

            # Randomize next node
            self.setNextNode(self.weighted_choice(probableLink))

            return

        def setNextNode(self, link):
            self.myAgent.visitedNodes.append(link[0].id)
            self.myAgent.path.append(link)
            self.myAgent.currNode = link[0]

        # Credit to: http://stackoverflow.com/a/4322940
        def weighted_choice(self, choices):
            values, weights = zip(*choices)
            total = 0
            cum_weights = []

            for w in weights:
                total += w
                cum_weights.append(total)

            x = random() * total
            i = bisect(cum_weights, x)

            return values[i]

    class BackwardState(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            print 'Ant #{} is now in Backward state.'.format(self.myAgent.id)
            self.myAgent.direction = globals.AntDirection.BACKWARD_ANT

        def _process(self):
            print 'Ant #{}\nPath: ({})'.format(self.myAgent.id, len(self.myAgent.path))

            for path in self.myAgent.path:
                print '{} ->'.format(path[0].id + 1),

            print '\n'

            if self.myAgent.isSourceNode(self.myAgent.currNode):
                self.myAgent._kill()
            else:
                self.myAgent._kill()
                # self._exitcode = self.myAgent.TRANSITION_DEFAULT

            time.sleep(globals.TICK_PERIOD)

    def isDestinationNode(self, node):
        return node.id == self.graph.nodes[self.destination].id

    def isSourceNode(self, node):
        return node.id == self.graph.nodes[self.source].id

    def __init__(self, agentjid, password, id, graph, direction, source, destination, resource="spade", port=5222, debug=[], p2p=False):
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

        # Path from source - destination and its cost in every step
        self.path = [(graph.nodes[source], 0)]

    def _setup(self):
        self.STATE_BACKWARD_CODE = 0
        self.STATE_FORWARD_CODE = 1

        self.TRANSITION_DEFAULT = 0
        self.TRANSITION_TO_BACKWARD = 10

        b = spade.Behaviour.FSMBehaviour()
        b.registerFirstState(self.ForwardState(), self.STATE_FORWARD_CODE)
        b.registerLastState(self.BackwardState(), self.STATE_BACKWARD_CODE)

        b.registerTransition(self.STATE_FORWARD_CODE, self.STATE_FORWARD_CODE, self.TRANSITION_DEFAULT)
        b.registerTransition(self.STATE_BACKWARD_CODE, self.STATE_BACKWARD_CODE, self.TRANSITION_DEFAULT)
        b.registerTransition(self.STATE_FORWARD_CODE, self.STATE_BACKWARD_CODE, self.TRANSITION_TO_BACKWARD)

        self.addBehaviour(b, None)
