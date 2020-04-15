# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        # print newPos
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        from sys import maxint
        foodlist = newFood.asList()
        closestFood = maxint  # uses maxint from sys, maybe use float('inf')?? not sure
        closestGhost = maxint
        for food in foodlist:
            # find the distance to the closest dot, reassign if food found closer
            closestFood = min(manhattanDistance(newPos, food), closestFood)
        for ghost in newGhostStates:
            # find the distance to the closest ghost, reassign if ghost found closer
            closestGhost = min(manhattanDistance(ghost.getPosition(), newPos), closestGhost)
        if closestGhost == 0:
            # if ghost is right next to us, this is the worst utility so return the most negative number
            return -maxint
        if sum(newScaredTimes) > 0:
            # if big dot is eaten, see positive utility in going towards ghosts
            score = successorGameState.getScore() + 10.0 / closestFood + 20.0 / closestGhost
        else:
            # regular play, penalty for ghosts, positive utility for food
            score = successorGameState.getScore() + 10.0 / closestFood - 20.0 / closestGhost
        return score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def minimax(self, state, depth, agentIndex, alpha=None, beta=None):
        '''
        This function is an overloaded one for mimimax with alpha beta pruning
        overloaded for simplicity because it is essentially identical to the minimax function
        with the addition of alpha and beta pruning
        :param state: state of the game
        :param depth: depth in tree
        :param agentIndex: the index of the agent which is 0 for pacman, and higher for ghosts
        :param alpha: the lower bound, None for regular minimax
        :param beta: the upper bound, None for regular minimax
        :return: a list of the utility and the actions
        '''
        from sys import maxint
        PACINDEX = 0
        next_action = None
        if depth <= 0 or state.isLose() or state.isWin():
            # if minimum depth reached, or if no more moves left, return current state and no moves
            return self.evaluationFunction(state), None
        if agentIndex == PACINDEX:
            # pacman
            score = -maxint
            for legalAction in state.getLegalActions(agentIndex):
                # for all legalActions for pacman, find the successor states and evaluate utility of ghost now
                successor_state = state.generateSuccessor(agentIndex, legalAction)
                action_evaluation = self.minimax(successor_state, depth, agentIndex + 1, alpha, beta)
                # reassign score and make next action the one with higher utility
                if score < action_evaluation[0]:
                    score = action_evaluation[0]
                    next_action = legalAction
                if alpha and beta is not None:
                    # overloaded function so does alpha beta pruning if alpha and beta are passed to it following
                    # alpha beta algorithm, break if greater than beta, and alpha is whatever's bigger vs score
                    if alpha < score:
                        alpha = score
                    if score > beta:
                        break
        else:
            # for ghosts
            # need to minimize utility
            score = maxint
            for legalAction in state.getLegalActions(agentIndex):
                if agentIndex == (state.getNumAgents() - 1):
                    # getNumAgents returns number of ghosts, go into this if agent is last ghost, (pacman next)
                    action_evaluation = self.minimax(state.generateSuccessor(agentIndex, legalAction), depth - 1,
                                                     PACINDEX, alpha, beta)
                    # evaluation utility at the depth above
                    # print action_evaluation
                else:
                    # not the last ghost, we still need to evaluate for more ghosts at the same depth
                    action_evaluation = self.minimax(state.generateSuccessor(agentIndex, legalAction), depth,
                                                     agentIndex + 1, alpha, beta)
                if score > action_evaluation[0]:
                    score = action_evaluation[0]
                    next_action = legalAction
                if alpha and beta is not None:
                    # overloaded function so does alpha beta pruning if alpha and beta are passed to it
                    # following alpha beta algorithm, break if less than alpha, and beta is whatever's smaller vs score
                    if score < alpha:
                        break
                    if score < beta:
                        beta = score
        return score, next_action


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        PACINDEX = 0
        return self.minimax(gameState, self.depth, PACINDEX)[1]


#        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        from sys import maxint
        PACINDEX = 0
        # call overloaded minimax with -infinity as alpha and infinity as beta
        return self.minimax(gameState, self.depth, PACINDEX, -maxint, maxint)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax(self, state, depth, agentIndex):
        '''
        similar to minimax except for adversaries we now average the scores
        :param state: state of game
        :param depth: depth in tree
        :param agentIndex: the index of the agent which is 0 for pacman, and higher for ghosts
        :return: list of utility and the next actions
        '''
        # very similar function to minimax
        from sys import maxint
        PACINDEX = 0
        next_action = None
        if depth <= 0 or state.isLose() or state.isWin():
            # if minimum depth reached, or if no more moves left, return current state and no moves
            return self.evaluationFunction(state), None
        if agentIndex == PACINDEX:
            # pacman (maximize)
            score = -maxint
            for legalAction in state.getLegalActions(agentIndex):
                # for all legalActions for pacman, find the successor states and evaluate utility of ghost now
                successor_state = state.generateSuccessor(agentIndex, legalAction)
                action_evaluation = self.expectimax(successor_state, depth, agentIndex + 1)
                if score < action_evaluation[0]:
                    # reassign score and make next action the one with higher utility
                    score = action_evaluation[0]
                    next_action = legalAction
        else:
            # ghosts (minimize)
            score = 0  # score is now set to 0 instead of -"infinity" because we are continuously adding to it
            action_count = len(state.getLegalActions(agentIndex))  # get total number of legal actions
            for legalAction in state.getLegalActions(agentIndex):
                if agentIndex == (state.getNumAgents() - 1):
                    # getNumAgents returns number of ghosts, if agent is last ghost
                    action_evaluation = self.expectimax(state.generateSuccessor(agentIndex, legalAction), depth - 1,
                                                        PACINDEX)  # [0]
                    # print action_evaluation
                else:
                    action_evaluation = self.expectimax(state.generateSuccessor(agentIndex, legalAction), depth,
                                                        agentIndex + 1)
                score += action_evaluation[0]/float(action_count)  # convert to float to avoid integer division
                # average score is now added to existing score, and legal action is the next action
                next_action = legalAction
        return score, next_action

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        PACINDEX = 0
        return self.expectimax(gameState, self.depth, PACINDEX)[1]
        # util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # identical to evaluation function, replaced instances of successorGameState
    from sys import maxint
    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    pos = currentGameState.getPacmanPosition()
    # print newPos
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    foodlist = food.asList()
    closestFood = maxint
    for food in foodlist:
        closestFood = min(manhattanDistance(pos, food), closestFood)
    closestGhost = maxint
    for ghost in ghostStates:
        closestGhost = min(manhattanDistance(ghost.getPosition(), pos), closestGhost)
    if closestGhost == 0:
        return -maxint
    if sum(scaredTimes) > 0:
        score = currentGameState.getScore() + 10.0 / closestFood + 20.0 / closestGhost
    else:
        score = currentGameState.getScore() + 10.0 / closestFood - 20.0 / closestGhost
    return score

# util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
