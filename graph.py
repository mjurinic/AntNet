from prettytable import PrettyTable

import node


class Graph:
    def __init__(self, N, E):
        # Number of nodes
        self.N = N

        # Number of edges
        self.E = E

        # Contains edges for each node (in simple integer notation)
        self.graph = {}

        # Actual Node instances
        self.nodes = [node.Node(i) for i in xrange(N)]

    # Adds two nodes and the weight on their edge
    def add(self, nodeIdA, nodeIdB, weight):
        nodeIdA -= 1
        nodeIdB -= 1

        self.graph.setdefault(nodeIdA, []).append((nodeIdB, weight))
        self.graph.setdefault(nodeIdB, []).append((nodeIdA, weight))

        self.nodes[nodeIdA].addLink(self.nodes[nodeIdB], weight)
        self.nodes[nodeIdB].addLink(self.nodes[nodeIdA], weight)

    def update(self, node):
        for i in xrange(len(self.nodes)):
            if self.nodes[i].id == node.id:
                # print 'Updating node ({})'.format(node.id + 1)
                self.nodes[i] = node

    def printPheromoneStatus(self, destination):
        for node in self.nodes:
            t = PrettyTable(['i', 'j', 'd', 'goodness'])

            print "\nNode: {}".format(node.id + 1)

            for entry in node.pheromoneTable[destination]:
                t.add_row([node.id + 1, entry.link[0].id + 1, destination, entry.probability])

            print t

        print '\n'
