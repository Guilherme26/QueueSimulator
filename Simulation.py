import numpy, argparse

'''
    This work is meant to simulate how does system with queues behave in a
    context where arrival and service time coefficient is given by an exponentially
    distributed function.

    The parameters can be set either modifying this source code, or by line
    parameter with the flags described from line 60 to 62
'''


class QueueSimulator:
    def __init__(self, totalArrivals, lambdaArrival, muService):
        self.totalArrivals = totalArrivals
        # The coefficient that represents the arrival time of new users
        self.lambdaArrival = lambdaArrival
        # The coefficient that represents the time spent on the service
        self.muService = muService
        # A list to keep track of the user wait to be served
        self.waitings = []
        # A list to keep track of the attendant's idle time
        self.idleness = []
        self.arrivals = self.getArrivals()
        self.serviceTimes = self.getServiceTimes()
        self.departureTimes = []

    def getServiceTimes(self):
        return [numpy.random.exponential(self.muService) for i in range(self.totalArrivals)]

    def getArrivals(self):
        arr = []
        for i in range(self.totalArrivals):
            if(len(arr) == 0):
                arr.append(numpy.random.exponential(self.lambdaArrival))
            else:
                arr.append(arr[-1] + numpy.random.exponential(self.lambdaArrival))
        return arr

    def outputData(self):
        print "Mean Wait ", sum(self.waitings) / float(len(self.waitings))
        print "Mean Service Time  ", sum(self.serviceTimes) / len(self.serviceTimes)
        print "Idleness Time  ", sum(self.idleness) / self.departureTimes[-1]

    def run(self):
        for arrival,timeSpent in zip(self.arrivals, self.serviceTimes):
            if(len(self.departureTimes) == 0):
                self.departureTimes.append(arrival+timeSpent)
                continue
            elif(arrival < self.departureTimes[-1]):
                self.waitings.append(self.departureTimes[-1] - arrival)
            elif(arrival > self.departureTimes[-1]):
                self.idleness.append(arrival - self.departureTimes[-1])
            self.departureTimes.append(max(self.departureTimes[-1], arrival)+timeSpent)

        self.outputData()

def main():
    parser = argparse.ArgumentParser(description="Arguments Description")
    parser.add_argument('--lambdaArrival', nargs='?', default=5, help='Number of individuals that arrives in an amount t of time')
    parser.add_argument('--muService', nargs='?', default=5, help='Number of individuals that are served in an amount t of time')
    parser.add_argument('--totalArrivals', nargs='?', default=100000, help='Total number of arrivals in the simulation')

    args = parser.parse_args()

    LAMBDA_ARRIVAL = 1/float(args.lambdaArrival)
    MU_SERVICE = 1/float(args.muService)
    TOTAL_ARRIVALS = int(args.totalArrivals)

    sim = QueueSimulator(TOTAL_ARRIVALS, LAMBDA_ARRIVAL, MU_SERVICE)
    sim.run()

if __name__ == '__main__':
    main()
