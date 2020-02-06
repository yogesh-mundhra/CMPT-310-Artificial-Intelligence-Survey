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
    visited_set = []
    data_struct.push((problem.getStartState(), [], 0))
    # visited_set.append(problem.getStartState()) seems to break the 8 problem
    while not data_struct.isEmpty():
        state, actions, cost = data_struct.pop()
        if state not in visited_set:
            visited_set.append(state)
            if problem.isGoalState(state):
                return actions
            for successor_state, successor_actions, successor_cost in problem.getSuccessors(state):
                # visited_set.append(successor_state)
                actions_path = actions + [successor_actions]
                data_struct.push((successor_state, actions_path, successor_cost))
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
    frontier = util.Stack()
    return genericGraphSearch(problem, frontier)

def breadthFirstSearch(problem):
    """
    Q1.2
    Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
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
    frontier = util.PriorityQueue()
    frontier.push((problem.getStartState(), [], 0), 0)
    visited_set = []
    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()
        if problem.isGoalState(state):
            return actions
        if state not in visited_set:
            visited_set.append(state)
            for successor_state, successor_actions, successor_cost in problem.getSuccessors(state):
               # if successor_state not in visited_set:
                f = successor_cost + cost + heuristic(successor_state, problem)
                frontier.push((successor_state, actions + [successor_actions], successor_cost + cost), f)
    return []



def priorityQueueDepthFirstSearch(problem):
    """
    Q1.4a.
    Reimplement DFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    visited_set = []
    frontier.push((problem.getStartState(), [], 0), 0)
    # visited_set.append(problem.getStartState()) seems to break the 8 problem
    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()
        if state not in visited_set:
            visited_set.append(state)
            if problem.isGoalState(state):
                return actions
            for successor_state, successor_actions, successor_cost in problem.getSuccessors(state):
                actions_path = actions + [successor_actions]
                length_path = len(actions_path)
                frontier.push((successor_state, actions_path, successor_cost), -length_path)
    return []

def priorityQueueBreadthFirstSearch(problem):
    """
    Q1.4b.
    Reimplement BFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    visited_set = []
    frontier.push((problem.getStartState(), [], 0), 0)
    # visited_set.append(problem.getStartState()) seems to break the 8 problem
    while not frontier.isEmpty():
        level = 0
        state, actions, cost = frontier.pop()
        if state not in visited_set:
            visited_set.append(state)
            if problem.isGoalState(state):
                return actions
            for successor_state, successor_actions, successor_cost in reversed(problem.getSuccessors(state)):
                actions_path = actions + [successor_actions]
                level = level + 1
                frontier.push((successor_state, actions_path, successor_cost), level)
    return []

#####################################################
#####################################################
# Discuss the results of comparing the priority-queue
# based implementations of BFS and DFS with your original
# implementations.

"""
<Your discussion goes here>
"""



#####################################################
#####################################################



# Abbreviations (please DO NOT change these.)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
bfs2 = priorityQueueBreadthFirstSearch
dfs2 = priorityQueueDepthFirstSearch