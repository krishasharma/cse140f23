from pacai.agents.learning.value import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        '''
        args:
            index: the agent index
            mdp: the Markov Decision Process
            discountRate: the discount rate for future rewards (default is 0.9)
            iters: the number of iterations for value iteration (default is 100)
            **kwargs: additional keyword arguments???
        '''
        # initialize super class
        super().__init__(index, **kwargs)
        # initialize instance variables
        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.
        # going to have a dict with the previous values of the states

        # Compute the values here.
        # Perform value iteration
        for _ in range(iters):
            newValues = {}
            # iterate through all states in the MDP
            for state in mdp.getStates():
                # can possibly check if it is a terminal state somewhere else in the code
                # check if the state is not terminal
                # skip terminal states bc their values are normally 0
                if not mdp.isTerminal(state):
                    # get list of all possible actions in the current state
                    possibleActions = mdp.getPossibleActions(state)
                    # check if there are legal actions in the current state
                    if not possibleActions:
                        # if there are no legal actions in the current state, skip to next state
                        continue
                    # check if there are legal actions?? 
                    # initialize max q value to large negative number
                    # the worst case???
                    maxQValue = float('-inf')
                    # choose the action with the highest q-value
                    # iterate through all possible actions in the current state
                    for action in possibleActions:
                        # calculate the q value for each action
                        qValue = self.getQValue(state, action)
                        # update max q value if the calc q value is greater than the current maximum
                        maxQValue = max(maxQValue, qValue)
                    # update the value for the current state
                    newValues[state] = maxQValue
            # update the values
            # AFTER ONE ITERATION KAIA???!!!
            self.values = newValues
        # raise NotImplementedError()

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)
    
    def getQValue(self, state, action):
        """
        Return the q-value of the (state, action) pair.
        """
        '''
        args:
            state: the current state
            action: the action to take in the current state
        returns:
            the q-value of the (state, action) pair
        '''

        qValue = 0
        # get the possinle next states and their transition probabilities
        transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        # iterate through each possible next state and its probability
        for nextState, prob in transitionStatesAndProbs:
            # get the immediate reward for the transition
            reward = self.mdp.getReward(state, action, nextState)
            # calculate the discounted value of the next state
            discountedValue = self.discountRate * self.getValue(nextState)
            # Update the q-value based on:
            # the transition probability, immediate reward, and discounted future value
            qValue += prob * (reward + discountedValue)
        return qValue
    
    def getPolicy(self, state):
        """
        Return the best action according to computed values.
        """
        '''
        args:
            state: the current state for which to determine the best action
        returns:
            the best action to take in the given state
        '''

        # check if the state is terminal
        if self.mdp.isTerminal(state):
            # no action in terminal state
            return None
        # get the possible actions
        possibleActions = self.mdp.getPossibleActions(state)
        # handle no legal actions
        if not possibleActions:
            # there are no legal actions avaliable
            return None
        # initialie best action
        bestAction = None
        # initialize max q value to large negative number
        # the worst case???
        maxQValue = float('-inf')
        # choose the action with the highest q value
        # iterate through each possible action
        for action in possibleActions:
            # calculate q value for each action
            qValue = self.getQValue(state, action)
            # if q value for the current action is greater than
            # the max q value
            if qValue > maxQValue:
                # update max value
                maxQValue = qValue
                # set best action to the current action
                bestAction = action
        # return the best acton after iterating through all possible actions
        return bestAction

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)
