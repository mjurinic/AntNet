import time
import sys
import graph
import globals
import ant
import result

if __name__ == "__main__":
    # N - nodes count
    # E - edges count
    N, E = map(int, raw_input().split())

    graphInstance = graph.Graph(N, E)
    resultsInstance = result.Result()

    # S - source node
    # D - destination node
    S, D = map(int, raw_input().split())

    for i in xrange(E):
        # a - node
        # b - node
        # d - weight
        a, b, weight = map(int, raw_input().split())
        graphInstance.add(a, b, weight)

    for node in graphInstance.nodes:
        node.initPheromoneTable(N)

    # Generate ants
    ants = []

    for i in xrange(globals.ANT_COUNT):
        a = ant.Ant('ant_' + str(i) + '@127.0.0.1',
                    globals.PASSWORD,
                    i,
                    graphInstance,
                    globals.AntDirection.FORWARD_ANT,
                    S - 1,
                    D - 1,
                    resultsInstance)

        a.start()
        # a.setDebugToScreen()
        ants.append(a)

        time.sleep(globals.TICK_PERIOD)

    # For interrupt purposes...
    alive = True

    while alive:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            alive = False

    for a in ants:
        a.stop()

    sys.exit(0)
