import itertools
import heapq
import globals


class Node:
    def __init__(self, id):
        # Node label
        self.id = id

        # List of pairs (neighbourNode, weight)
        self.links = []

        # Maximum number of ants in a node
        self.capacity = globals.NODE_CAPACITY

        # Current ants in the node
        self.antsInNode = self.PriorityQueue()

        # Pheromone table for neighbour nodes
        self.pheromoneTable = {}

    # Storing Node instance
    def addLink(self, node, weight):
        self.links.append((node, weight))

    def initPheromoneTable(self, N):
        for i in xrange(N):
            for j in xrange(len(self.links)):
                # Initially setting all pheromone values to 0.01
                self.pheromoneTable.setdefault(i, []).append(self.TableEntry(self.links[j], 0.01))

    # localDestination - the chosen neighbour
    def updatePheromoneTable(self, localDestination, finalDestination, r):
        # print 'LocalDest: {} FinalDest: {} r: {}'.format(localDestination + 1, finalDestination +1, r)
        #
        # print 'Before'
        # for entry in self.pheromoneTable[finalDestination]:
        #     print 'Node ({}) Probability: {}%'.format(entry.link[0].id + 1, entry.probability)

        for i in xrange(len(self.pheromoneTable[finalDestination])):
            entry = self.pheromoneTable[finalDestination][i]

            if entry.link[0].id == localDestination:
                self.pheromoneTable[finalDestination][i] = self.TableEntry(entry.link, entry.probability + r * (1 - entry.probability))
                break

        # print 'After'
        # for entry in self.pheromoneTable[finalDestination]:
        #     print 'Node ({}) Probability: {}%'.format(entry.link[0].id + 1, entry.probability)

    def connectAnt(self, ant):
        # TODO Should check if node is full...but lets keep it simple for now
        self.antsInNode.add(ant)
        return True

    # Contains the probability for a neighbour node to be chosen next
    class TableEntry:
        def __init__(self, link, probability):
            self.link = link
            self.probability = probability

    class PriorityQueue:
        def __init__(self):
            # list of entries arranged in a heap
            self.ants = []

            # mapping of ants to entries
            self.antFinder = {}

            # placeholder for a removed ant
            self.REMOVED = 'REMOVED'

            # unique sequence count
            self.counter = itertools.count()

        # Takes an instance of Ant class
        def add(self, ant):
            # Add a new task or update the priority of an existing task
            if ant in self.antFinder:
                self.remove(ant)

            count = next(self.counter)
            entry = [ant.direction, count, ant]

            self.antFinder[ant] = entry

            heapq.heappush(self.ants, entry)

        def remove(self, ant):
            # Mark an existing ant as REMOVED. Raise KeyError if not found.
            entry = self.antFinder.pop(ant)
            entry[-1] = self.REMOVED

        def pop(self):
            # Remove and return the lowest priority task. Raise KeyError if empty.
            while self.ants:
                priority, count, ant = heapq.heappop(self.ants)

                if ant is not self.REMOVED:
                    del self.antFinder[ant]
                    return ant

            raise KeyError('pop from an empty priority queue')
