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
        # get action needs to return the best action as pacman
        return legalMoves[chosenIndex]

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
    # one turn in minimax has a depth of 1, at the end, depth of 4
    def __init__(self, index, **kwargs):
        # mean that you are inheriting from another class
        # **kwargs means that it takes in the name and the variable argument
        super().__init__(index, **kwargs)
        # there is no depth given, create one
    
    def myLegalActions(self, state, agentid):
        # copyactions = state.getLegalActions(agentid)
        # list of [east, stop, east] for ex.
        actions = state.getLegalActions(agentid)
        if (Directions.STOP in actions) or ('Stop' in actions):
            actions.remove('Stop')
        return actions

    def getAction(self, state):
        # starts the search and selects the best action for pacman
        # get the legal actions for pacman (agent 0)
        totalDepth = self.getTreeDepth()
        legalActions = state.getLegalActions(0)
        bestAction = Directions.STOP
        # initialize value to negative infinity
        value = float('-inf')
        # initialize max to negative infinity
        # both are initialized to the worst case
        max = float('-inf')
        # remove/handle STOP action
        legalActions.remove("Stop")
        # iterate through legal actions and go through each action
        # find the one with the minimum value
        for action in legalActions:
            # generate the successor for pacman
            sucessorState = state.generateSuccessor(0, action)
            # start with ghost 1 at depth 1
            # create a new state
            value = self.minValue(sucessorState, totalDepth - 1, 1)
            if value >= max:
                max = value
                bestAction = action
        return bestAction
        pass
        
    def maxValue(self, state, depth, ghostIndex):
        # maximizer function for pacman
        # if we've reached the specified depth or a terminal state (win or lose)
        if depth <= 0 or state.isWin() or state.isLose():
            # return the state's evaluation
            return self.getEvaluationFunction()(state)
        legalActions = state.getLegalActions(0)
        # initialize value to negative infinity
        # set to the worst case
        value = float('-inf')
        # handle/remove STOP action
        legalActions.remove('Stop')
        # iterate through legal actions and go through each action
        for action in legalActions:
            # generate the successor
            successorState = state.generateSuccessor(0, action)
            # call min value for the first ghost
            # call and update the value with max value
            value = max(value, self.minValue(successorState, depth - 1, 1))
        return value
        pass

    def minValue(self, state, depth, ghostIndex):
        # minimizer function for the ghosts
        # if we've reached the specified depth or a terminal state (win or lose)
        if depth <= 0 or state.isWin() or state.isLose():
            # return the state's evaluation
            return self.getEvaluationFunction()(state)
        legalActions = state.getLegalActions(ghostIndex)
        # initialize value to positive infinity
        # set value to the worst possible case for min
        value = float('inf')
        # iterate through legal actions and go through each action
        for action in legalActions:
            # if this is not the last ghost
            # get max for pacman
            if ghostIndex == (state.getNumAgents() - 1):
                # generate the successor state
                successorState = state.generateSuccessor(ghostIndex, action)
                # get the minimizing value and update
                value = min(value, self.maxValue(successorState, depth - 1, 0))
            # else call min for the next ghost
            else:
                # generate the successor state
                successorState = state.generateSuccessor(ghostIndex, action)
                # call the minimizing value and update
                value = min(value, self.minValue(successorState, depth, ghostIndex + 1))
        return value
        pass

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

    def getAction(self, state, depth = 4):
        # get the legal actions for pacman (agent 0)
        legalActions = state.getLegalActions(0)
        bestAction = Directions.STOP
        # initialize alpha to negative infinity
        alpha = float('-inf')
        # initialize beta to poisitve infinity
        beta = float("inf")
        for action in legalActions:
            sucessorState = state.generateSuccessor(0, action)
            value = self.minValue(sucessorState, depth - 1, 1, alpha, beta)
            if value > alpha:
                alpha = value
                bestAction = action
        return bestAction
    
    def maxValue(self, state, depth, ghostIndex, alpha, beta):
        # maximizer function for pacman
        if depth <= 0 or state.isWin() or state.isLose():
            return self.getEvaluationFunction()(state)
        legalActions = state.getLegalActions(0)
        value = float('-inf')
        for action in legalActions:
            successorState = state.generateSuccessor(0, action)
            value = max(value, self.minValue(successorState, depth - 1, 1, alpha, beta))
            if value >= beta:
                # prune the rest of the branches
                return value
            alpha = max(alpha, value)
        return value

    def minValue(self, state, depth, ghostIndex, alpha, beta):
        # minimizer function for the ghosts
        if depth <= 0 or state.isWin() or state.isLose():
            return self.getEvaluationFunction()(state)
        legalActions = state.getLegalActions(ghostIndex)
        value = float('inf')
        for action in legalActions:
            if ghostIndex == (state.getNumAgents() - 1):
                successorState = state.generateSuccessor(ghostIndex, action)
                value = min(value, self.maxValue(successorState, depth - 1, 0, alpha, beta))
            else:
                successorState = state.generateSuccessor(ghostIndex, action)
                value = min(value, self.minValue(successorState, depth, ghostIndex + 1,
                                                 alpha, beta))
            if value <= alpha:
                # prune the rest of the branches
                return value
            beta = min(beta, value)
        return value

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

    def getAction(self, state):
        # start the search and select the best action for pacman
        # get the legal actions for pacman (agent 0)
        legalActions = state.getLegalActions(0)
        totalDepth = self.getTreeDepth()
        # initialize the best action and best value
        bestAction = Directions.STOP
        # initialize value to negative infinity
        value = float('-inf')
        # initialize max to negative infinity
        # both are initialized to the worst possible case
        max = float('-inf')
        # iterate through legal action and go through each actio
        for action in legalActions:
            # generate the successor state for pacman
            successorState = state.generateSuccessor(0, action)
            # start the expectimax search for ghosts
            # ghost 1, at depth 1?
            value = self.minValue(successorState, totalDepth, 1)
            # if the value for this action is better, update the best action and value
            if value > max:
                max = value
                bestAction = action
        return bestAction
    
    def maxValue(self, state, depth, ghostIndex):
        # the expectation is based on my agent's model of how the ghosts act
        # if we have reached the specified depth or a terminal state (win or lose)
        if depth <= 0 or state.isWin() or state.isLose():
            # return the state's evaluation
            return self.getEvaluationFunction()(state)
        # pacman's turn
        # get the legal actions at index 0
        legalActions = state.getLegalActions(ghostIndex)
        # initialize value to negative infinity
        # set to the worst case
        value = float('-inf')
        # handle/remove the STOP action
        legalActions.remove('Stop')
        # iterate through the legal actions and go through each action
        for action in legalActions:
            # KAIA CHECK: do we want to index agentIndex for every action?
            # agentIndex = agentIndex + 1
            # generate the successor for pacman at index 0
            successorState = state.generateSuccessor(0, action)
            # continue the expectimax search with the next agent (ghost)
            # decrement depth??? was just depth changing to depth - 1
            # call and update value with the max value at index 1
            value = max(value, self.minValue(successorState, depth - 1, 1))
        return value
        
    def minValue(self, state, depth, ghostIndex):
        # minimizer function for the ghosts
        # if we've reached the specified depth or a terminal state (win or lose)
        if depth <= 0 or state.isWin() or state.isLose():
            # return the state's evaluation
            return self.getEvaluationFunction()(state)
        # ghosts' turn (expectation)
        # get the legal actions for the current ghost
        legalActions = state.getLegalActions(ghostIndex)
        # initialize value to positive infinity
        # set value to the worst possible case for min
        value = float('inf')
        totalValue = 0
        # iterate through legal actions and go through each action
        for action in legalActions:
            # if this is not the last ghost
            # get the max for pacman
            if ghostIndex == (state.getNumAgents() - 1):
                # generate the successor state
                successorState = state.generateSuccessor(ghostIndex, action)
                # get the minimizing value and update
                value = min(value, self.maxValue(successorState, depth - 1, 0))
                # accumulate the values for the pacman moves
                totalValue += value
            # else call min for the next ghost
            else:
                # generate the successor state
                successorState = state.generateSuccessor(ghostIndex, action)
                # call the minimizing value and update
                # continue the expectimax search with the next agent
                value = min(value, self.minValue(successorState, depth, ghostIndex + 1))
                # accumulate the values for each ghost move
                totalValue += value
        # return the average value for the ghost's moves (expectation)
        return totalValue / len(legalActions)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    """
    improved evaluation function for pacman
    DESCRIPTION: this evaluation function focuses on other important factors to make pacman
    perform better. it considers the following:
    1. current score: pacman's current score reflects his progress, so we want to maximize it.
    2. remaining food: the number of remaining food dots is a crucial factor. we want to
       prioritize eating remaining food.
    3. capsules: eating capsules can make pacman fearless, so we consider them in the evaluation.
    4. ghosts: we want to avoid ghosts as much as possible. the distance to the nearest ghost is
       inversely proportional to the evaluation.

    we use a weighted sum of these factors to evaluate the current state, but we return
    currentGameState.getScore() as the final evaluation.
    """
    
    # get the game state data
    gameState = currentGameState
    # extract relevant information
    score = gameState.getScore()
    pacmanPosition = gameState.getPacmanState().getPosition()
    food = gameState.getFood().asList()
    remainingFood = len(food)
    capsules = gameState.getCapsules()
    ghosts = gameState.getGhostStates()
    # initialize the evaluation score with the current score
    evaluation = score
    # weight factors for the evaluation components
    foodWeight = 10
    capsuleWeight = 5
    ghostWeight = -20
    # update the evaluation based on the factors
    evaluation += remainingFood * foodWeight
    evaluation += len(capsules) * capsuleWeight
    # calculate the proximity to the nearest ghost
    ghostDistances = [manhattan(pacmanPosition, ghost.getPosition()) for ghost in ghosts]
    nearestGhostDistance = min(ghostDistances)
    # avoid division by zero by handling the case when nearestGhostDistance is zero
    if nearestGhostDistance == 0:
        # a large negative value to indicate extreme undesirability
        ghostWeight = -float('inf')
    else:
        # adjust the evaluation based on ghost proximity
        evaluation += ghostWeight / nearestGhostDistance
    return evaluation
    # return currentGameState.getScore()

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
