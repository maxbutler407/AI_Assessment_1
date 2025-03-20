# puzzleWorld.py
#
# A file that represents a puzzle version of the Wumpus World, keeping
# track of the position of the Wumpus and Link.
#
# Written by: Simon Parsons
# Last Modified: 17/12/24

import random
import config
import utils
import copy
import heapq
from world import World
from utils import Pose
from utils import Directions
from utils import State
from node import Node

class PuzzleWorld(World):

    def __init__(self):

        # Import boundaries of the world. because we index from 0,
        # these are one less than the number of rows and columns.
        self.maxX = config.worldLength - 1
        self.maxY = config.worldBreadth - 1

        # Keep a list of locations that have been used.
        self.locationList = []

        # Wumpus
        self.wLoc = []
        for i in range(config.numberOfWumpus):
            newLoc = utils.pickUniquePose(self.maxX, self.maxY, self.locationList)
            self.wLoc.append(newLoc)
            self.locationList.append(newLoc)

        # Link
        newLoc = utils.pickUniquePose(self.maxX, self.maxY, self.locationList)
        self.lLoc = newLoc
        self.locationList.append(newLoc)
        
        # Other elements that we don't use
        self.pLoc = []
        self.gLoc = []
        
        # Game state
        self.status = utils.State.PLAY

        # What moves are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]

        # A plan
        self.plan = [[Directions.NORTH, 0, 0], [0, Directions.NORTH, 0], [0, 0, Directions.NORTH]]

    #
    # Methods
    #
    # These are the functions that are used to update and report on
    # puzzle information.
    def isSolved(self, goal):
        if utils.sameAs(self, goal):
            self.status = utils.State.WON 
            print("Puzzle Over!")
            return True
        else:
            return False

    # A single move is to shift Link or one Wumpus in one direction.
    #
    # This relies on having something in self.plan. Once this has been
    # reduced to [], this code will just print a message each step.
    #
    # This is where you should start writing your solution to the
    # puzle problem.
    def makeAMove(self, goal):
        
        ### Link's movement logic ###
        # goal is a pose object that represents the stationary Link's position
        lGoalLocation = goal.lLoc

        # CHOOSE 1 FROM THE FOLLOWING ALGORITHMS (do the same for Wumpus):
        #self.plan = self.greedySearch(self.lLoc, lGoalLocation)
        self.plan = self.aStarSearch(self.lLoc, lGoalLocation)
        
        #self.plan = self.breadthFirstSearch(self.lLoc, lGoalLocation)
        #self.plan = self.depthFirstSearch(self.lLoc, lGoalLocation)
        #self.plan = self.uniformCostSearch(self.lLoc, lGoalLocation)
        
        # validate the generated plan
        print(f"Link plan generated: {self.plan}")
        
        # if there are moves in the plan, execute them
        if self.plan:
            
            # get the first move from the plan
            lNextMove = self.plan.pop(0)
            
            # calls the takeStep method to move Link
            self.takeStep(lNextMove)
                
        else:
            print("No Link plan available or Link already at the goal!")

        # check if the puzzle is solved after making the move
        if utils.sameLink(self, goal):
            self.status = utils.State.WON
        
        
        ### Wumpus movement logic ###
        # goal is a pose object that represents the stationary Wumpus' positions
        wGoalLocation = goal.wLoc

        # iterate through each Wumpus and calculate its move
        for wumpusIndex in range(len(self.wLoc)):
            
            # current wumpus is based off where in the index we are
            currentWumpus = self.wLoc[wumpusIndex]
            
            # corresponding target position
            wTargetPosition = wGoalLocation[wumpusIndex]

            # CHOOSE 1 FROM THE FOLLOWING ALGORITHMS (do the same for Link):
            #wumpusPlan = self.greedySearch(currentWumpus, wTargetPosition)
            wumpusPlan = self.aStarSearch(currentWumpus, wTargetPosition)
            
            #wumpusPlan = self.breadthFirstSearch(currentWumpus, wTargetPosition)
            #wumpusPlan = self.depthFirstSearch(currentWumpus, wTargetPosition)
            #wumpusPlan = self.uniformCostSearch(currentWumpus, wTargetPosition)
            
            # validate the generated plan
            print(f"Wumpus {wumpusIndex} plan generated: {wumpusPlan}")

            if wumpusPlan:
                
                # unwrap direction from the plan
                wNextMove = wumpusPlan.pop(0)[0]

                # Initialize move list with zeros
                wumpus_moves = [0] * len(self.wLoc)
                
                # assign a move for this Wumpus
                wumpus_moves[wumpusIndex] = wNextMove

                # validates whether the wumpus has made a move
                print(f"Before step for Wumpus {wumpusIndex}: {currentWumpus}")
                
                # calls the takeStep method to move the Wumpus
                self.takeStep([0] + wumpus_moves)
                print(f"After step for Wumpus {wumpusIndex}: {self.wLoc[wumpusIndex]}")
                
            else:
                print(f"No plan for Wumpus {wumpusIndex} or Wumpus already at the goal.")



    # A move is a list of the directions that [Link, Wumpus1, Wumpus2,
    # ...] move in.  takeStep decodes these and makes the relevant
    # change to the state. Basically it looks for the first list
    # element that is non-zero and interprets this as a
    # direction. Movements that exceed the limits of the world have no
    # effect.
    def takeStep(self, move):
        
        # Debug the input move
        print(f"takeStep received move: {move}")
        print(f"Move type: {type(move)}, Direction type: {type(move[0])}")

        # Move Link
        if move[0] != 0:
            print("Moving Link")
            direction = move[0]
            if direction == Directions.NORTH and self.lLoc.y > 0:
                
                # move North
                self.lLoc.y -= 1
            elif direction == Directions.SOUTH and self.lLoc.y < self.maxY:
                
                # move South
                self.lLoc.y += 1
            elif direction == Directions.EAST and self.lLoc.x < self.maxX:
                
                # move East
                self.lLoc.x += 1
            elif direction == Directions.WEST and self.lLoc.x > 0:
                
                # move West
                self.lLoc.x -= 1
                print(f"Link moved to: {self.lLoc}")
                
        # Otherwise move the relevant Wumpus
        else:
            for i in range(1, len(self.wLoc) + 1):
                if move[i] != 0:
                    
                    # helpful debug statements
                    print(f"Processing Wumpus {i-1}'s move: {move[i]}")
                    print(f"Wumpus {i-1}'s position before move: {self.wLoc[i-1]}")
                    direction = move[i]
                    
                    # adjust the index for wLoc
                    j = i - 1
                    if direction == Directions.NORTH and self.wLoc[j].y > 0:
                        
                        # move North
                        self.wLoc[j].y -= 1
                    elif direction == Directions.SOUTH and self.wLoc[j].y < self.maxY:
                        
                        # move South
                        self.wLoc[j].y += 1
                    elif direction == Directions.EAST and self.wLoc[j].x < self.maxX:
                        
                        # move East
                        self.wLoc[j].x += 1
                    elif direction == Directions.WEST and self.wLoc[j].x > 0:
                        
                        # move West
                        self.wLoc[j].x -= 1
                    print(f"Wumpus {i-1}'s position after move: {self.wLoc[j]}")
                            
                            
    ### search algorithms and their required methods ###
    def greedySearch(self, start, goal):
        
        print(f"Starting Greedy Search from {start} to {goal}")
        node = Node(start, None, None, 0)
        
        # Goal test:
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []
        
        frontiers = []
        heapq.heappush(frontiers, (utils.separation(start, goal), node))  # use heapq for priority queue
        explored = set()
        
        while frontiers:
            _, node = heapq.heappop(frontiers)  # get the node with the lowest heuristic value
            
            nodeLocation = (node.location.x, node.location.y)
            print(f"Exploring node at {nodeLocation}")
            
            # check if the moving one matches the stationary one (goal state)
            if node.location == goal:  # compare the current state with the goal state
                return self.recoverPlan(node)
            
            # check for goal
            if node.isGoal(goal):
                print("Found goal")
                return self.recoverPlan(node)
            
            # mark the node as explored after popping it from the frontier
            explored.add(nodeLocation)
            
            # for each action the agent can take
            for action in self.getActions(node.location):
                child = self.createChildNode(node, action)
                child_location = (child.location.x, child.location.y)

                # if the child hasn't been explored and isn't already in the frontier
                if child_location not in explored:
                    heuristic_value = utils.separation(child.location, goal)  # calculate the Euclidean distance
                    heapq.heappush(frontiers, (heuristic_value, child))
                    print(f"Adding child node at {child_location} with heuristic {heuristic_value}")
        
        print("Failed to find a path")
        return []
    
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
            
            explored.add(nodeLocation)  # mark as visited
            
            # for each action the vacuum can take
            for action in self.getActions(node.location):
                child = self.createChildNode(node, action)
                child_location = (child.location.x, child.location.y)

                # if the child hasn't been explored, add it based on heuristic
                if child_location not in explored:
                    heuristic_value = utils.separation(child.location, goal)  # calculate the Euclidean distance
                    heapq.heappush(frontiers, (heuristic_value, child))
                    explored.add(child_location)  # add to explored                    
        
        print("Failed to find a path")
        return []
    
    def depthFirstSearch(self, start, goal):
        print("DFS started!")

        node = Node(start, None, None)
        
        # goal test:
        if node.isGoal(goal):
            return []
        
        frontiers = [node] 
        explored = []        
        
        while frontiers:
            node = frontiers[-1] # get the last item
            frontiers = frontiers[:-1] # remove the last item
            
            # for each action Link can take
            for action in self.getActions(node.location):
                child = self.createChildNode(node, action)
                
                # note, in the Node class we override the equals operator --- two nodes are equal if the location is the same (which means we can use "not in" here). 
                if child not in explored and child not in frontiers:

                    # check for goal
                    if child.isGoal(goal):
                        print("Found goal")
                        #path = self.recoverPlan(child)
                        #print("Recovered path:", path)  # Add this line to check the recovered path
                    frontiers.append(child)
            
            explored.append(node)                        
        
        print("Failed to find a path")
        return []
    
    def breadthFirstSearch(self, start, goal):
        print("BFS started!")

        node = Node(start, None, None)
        print("Node created!")

        # Goal test:
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []

        frontiers = [node]  # BFS uses a queue (FIFO)
        explored = []    

        while frontiers:
            node = frontiers[0]  # Get the FIRST item (FIFO)
            node = frontiers.pop(0)  # Remove from the front (FIFO)  # Remove the FIRST item

            # For each action Link can take
            for action in self.getActions(node.location):
                child = self.createChildNode(node, action)

                # Check if child is in explored or frontiers
                if child not in explored and child not in frontiers:
                    # Check for goal
                    if child.isGoal(goal):
                        print("Found goal")
                    frontiers.append(child)  # BFS adds new nodes to the **end** (FIFO)
            
            explored.append(node)                        

        print("Failed to find a path")
        return []
    
    def uniformCostSearch(self, start, goal):
        node = Node(start, None, None, 0)
        
        # goal test:
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []
        
        frontiers = []
        heapq.heappush(frontiers, (0, node)) # uses heapq to create a heap queue
        explored = {}
        
        while frontiers:
            cost, node = heapq.heappop(frontiers) # get the FIRST item
            
            # check for goal
            if node.isGoal(goal):
                print("Found goal")
                return self.recoverPlan(node)
            
            explored[node.location.x, node.location.y] = cost
            
            # for each action the vacuum can take
            for action in self.getActions(node.location):
                child = self.createChildNode(node, action)
                child.pathCost = node.pathCost + 1
                
                # note, in the Node class we override the equals operator --- two nodes are equal if the location is the same (which means we can use "not in" here). 
                if (child.location.x, child.location.y) not in explored or explored[(child.location.x, child.location.y)] > child.pathCost:
                    heapq.heappush(frontiers, (child.pathCost, child))
                    explored[(child.location.x, child.location.y)] = child.pathCost                        
        
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
            path.append([node.action])  # Wrap node.action in a list
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
