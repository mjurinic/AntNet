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
