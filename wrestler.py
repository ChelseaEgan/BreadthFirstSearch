from queue import *
from sys import argv

#####################################################
# Program Name: wrestler.py                         #
# Author: Chelsea Egan                              #
# Class: CS 325-400                                 #
# Assignment: Homework 5                            #
# Date: November 4, 2018                            #
# Description: This program determines whether it   #
# is possible to designate wrestlers from an input  #
# file as either Babyfaces or Heels such that each  #
# rivalry is between a Babyface and a Heel. If      #
# possible, it prints the list of each.             #
#####################################################


# The BFS_WRESTLERS function iterates over each wrestler to see if it
# has been examined. If not, it runs a breadth-first search algorithm
# to determine whether it is a babyface or a heel and to see if that
# conflicts with any of its rivals. If no conflicts, it prints a list
# of all babyfaces and heels. It takes a list of dictionaries that
# represent wrestlers.
def BFS_WRESTLERS(wrestlers):
    # Store names of babyfaces and heels
    babyfaces = []
    heels = []

    # Iterate over every wrestler dictionary
    for s in wrestlers:

        # If this wrestler has not been examined
        if s['color'] != 'black':
            # Initialize as "touched" with zero distance - it is the root
            s['color'] = 'gray'
            s['distance'] = 0

            # Per instructions, first is a babyface
            babyfaces.append(s['name'])

            # FIFO queue to process rivalries starting with the root (s)
            BFSQueue = Queue()
            BFSQueue.put(s)

            # While there are wrestlers/rivalries to process
            while not BFSQueue.empty():

                # Get the first wrestler
                wrestler = BFSQueue.get()

                # For each rival of this wrestler
                for r in wrestler['rivals']:

                    # Get the dictionary that responds to the rival's name
                    rival = next((wrestler for wrestler in wrestlers if wrestler['name'] == r), None)

                    # If this rival has not been "touched"
                    if rival['color'] == 'white':

                        # Mark as touched and update distance from root
                        rival['color'] = 'gray'
                        rival['distance'] = wrestler['distance'] + 1

                        # If the distance is even, then it is babyface
                        if rival['distance'] % 2 == 0:
                            babyfaces.append(r)
                        # If the distance is odd, then it is a heel
                        else:
                            heels.append(r)
                        # Add to queue for further processing
                        BFSQueue.put(rival)

                    # This rival has been "touched" previously
                    else:
                        # If both the wrestler and rival are at an even distance from the
                        # root - they are both babyfaces and thus conflict
                        if (rival['distance'] % 2 == 0 and wrestler['distance'] % 2 == 0):
                            print('No')
                            return
                        # If they are both at an odd distance, then they are both heels and
                        # they conflict
                        elif(rival['distance'] % 2 != 0 and wrestler['distance'] % 2 != 0):
                            print('No')
                            return

                # Indicate that this wrestler has been fully examined
                wrestler['color'] = 'black'

    # No conflicts arose - print results
    print('Yes')
    print('Babyfaces: ' + ' '.join(babyfaces))
    print('Heels: ' + ' '.join(heels))

# Get command line argument for file name
script, fileName = argv

# Open the file for reading
with open(fileName) as fp:
    # Get the number of wrestlers
    numberOfWrestlers = int(fp.readline())
    # List to store the wrestlers
    wrestlers = []
    
    # Get the name of each wrestler and create a dictionary to store its values
    for wrestler in range(numberOfWrestlers):
        name = fp.readline().strip()
        wrestler = {
            "name": name,
            "color": "white",
            "distance": 0,
            "rivals": []
            } 
        wrestlers.append(wrestler)
    #Get the number of rivalries
    numberOfRivalries = int(fp.readline())

    # Store all rivalries for each wrestler in an adjacency list
    for rivalry in range(numberOfRivalries):
        # Get names of rivals
        w1, w2 = [str(x) for x in next(fp).split()]

        # Get the dictionaries that correspond to those names
        rival1 = next((wrestler for wrestler in wrestlers if wrestler['name'] == w1), None)
        rival2 = next((wrestler for wrestler in wrestlers if wrestler['name'] == w2), None)

        # Add to rival lists
        rival1['rivals'].append(rival2['name'])
        rival2['rivals'].append(rival1['name'])

# Run program to get solution
BFS_WRESTLERS(wrestlers)
