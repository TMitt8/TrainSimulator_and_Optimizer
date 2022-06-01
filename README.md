# TrainSimulator_and_Optimizer
This repository includes a class to simulate a rail system, and an algorithm to create an optimal schedule for any railway system.

This is an open-source GitHub repository centered around train modeling and scheduling. To use it, simply enter whatever layout and trains you would like in the runRail() function, change the value of numtrains in the main method to the number of train in the system, and run it. It will output the ideal train order and headway for your system.

There are two main parts to this project:

RaiSimulator.py simulates railway processes, given a set of trains and stations. It supports a rail that has two tracks at each point, each for a train going in different directions. Each block and rail only holds one train, so if a train is coming, it will stop if the block in front is occupied.

Optimizer.py uses the railSimulator.py to create an optimal schedule for trains traversing a certain line. It takes into account the order of the trains and the headway between them and minimizes delay, as well as headway.
