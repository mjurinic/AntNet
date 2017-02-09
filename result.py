import operator


class Result:
    def __init__(self):
        # Routes used by ants
        self.routes = {}

    # route = 1,2,3,4,5
    def updateRoutes(self, route):
        self.routes[route] = self.routes.get(route, 0) + 1

    def printRoutes(self):
        print '\n'
        print '+---------------+'
        print '|    RESULTS    |'
        print '+---------------+'

        sorted_routes = sorted(self.routes.items(), key=operator.itemgetter(1), reverse=True)

        for key, value in sorted_routes:
            print 'Route: [{}]  Times used: {}'.format(key, value)

        print '\n'
