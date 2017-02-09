import time
import graph
import globals
import ant

if __name__ == "__main__":
    # N - nodes count
    # E - edges count
    N, E = map(int, raw_input().split())

    graph = graph.Graph(N, E)

    # S - source node
    # D - destination node
    S, D = map(int, raw_input().split())

    for i in xrange(E):
        # a - node
        # b - node
        # d - weight
        a, b, weight = map(int, raw_input().split())
        graph.add(a, b, weight)

    for node in graph.nodes:
        node.initPheromoneTable()

    # Debug output - init pheromone table
    for node in graph.nodes:
        print "\nId: " + str(node.id + 1)
        print "Links: "

        for entry in node.pheromoneTable:
            print "\tId: " + str(entry.link[0].id + 1) + " - " + str(entry.probability) + '%'

    # Generate ants
    for i in xrange(globals.ANT_COUNT):
        a = ant.Ant('ant_' + str(i) + '@127.0.0.1',
                    globals.PASSWORD,
                    i,
                    graph,
                    globals.AntDirection.FORWARD_ANT,
                    S - 1,
                    D - 1)

        a.start()
        time.sleep(globals.TICK_PERIOD)
