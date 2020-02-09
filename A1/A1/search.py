# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 0
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>

"""
#####################################################
#####################################################

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def genericGraphSearch(problem, data_struct):
    """
        Returns search result provided a data structure type (more like implementation)
        Works as a skeleton for depth and breadth first search, and creates fringe most appropriate to search
    """
    visited_set = [] #initialized set of visited nodes
    data_struct.push((problem.getStartState(), [], 0)) #push starting state with 0 cost and no actions list into fringe
    while not data_struct.isEmpty():    #while queue/stack is not  empty
        state, actions, cost = data_struct.pop()    #remove a node, deepest node for dfs, shallowest for bfs
        if state not in visited_set:                #if state removed is not already visited
            visited_set.append(state)               #add to visited state
            if problem.isGoalState(state):          #if goal state, return actions
                return actions
            for successor_state, successor_actions, successor_cost in problem.getSuccessors(state):
                #for successor states, actions and cost from current state
                actions_path = actions + [successor_actions]    #calculate total actions
                data_struct.push((successor_state, actions_path, successor_cost)) #add to our frontier/fringe
    return []


def depthFirstSearch(problem):
    """
    Q1.1
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ( problem.getStartState() )
    You will get (5,5)

    print (problem.isGoalState(problem.getStartState()) )
    You will get True

    print ( problem.getSuccessors(problem.getStartState()) )
    You will get [((x1,y1),'South',1),((x2,y2),'West',1)]
    """
    "*** YOUR CODE HERE ***"
    """intiialize fringe empty stack here"""
    frontier = util.Stack() #initialize stack and call skeleton graph search
    return genericGraphSearch(problem, frontier)

def breadthFirstSearch(problem):
    """
    Q1.2
    Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue() #initialize queue and call skeleton graph search
    return genericGraphSearch(problem, frontier)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Q1.3
    Search the node that has the lowest combined cost and heuristic first."""
    """Call heuristic(s,problem) to get h(s) value."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue() #similar to dfs and bfs, comments only where the differences are
    frontier.push((problem.getStartState(), [], 0), 0) #now pushing into fringe/frontier with priority as well
    visited_set = []
    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()
        if problem.isGoalState(state):
            return actions
        if state not in visited_set:
            visited_set.append(state)
            for successor_state, successor_actions, successor_cost in problem.getSuccessors(state):
                #we now calculate f(n) = g(n) + h(n), using cost of current state, successor_states as well as heuristic
                f = successor_cost + cost + heuristic(successor_state, problem)
                #push into fringe with priority f(n)
                frontier.push((successor_state, actions + [successor_actions], successor_cost + cost), f)
    return []


def priorityQueueDepthFirstSearch(problem):
    """
    Q1.4a.
    Reimplement DFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue() #similar to astar, except for depth first
    visited_set = []
    frontier.push((problem.getStartState(), [], 0), 0) #initial priority  0
    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()
        if state not in visited_set:
            visited_set.append(state)
            if problem.isGoalState(state):
                return actions
            for successor_state, successor_actions, successor_cost in problem.getSuccessors(state):
                #depth first implementation so priority is assigned based on length of actions in path
                #deepest nodes will have higher length_path
                actions_path = actions + [successor_actions]
                length_path = len(actions_path)
                #pushed negated length path to prioritize highest magnitude values first
                frontier.push((successor_state, actions_path, successor_cost), -length_path)
    return []

def priorityQueueBreadthFirstSearch(problem):
    """
    Q1.4b.
    Reimplement BFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue() #almsot identical to dfs2, differences commented
    visited_set = []
    frontier.push((problem.getStartState(), [], 0), 0)
    while not frontier.isEmpty():
        level = 0   #initialize level, think of this is as the depth of the graph/tree
        state, actions, cost = frontier.pop()
        if state not in visited_set:
            visited_set.append(state)
            if problem.isGoalState(state):
                return actions
            for successor_state, successor_actions, successor_cost in reversed(problem.getSuccessors(state)):
                #notice this is now done in reversed successors order
                actions_path = actions + [successor_actions] #actions_path remains the same
                level = level + 1   #level increases for shallower actions
                frontier.push((successor_state, actions_path, successor_cost), level)
                #priority based on level, therefore highest priority returned first, which will be the shallower actions
    return []

#####################################################
#####################################################
# Discuss the results of comparing the priority-queue
# based implementations of BFS and DFS with your original
# implementations.

"""
<Your discussion goes here>
algorithm used       mazeType         nodes expanded      cost      delta (nodes)     delta(cost)
bfs                  mediumMaze       269                 68        
bfs2                 mediumMaze       180                 68        -89               0
dfs                  mediumMaze       146                 130       
dfs2                 mediumMaze       269                 246       -33               +130 
bfs                  bigMaze          620                 210       
bfs2                 bigMaze          558                 210       -62
dfs                  bigMaze          390                 210               
dfs2                 bigMaze          466                 210       +
astar                mediumMaze       269                 68
astar                bigMaze          620                 210       (for reference)

The difference is visible in this table. In the case of bfs implemented with a priority queue, bfs2 improved it in
both bigMaze as well as mediumMaze with less nodes expanded in both cases. dfs2 provided a marginal improvement for
mediumMaze and a drop in performance for bigMaze, with MORE nodes expanded than originally. Most likely,
this is due to the priority queue prioritizing nodes with more depth even more, which means it keeps exploring paths
even if they don't lead to the goalstate
"""



#####################################################
#####################################################



# Abbreviations (please DO NOT change these.)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
bfs2 = priorityQueueBreadthFirstSearch
dfs2 = priorityQueueDepthFirstSearch