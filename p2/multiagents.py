import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.distance import manhattan
from pacai.core.directions import Directions

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # collect legal moves.
        legalMoves = gameState.getLegalActions()
        # choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]
        # get action needs to return the best action as pacman

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        # generate the successor game state
        # after taking in the action that was specificed
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # getScaredTime is the time
        newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]
        # initialize a score based on the current game state's score
        score = successorGameState.getScore()
        # calculate distances to the closest food pellet
        foodDistances = [manhattan(newPos, food) for food in newFood.asList()]
        if foodDistances:
            closestFoodDistance = min(foodDistances)
            # add a positive score for being closer to the food
            # the reciprocal of the distance is used here???
            score += 1.0 / closestFoodDistance
        # avoid ghosts if they are not scared, and approach them if they are
        for ghost, scaredTime in zip(newGhostStates, newScaredTimes):
            ghostPos = ghost.getPosition()
            # if a ghost is too close, and not scared
            # then aviod it (negative score?)
            if scaredTime == 0 and manhattan(newPos, ghostPos) < 2:
                score -= 1000  # strongly avoid ghosts
            # if a ghost is too close and scared
            # approach it (positive score)
            elif scaredTime > 0 and manhattan(newPos, ghostPos) < 2:
                score += 500  # approach scared ghosts
        return score

        return successorGameState.getScore()

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    # you can have a max amount of 4 agents
    # this will be you and three ghosts DO NOT HARDCOE THIS, it will change
    # one turn in minimaz has a depth of 1, at the end, depth of 4
    def __init__(self, index, **kwargs):
        # mean that you are inheriting from another class
        # **kwargs means that it takes in the name and the variable argument
        super().__init__(index, **kwargs)
        # there is no depth given, create one
    
    '''
    def getAction(self, gameState):
        totalDepth = self.getTreeDepth()
        # TESTING to check tree depth
        # print(totalDepth)
        # take out return later
        # call the first pass through of the min max exchange
        newstate =
        value = self.maxValue(gameState)
    '''

    def getAction(self, state):
        # here state is the game state??? CHECK THIS KAI
        # totalDepth = self.getTreeDepth()
        # get the legal actions for Pac-Man (agent 0).
        legalActions = state.getLegalActions(0)
        # initialize the best action and best value.
        bestAction = Directions.STOP
        bestValue = float('-inf')
        # iterate through legal actions and find the one with the maximum value.
        for action in legalActions:
            successorState = state.generateSuccessor(0, action)
            # start with ghost 1 at depth 0.
            # create a new state
            value = self.minValue(successorState, 1, 0)
            if value > bestValue:
                bestValue = value
                # change the action score if better
                bestAction = action
            return bestAction
        
    def maxValue(self, state, depth, ghostIndex):
        # going from bottom up, hence decrement the depth
        # base case #1: tree depth reached
        # base case #2: if you win
        # base case #3: if you loose
        # prev. if depth >= self.depth
        if depth <= 0 or state.isWin() or state.isLose():
            # if we've reached the specified depth or a terminal state (win or lose)
            # return the state's evaluation.
            return self.getEvaluationFunction()(state)
        legalActions = state.getLegalActions(0)
        # initialize the best value to negative infinity.
        bestValue = float('-inf')
        for action in legalActions:
            successorState = state.generateSuccessor(0, action)
            # call minValue for the first ghost.
            value = self.minValue(successorState, depth - 1, ghostIndex)
            # update the best value with the maximum value.
            bestValue = max(bestValue, value)
        return bestValue

    def minValue(self, state, depth, ghostIndex):
        '''
        if depth >= self.depth or state.isWin() or state.isLose():
            # if we've reached the specified depth or a terminal state (win or lose)
            # return the state's evaluation.
            return self.getEvaluationFunction()(state)
        '''
        # use modulo check and increment the turn
        # REVISIT MODULO IN PYTHON
        # check if you have won or lost
        if depth <= 0 or state.isWin() or state.isLose():
            # if we've reached the specified depth or a terminal state (win or lose)
            # return the state's evaluation.
            return self.getEvaluationFunction()(state)
        legalActions = state.getLegalActions(ghostIndex)
        # initialize the best value to positive infinity.
        bestValue = float('inf')
        for action in legalActions:
            if ghostIndex == (state.getNumAgents() - 1):
                # if this is the last ghost, call maxValue for pacman
                successorState = state.generateSuccessor(ghostIndex, action)
                value = self.maxValue(successorState, depth - 1, 0)
            else:
                # call minValue for the next ghost.
                successorState = state.generateSuccessor(ghostIndex, action)
                value = self.minValue(successorState, depth, (ghostIndex + 1) % state.getNumAgents())
            # update the best value with the minimum value.
            bestValue = min(bestValue, value)
        return bestValue

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """
    
    # according to batu:
    # alpha beta only needs 4-5 lines added
    # other than that it is the same as minimax
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    return currentGameState.getScore()

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
