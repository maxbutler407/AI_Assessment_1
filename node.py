# node.py
#
#
# Written by: Helen Harman
# Last Modified: 02/02/24

import utils
from location import Location
        
class Node():
    def __init__(self, location, parent, action, depth = 4, pathCost = 0):
        if isinstance(location, tuple):
            # If location is given as (x, y), convert it to a Location object
            self.location = Location(location[0], location[1])
        else:
            # Otherwise, assume it's already a Location object
            self.location = location
        
        self.parent = parent
        self.action = action
        self.parent = parent
        self.action = action
        self.depth = depth if parent is None else parent.depth + 1
        self.pathCost = pathCost

    def __lt__(self, other):  
        return self.pathCost < other.pathCost # needed for heapq comparison     
        
    def isGoal(self, goal):
        #return utils.sameLocation(self.location, goal)
        return self.location == goal
    
    
    def __repr__(self):
        return f"<Node location:{self.location} action:{self.action}>"
            
    def __str__(self):
        return f"[location:{self.location} action:{self.action}]"
        
        
    # by just using the location to check if two Nodes are the same, 
    #    checking if the location has been visited/explored or added to frontiers easier.
    #     -- i.e. we can make use of "in" 
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Node):
            return (self.location == other.location)
        return False    