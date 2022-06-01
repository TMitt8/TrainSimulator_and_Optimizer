
#This class uses the railSimulator to create an optimal schedule for trains traversing a certain line. 
#It takes into account the order of the trains and the headway between them and minimizes delay, as well as headway.
# Written by Tanush Mittal

import railSimulator
import simpy
import random
import math
import itertools
from collections import defaultdict
import sys

trains = []
#Add trains to a seperate list, only used for a cleaner printed message

def runRail(headway, order):
    #Define all trains and stations in here, change the layout/trains however you want
    env = simpy.Environment()
    railline = railSimulator.Rail(env)
    start = railline.Station(env, "Start", 0, holdtime = 0)
    switchY = railline.Station(env, "SwitchY", 3, holdtime = 2)
    stationA = railline.Station(env, "StationA", 2)
    stationB = railline.Station(env, "StationB", 10)
    stationC = railline.Station(env, "StationC", 12, holdtime=10)
    stationD = railline.Station(env, "StationD", 5, holdtime = 3)
    switchX = railline.Station(env, "SwitchX", 5, holdtime = 2)
    trainB = railline.Train(env, "TrainB", [start, stationA, stationD, switchX, stationA])
    trainA = railline.Train(env, "TrainA", [start, stationA, stationC, stationD, switchX, stationA])
    trainC = railline.Train(env, "TrainC", [start, stationA, switchY, stationB, stationC])
    trainD = railline.Train(env, "TrainD", [start, stationD, switchX, stationC, stationA, switchY, stationB, stationD])
    createProcess(env, railline, headway, order)
    random.seed(42)
    env.run(until = 300)
    #print("The delay was " + str(railline.delay))
    return math.exp(railline.delay) * headway

#Create all processes for the train, in the order
def createProcess(env, rail, headway, order):
    i = 0
    for x in order:
        trains.append(rail.trains[x].name)
        env.process(rail.trains[x].travel(i * headway))
        i += 1

#Run through all the possible headways and trains orders, run the simulation for each and find the delay
#Store all of this info in a dictionary
def main():
    numtrains = 4
    orders = itertools.permutations(list(range(0, numtrains)))
    data = defaultdict(dict)
    headways = 30
    for order in orders:
        for i in range(headways):
            data[order][i+1] = runRail(i+1, order)
    
    #Find the minimum delay value and store the order and headway for the optimal value
    MAX_INT = sys.maxsize
    minimum = MAX_INT
    bestorder = []
    bestheadway = None
    moreorders = itertools.permutations(list(range(0, numtrains)))
    for ord in moreorders:
        for num in range(headways):
            if data[ord][num+1] < minimum:
                minimum = data[ord][num+1]
                bestorder = ord
                bestheadway = num+1

    bestordnames = ""
    for i in bestorder:
        bestordnames = bestordnames + str(trains[i]) + ", "
    print("The ideal circumstances are when trains are in order: {} and  the headway is {}".format(bestordnames, bestheadway))

if __name__ == "__main__":
    main()