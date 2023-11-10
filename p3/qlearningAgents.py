from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection
from pacai.util.probability import flipCoin
import random

class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index, **kwargs):
        """
        initialize the Q-Learning agent.

        args:
            index: the agent index
            alpha: the learning rate (default is 0.5)
            epsilon: the exploration rate (default is 0.5)
            gamma: the discount factor (default is 0.9)
            numTraining: the number of training episodes (default is 100)
            **kwargs: additional keyword arguments
        """

        # inherits from reinforcment agent
        super().__init__(index, **kwargs)
        # q values are stored in the dictionary, which maps state-action pairs
        self.qValues = {}  # dictionary to store Q-values

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """
        # need to keep track of q values 
        """
        get the Q-Value for a state-action pair

        args:
            state: The current state
            action: The action taken in the current state

        returns:
            The Q-value for the (state, action) pair
        """

        # retruves the q value for any given state 
        return self.qValues.get((state, action), 0.0)
        return 0.0

    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """
        """
        return the value of the best action in a state

        args:
            state: the current state

        returns:
            the value of the best action in the given state
        """

        legalActions = self.getLegalActions(state)
        if not legalActions:
            return 0.0
        # choose the action with the maximum Q-value
        return max(self.getQValue(state, action) for action in legalActions)
        return 0.0

    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """
        """
        return the best action in a state

        args:
            state: the current state

        returns:
            the best action in the given state
        """

        legalActions = self.getLegalActions(state)
        if not legalActions:
            return None
        # choose the action with the maximum Q-value
        bestActions = [action for action in legalActions if self.getQValue(state, action) == self.getValue(state)]
        return random.choice(bestActions)
        return None
    
    def getAction(self, state):
        """
        compute the action to take in the current state

        returns:
            the action to take
        """

        legalActions = self.getLegalActions(state)
        if not legalActions:
            return None
        # with probability epsilon, choose a random action
        if flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            # otherwise, choose the action with the maximum Q-value
            return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        """
        update the Q-value for a state-action pair

        args:
            state: the current state
            action: the action taken in the current state
            nextState: the next state
            reward: the immediate reward
        """

        # calculate the Q-value update using the Q-learning formula
        sample = reward + self.getDiscountRate() * self.getValue(nextState)
        self.qValues[(state, action)] = (1 - self.getAlpha()) * self.getQValue(state, action) + self.getAlpha() * sample


class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index,
            extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # You might want to initialize weights here.

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            # *** Your Code Here ***
            raise NotImplementedError()
