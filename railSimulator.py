# This class simulates railway processes, given a set of trains and stations. 
# It supports a rail that has two tracks at each point, each for a train going in different directions
# Each block and rail only holds one train, so if a train is coming, it will stop if the block in front is occupied
# Written by Tanush Mittal


import simpy

class Rail(object):
#Initialize all the needed variables

    trains = []
    rail = []
    reverserail = []
    railLayout = []
    reverseRailLayout = []
    num_block = 0
    num_trains = 0
    num_station = 0
    delay = 0

    def __init__(self, env):
        #Reset all the class variables
        Rail.env = env
        Rail.trains = []
        Rail.rail = []
        Rail.reverserail = []
        #All stations and blocks are added to this in order to create a layout of the rail
        Rail.railLayout = []
        Rail.reverseRailLayout = []
        Rail.num_block = 0
        Rail.num_trains = 0
        Rail.num_station = 0
        Rail.delay = 0

    class Station(object):
        #Creating my stations
        def __init__(self, env, name, distance, holdtime = 5, length = 150):
            #give it various parameters
            self.env = env
            self.type = "station"
            self.name = name
            self.holdtime = holdtime
            self.length = length
            self.distance = distance
            Rail.num_station += 1
            #Based on distance, create that many blocks
            for i in range(distance):
                block = Rail.Block(env)
            Rail.railLayout.append(self)
            #add this object to list and create a parallel resource to store parallelly in another list
            station = simpy.Resource(env, capacity = 1)
            Rail.rail.append(station)
            #create both lists in reverse order
            Rail.reverseRailLayout = Rail.railLayout[::-1]
            self.createRRail()

        #Make new reources and store them in the reverse order
        def createRRail(self):
            for i in Rail.reverseRailLayout:
                if i.type == "block":
                    block = simpy.Resource(self.env, capacity = 1)    
                    Rail.reverserail.append(block)
                else:
                    station = simpy.Resource(self.env, capacity = 1)
                    Rail.reverserail.append(station)
   

    class Block(object):
        #class for creating blocks of rail
        def __init__(self, env, length = 150):
            self.env = env
            self.type = "block"
            self.length = length
            self.name = "block" + str(Rail.num_block)
            Rail.railLayout.append(self)
            Rail.num_block += 1
            block = simpy.Resource(env, capacity = 1)
            Rail.rail.append(block)

   
    class Train(object):
        #create trains
        def __init__(self, env, name, route, avgV = 50):
            self.env = env
            self.avgV = avgV
            self.name = name
            self.route = route
            Rail.num_trains += 1
            Rail.trains.append(self)

        def travel(self, timeout):
            #implement headway, could be made more complex, but works just fine like this
            yield self.env.timeout(timeout)
            while True:
                #Use the route passed to each train and iterate through the rail layout to find the next stop
                current = self.route[0]
                for dest in self.route[1:]:
                    if Rail.railLayout.index(current) > Rail.railLayout.index(dest):
                        raillayout = Rail.reverseRailLayout.copy()
                        rail1 = Rail.reverserail.copy()
                    else:
                        raillayout = Rail.railLayout.copy()
                        rail1 = Rail.rail.copy()
                    #All the print statements are commented out for convenience, 
                    #but if you would like to see how the simulation works, just uncomment them.
                    #print("{} is travelling from {} to {} at {}".format(self.name, current.name, dest.name, str(self.env.now)))
                    i = raillayout.index(current)
                    while raillayout[i].name != dest.name:
                        #print("{}travelling through {} at {}".format(self.name, raillayout[i].name, self.env.now))
                        request = rail1[i].request()
                        #attempt to enter the next block/station, and wait for time it takes 
                        time = self.env.now
                        yield request
                        Rail.delay += self.env.now - time
                        #Log how long it takes enter the blocks and store it in the delay variable
                        yield self.env.timeout(raillayout[i].length/self.avgV)
                        #time it takes to travel through the block
                        rail1[i].release(request) 
                        #release the resource so the next block can enter it
                        i+= 1
                    #print("{} arrived at {} at {}".format(self.name, dest.name, str(self.env.now)))
                    #print("staying here for {}".format(dest.holdtime))
                    request = rail1[i].request()
                    time = self.env.now
                    yield request
                    Rail.delay += self.env.now - time
                    yield self.env.timeout(dest.holdtime)
                    rail1[i].release(request)
                    current = dest
                    #Once you arrive at your station, wait for it to be open and 
                    #hold there for a certain amount of time

