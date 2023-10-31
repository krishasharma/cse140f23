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

    def myLegalActions(self, state, agentid):
        # copyactions = state.getLegalActions(agentid)
        # list of [east, stop, east] for ex.
        actions = state.getLegalActions(agentid)
        if actions == Directions.STOP or 'Stop':
            actions.remove('Stop')
            return actions

    def getAction(self, state):
        # starts the search and selects best action for pac-man
        # here state is the game state??? CHECK THIS KAI
        # totalDepth = self.getTreeDepth()
        # get the legal actions for Pac-Man (agent 0).
        legalActions = self.myLegalActions(state, 0)
        # initialize the best action and best value.
        bestAction = Directions.STOP
        value = float('-inf')
        # iterate through legal actions and find the one with the maximum value.
        for action in legalActions:
            # print("Actions", legalActions)
            successorState = state.generateSuccessor(0, action)
            # start with ghost 1 at depth 0.
            # create a new state
            newvalue = max(value, self.maxValue(successorState, self.getTreeDepth()))
            if newvalue > value:
                # bestValue = value
                # change the action score if better
                value = newvalue
                bestAction = action
            # print("best action: ", bestAction)
            return bestAction

    def maxValue(self, state, depth):
        # had ghost index included
        # going from bottom up, hence decrement the depth
        # base case #1: tree depth reached
        # base case #2: if you win
        # base case #3: if you loose
        # prev. if depth >= self.depth
        if depth <= 0 or state.isWin() or state.isLose():
            # if we've reached the specified depth or a terminal state (win or lose)
            # return the state's evaluation.
            return self.getEvaluationFunction()(state)
        depth = depth - 1
        legalActions = self.myLegalActions(state, 0)
        # initialize the best value to negative infinity.
        value = float('-inf')
        for action in legalActions:
            successorState = state.generateSuccessor(0, action)
            # call minValue for the first ghost.
            # had ghost index-- hardcoded to 1
            value = max(value, self.minValue(successorState, depth, 1))
            # update the best value with the maximum value.
            # value = max(value)
        return value

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
        value = float('inf')
        for action in legalActions:
            if ghostIndex == (state.getNumAgents() - 1):
                # if this is the last ghost, call maxValue for pacman
                successorState = state.generateSuccessor(ghostIndex, action)
                value = min(value, self.maxValue(successorState, depth - 1))
            else:
                # call minValue for the next ghost.
                successorState = state.generateSuccessor(ghostIndex, action)
                value = min(value, self.minValue(successorState, depth, ghostIndex + 1))
                # (ghostIndex + 1) % state.getNumAgents()
            # update the best value with the minimum value.
        return value

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
        # initialize the best action and best value
        bestAction = None
        bestValue = float('-inf')
        for action in legalActions:
            # generate the successor state for each action
            successorState = state.generateSuccessor(0, action)
            # start the expectimax search for ghosts
            value = self.expectimax(successorState, self.getTreeDepth(), 1)
            # if the value for this action is better, update the best action and value
            if value > bestValue:
                bestValue = value
                bestAction = action
        return bestAction

    def expectimax(self, state, depth, agentIndex):
        # base case: if the depth limit is reached or the game is over,
        if depth == 0 or state.isWin() or state.isLose():
            # return the evaluation
            return self.getEvaluationFunction()(state)
        # pacman's turn
        if agentIndex == 0:
            legalActions = state.getLegalActions(agentIndex)
            bestValue = float('-inf')
            for action in legalActions:
                successorState = state.generateSuccessor(agentIndex, action)
                # continue the expectimax search with the next agent (ghost)
                value = self.expectimax(successorState, depth, agentIndex + 1)
                # update the best value for pacman (max value)
                bestValue = max(bestValue, value)
            return bestValue
        # ghosts' turn (expectation)
        else:
            legalActions = state.getLegalActions(agentIndex)
            totalValue = 0
            for action in legalActions:
                successorState = state.generateSuccessor(agentIndex, action)
                # continue the expectimax search with the next agent
                value = self.expectimax(successorState, depth, (agentIndex + 1) %
                                        state.getNumAgents())
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
    Improved evaluation function for Pac-Man without considering power pills.

    DESCRIPTION: This evaluation function focuses on other important factors to make Pac-Man
    perform better. It considers the following:
    1. Current score: Pac-Man's current score reflects his progress, so we want to maximize it.
    2. Remaining food: The number of remaining food dots is a crucial factor. We want to
       prioritize eating remaining food.
    3. Capsules: Eating capsules can make Pac-Man fearless, so we consider them in the evaluation.
    4. Ghosts: We want to avoid ghosts as much as possible. The distance to the nearest ghost is
       inversely proportional to the evaluation.

    We use a weighted sum of these factors to evaluate the current state, but we return
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
