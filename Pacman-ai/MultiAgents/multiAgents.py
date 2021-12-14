"""
Name: Mohamed Yousef
ID: 211668975
"""
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        succGhostPos = successorGameState.getGhostPositions()
        if len(newFood.asList())==0:
            food = 1
        else :
            #the closer the food the better
            minDis = float('inf')
            for foodPosition in newFood.asList():
                minDis = min(manhattanDistance(newPos, foodPosition), minDis)
                food = 1/minDis
        minDis = float('inf')
        for ghostPosition in succGhostPos:
          minDis = min(manhattanDistance(newPos, ghostPosition), minDis)
        #check if worst case
        if minDis <= 1: return float('-inf')
        return successorGameState.getScore() + food
    
       

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxScoreAction(gameState,depth, index):
          if depth < 1 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          maxScore = float('-inf')
          for action in gameState.getLegalActions(index):
            succ = gameState.generateSuccessor(index,action)
            score = minScoreAction(succ,depth,index + 1)
            if score > maxScore:
              maxScore = score
              maxAction = action
          if depth == self.depth:
              #print(maxScore)
              return maxAction
          else: return maxScore

        def minScoreAction(gameState,depth,index):
          if depth < 1 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          minScore = float('inf')
          if index < gameState.getNumAgents()-1:
              #continue at the same depth
                for action in gameState.getLegalActions(index):
                  succ = gameState.generateSuccessor(index,action)
                  score = minScoreAction(succ,depth,index + 1)
                  minScore = min(minScore, score)
                return minScore
          else:
              #go to the max func with new depth
               for action in gameState.getLegalActions(index):
                 succ = gameState.generateSuccessor(index,action)
                 score = maxScoreAction(succ,depth - 1,0)
                 minScore = min(minScore, score)
               return minScore
        #return the action that has the maxscore
        return maxScoreAction(gameState,self.depth, 0)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxActionScore(state,depth, index, a, b):
          if depth < 1 or state.isLose() or state.isWin():
            return self.evaluationFunction(state)
          v = float("-inf")
          for action in state.getLegalActions(index):
            successor = state.generateSuccessor(index,action)
            score = minScore(successor,depth, index+1, a, b)
            if score > v:
              v = score
              maxAction = action
            if v > b:
              return v
            a = max(a,v)
         #check if we finished
          if depth == self.depth:
              #print(v)
              return maxAction
          else: return v

        def minScore(state,depth,index, a, b):
          if depth < 1 or state.isLose() or state.isWin():
            return self.evaluationFunction(state)
          v = float("inf")
          if index < state.getNumAgents()-1:
              #continue with the agents at the same depth
             for action in state.getLegalActions(index):
               successor = state.generateSuccessor(index,action)
               score = minScore(successor,depth,index + 1 , a, b)
               if score < v:
                 v = score
               if v < a:
                 return v
               b = min(b,v)
             return v
          else:
             #go to the max func in the next depth
             for action in state.getLegalActions(index):
               successor = state.generateSuccessor(index,action)
               score = maxActionScore(successor,depth - 1,0, a, b)
               if score < v:
                 v = score
               if v < a:
                 return v
               b = min(b,v)          
             return v
             
        
        return maxActionScore(gameState,self.depth,0, float("-inf"), float("inf"))



