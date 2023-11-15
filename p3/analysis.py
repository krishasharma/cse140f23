"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    [Enter a description of what you did here.]
    """

    # play around with discount and noise to make it go from
    answerDiscount = 0.9
    answerNoise = 0.000002

    return answerDiscount, answerNoise

def question3a():
    """
    [Enter a description of what you did here.]

    prefer the close exit (+1), risking the cliff (-10)
    """

    # lower discount to prefer immediate rewards
    answerDiscount = 0.1
    answerNoise = 0.2
    # higher negative living reward to discourage lingering
    answerLivingReward = -10.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    [Enter a description of what you did here.]
    
    prefer the close exit (+1), but avoiding the cliff (-10)
    """

    # lower discount to prefer immediate rewards
    answerDiscount = 0.1
    answerNoise = 0.2
    # slightly higher negative living reward to encourage avioding the cliff
    answerLivingReward = -1.0

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    [Enter a description of what you did here.]

    prefer the distant exit (+10), risking the cliff (-10)
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    # higher negative living reward to discourage lingering
    answerLivingReward = -10.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    [Enter a description of what you did here.]

    prefer the distant exit (+10), avoiding the cliff (-10)
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    # slightly higher negative living reward to encourage avioding the cliff
    # -1.0 ???
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    [Enter a description of what you did here.]

    avoid both exits (also avoiding the cliff)
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0
    # return NOT_POSSIBLE
    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]

    train a completely random q-learner with the default learning rate
    on the noiseless BridgeGrid for 50 episodes
    and observe whether it finds the optimal policy.
    """

    answerEpsilon = 0.3
    answerLearningRate = 0.5

    return answerEpsilon, answerLearningRate

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
