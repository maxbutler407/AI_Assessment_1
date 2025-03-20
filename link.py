# link.py
#
# The code that defines the behaviour of Link.
#
# You should be able to write the code for a simple solution to the
# game version of the Wumpus World here, getting information about the
# game state from self.gameWorld, and using makeMove() to generate the
# next move.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

import world
import random
import utils
from utils import Directions
from node import Node

import heapq

class Link():

    def __init__(self, dungeon):

        # Make a copy of the world an attribute, so that Link can
        # query the state of the world
        self.gameWorld = dungeon

        # what moves are possible for Link
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        
        # path is set to empty
        self.path = []
    
    ### methods ###
        
    def makeMove(self):
        # This is the function you need to define
        # if we haven't created a path yet, run the chosen one
        if not self.path:
            
            # gets both the gold and Link's location
            linkLoc = self.gameWorld.getLinkLocation()
            goldLoc = self.gameWorld.getGoldLocation()[0]
            print("Link Location:", linkLoc)
            print("Gold Location:", goldLoc)
            
            # Call the required search method:
            #self.path = self.depthFirstSearch(linkLoc, goldLoc)
            #self.path = self.breadthFirstSearch(linkLoc, goldLoc)
            
            #self.path = self.uniformCostSearch(linkLoc, goldLoc)
            #self.path = self.greedySearch(linkLoc, goldLoc)
            #self.path = self.aStarSearch(linkLoc, goldLoc)
            #self.path = self.depthLimitedSearch(linkLoc, goldLoc, 20)
            
            # path index is set to 0
            self.pathIndex = 0
            
        # if successfull in finding a path (by choosing from the above)
        if self.path:
            if self.pathIndex < len(self.path):
                nextMove = self.path[self.pathIndex]
                self.pathIndex += 1  # move to the next step
                return nextMove
            else:
                print("Path complete!")
                self.path = []  # reset path when finished
                return None
        
        # If no path was found, fall back to direct movement toward the gold
        if not self.path:
            # Get the location of the gold
            allGold = self.gameWorld.getGoldLocation()
            nextGold = None
            
            # If there is gold, set nextGold
            if len(allGold) > 0:
                nextGold = allGold[0]
            else:
                print("No gold left!")
                return None  

            # otherwise, set nextGold to the first gold
            nextGold = allGold[0]

            # sets Link's location to myPosition variable
            myPosition = self.gameWorld.getLinkLocation()
            
            # check if there are any possible actions Link can take
            possibleMoves = self.gameWorld.getActions(myPosition)
            
            # If there are no possible moves, return None or stay in place
            if not possibleMoves:
                return None
        
        # if not at the same x coordinate, reduce the difference
        # try to move towards the gold, checking each direction for obstacles
        # check for move towards gold on the x-axis
        if nextGold.x > myPosition.x and Directions.EAST in possibleMoves:
            # check if East is traversable
            if self.gameWorld.isXYTraversable(myPosition.x + 1, myPosition.y):
                return Directions.EAST
            
        elif nextGold.x < myPosition.x and Directions.WEST in possibleMoves:
            # check if West is traversable
            if self.gameWorld.isXYTraversable(myPosition.x - 1, myPosition.y):
                return Directions.WEST
        
        # if not at the same y coordinate, reduce the difference
        # check for move towards gold on the y-axis
        if nextGold.y > myPosition.y and Directions.NORTH in possibleMoves:
            # Check if North is traversable
            if self.gameWorld.isXYTraversable(myPosition.x, myPosition.y + 1):
                return Directions.NORTH
        elif nextGold.y < myPosition.y and Directions.SOUTH in possibleMoves:
            # Check if South is traversable
            if self.gameWorld.isXYTraversable(myPosition.x, myPosition.y - 1):
                return Directions.SOUTH
            
        # if direct path to gold is blocked, consider side moves to avoid Wumpus and pits
        # check if we can make a side move (90-degree turn)
        for move in possibleMoves:
            sideMove = self.gameWorld.sideMove(move)
            if self.gameWorld.isXYTraversable(myPosition.x + sideMove.x, myPosition.y + sideMove.y):
                return sideMove
        
        # checks whether pathIndex is within the valid bounds of the path
        if self.pathIndex <= 0 or self.pathIndex > len(self.path):
            print(f"Invalid pathIndex: {self.pathIndex}, path length: {len(self.path)}")
            return None

        # proceed with accessing the path if it's valid and increment (as we're going through the index)
        self.pathIndex += 1

        # Return the current position in the path
        return self.path[self.pathIndex - 1]

    
    ### SEARCH ALGORITHMS ###
    def depthFirstSearch(self, start, goal):
        print("DFS started!")

        # create a node object
        node = Node(start, None, None)
        
        # goal test:
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []
        
        frontiers = [node] 
        explored = []        
        
        while frontiers:
            
            # LIFO queue
            node = frontiers[-1]
            frontiers = frontiers.pop()
            
            # for each action Link can take
            for action in self.gameWorld.getActions(node.location):
                child = self.createChildNode(node, action)
                
                # note, in the Node class we override the equals operator --- two nodes are equal if the location is the same (which means we can use "not in" here)
                # check for goal
                if child not in explored and child not in frontiers:
                    if child.isGoal(goal):
                        print("Found goal")
                    
                    # add the child to the frontiers list
                    frontiers.append(child)
            
            # add the node to the explored list
            explored.append(node)                        
        
        print("Failed to find a path")
        return []
    
    # just like DFS, but uses a FIFO queue
    def breadthFirstSearch(self, start, goal):
        print("BFS started!")

        node = Node(start, None, None)

        # Goal test:
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []

        frontiers = [node]
        explored = []    

        while frontiers:
            
            # FIFO queue
            node = frontiers[0]
            node = frontiers.pop(0) 

            # For each action Link can take
            for action in self.gameWorld.getActions(node.location):
                child = self.createChildNode(node, action)

                # Check if child is in explored or frontiers
                if child not in explored and child not in frontiers:
                    # Check for goal
                    if child.isGoal(goal):
                        print("Found goal")

                    frontiers.append(child)
            
            explored.append(node)                        

        print("Failed to find a path")
        return []
    
    # similar to BFS, but uses a priority queue
    def uniformCostSearch(self, start, goal):
        node = Node(start, None, None, 0)
        
        # goal test:
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []
        
        frontiers = []
        explored = {}
        
        # uses heapq to create a heap queue
        heapq.heappush(frontiers, (0, node))
        
        while frontiers:
            
            # get the FIRST item from frontiers list
            cost, node = heapq.heappop(frontiers)
            
            # check for goal
            if node.isGoal(goal):
                print("Found goal")
                return self.recoverPlan(node)
            
            explored[node.location.x, node.location.y] = cost
            
            # for each action the vacuum can take
            for action in self.gameWorld.getActions(node.location):
                child = self.createChildNode(node, action)
                child.pathCost = node.pathCost + 1
                
                # note, in the Node class we override the equals operator --- two nodes are equal if the location is the same (which means we can use "not in" here). 
                if (child.location.x, child.location.y) not in explored or explored[(child.location.x, child.location.y)] > child.pathCost:
                    heapq.heappush(frontiers, (child.pathCost, child))
                    explored[(child.location.x, child.location.y)] = child.pathCost                        
        
        print("Failed to find a path")
        return []
    
    # similar to UCS, but uses a priority queue based on the heuristic value
    def greedySearch(self, start, goal):
        node = Node(start, None, None, 0)
        
        # goal test:
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []
        
        # uses heapq to create a heap queue - picks node with LOWEST heuristic value (this value is the closes path to the goal)
        frontiers = []
        heapq.heappush(frontiers, (utils.separation(start, goal), node))
        
        # makes explored into a set
        explored = set()
        
        while frontiers:
            
            # get the FIRST item from the priority frontiers queue
            _, node = heapq.heappop(frontiers)
            
            nodeLocation = (node.location.x, node.location.y)
            
            # check for goal
            if node.isGoal(goal):
                print("Found goal")
                return self.recoverPlan(node)
            
            # mark node as explored
            explored.add(nodeLocation)
            
            # for each action the vacuum can take
            for action in self.gameWorld.getActions(node.location):
                child = self.createChildNode(node, action)
                childLocation = (child.location.x, child.location.y)

                # If the child hasn't been explored, add it based on heuristic
                if childLocation not in explored:
                    
                    # calculates the Euclidean distance between the child and the goal
                    heuristic_value = utils.separation(child.location, goal)
                    
                    # adds the child node with its heuristic value to explored   
                    heapq.heappush(frontiers, (heuristic_value, child))
                    
                    # adds child location to explored list
                    explored.add(childLocation)                 
        
        print("Failed to find a path")
        return []
    
    # similar to UCS and greedy, but avoids local minima and uses heuristics
    def aStarSearch(self, start, goal):
        
        node = Node(start, None, None, 0)
        
        # goal test:
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []
        
        frontiers = []
        heapq.heappush(frontiers, (utils.separation(start, goal) + node.pathCost, node)) # uses heapq to create a heap queue - picks node with LOWEST heuristic value (this value is the closes path to the goal)
        
        explored = set()
        
        while frontiers:
            _, node = heapq.heappop(frontiers) # get the FIRST item
            
            nodeLocation = (node.location.x, node.location.y)
            
            # check for goal
            if node.isGoal(goal):
                print("Found goal")
                return self.recoverPlan(node)
            
            # mark as visited
            explored.add(nodeLocation)
            
            # for each action the vacuum can take
            for action in self.gameWorld.getActions(node.location):
                child = self.createChildNode(node, action)
                childLocation = (child.location.x, child.location.y)

                # If the child hasn't been explored, add it based on heuristics
                if childLocation not in explored:
                    
                    # calculates the Euclidean distance
                    heuristic_value = utils.separation(child.location, goal)
                    
                    heapq.heappush(frontiers, (heuristic_value, child))
                    explored.add(childLocation)              
        
        print("Failed to find a path")
        return []
    
    # similar to DFS, but with a set depth limit
    def depthLimitedSearch(self, start, goal, depthLimit):
        
        # depth is set to 0 because this is the root node
        node = Node(start, None, None, 0)
        
        # goal test:
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []
        
        frontiers = [node] 
        explored = []        
        
        while frontiers:
            
            # LIFO queue because this is DFS
            node = frontiers.pop(0)
            
            if node.depth >= depthLimit:
                print("depth limit reached. Depth Limit:" , depthLimit, "Location: ", node.location)
                continue
            
            # for each action the vacuum can take
            for action in self.gameWorld.getActions(node.location):
                child = self.createChildNode(node, action) 
                
                child.depth = node.depth + 1
                
                # note, in the Node class we override the equals operator --- two nodes are equal if the location is the same (which means we can use "not in" here). 
                if child not in explored and child not in frontiers:
                    
                    # check for goal
                    if child.isGoal(goal):
                        print("Found goal")
                        path = self.recoverPlan(child)
                    
                    # add the child to the frontiers list
                    frontiers.append(child)
            
            # add the node to the explored list
            explored.append(node)     
        
        print("Failed to find a path")
        return []
    
    ### methods that help the algorithms run ###
    # creates a child node of the parent for the given direction
    def createChildNode(self, parent, action):
        if action == Directions.EAST:
            return Node( utils.Pose(parent.location.x + 1, parent.location.y), parent, action)
        if action == Directions.WEST:
            return Node( utils.Pose(parent.location.x - 1, parent.location.y), parent, action)
        if action == Directions.SOUTH:
            return Node( utils.Pose(parent.location.x, parent.location.y + 1), parent, action)
        if action == Directions.NORTH:
            return Node( utils.Pose(parent.location.x, parent.location.y - 1), parent, action)
        
    # traces back from the goal node to the starting node - returns the path
    def recoverPlan(self, node):
        path = []
        
        while node.parent is not None:
            path.append(node.action)
            node = node.parent
        
        path.reverse()
        
        return path

    # recursive version of recoverPlan() - calls itself recursivley to trace back from the goal node to the starting node
    def recoverPlanRecursive(self, node, plan):
        if node.parent:            
            self.recoverPlanRecursive(node.parent, plan)
            plan.append(node.action)
    
    # defines how 2 nodes are compared for equality - useful for checking if a node has been visited or added to the frontiers
    def __eq__(self, other):
        return isinstance(other, Node) and self.location == other.location

    # allows node objects to be used in the sets - hashes them based on their location
    def __hash__(self):
        return hash(self.location)
