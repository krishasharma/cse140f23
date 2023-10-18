from lib2to3.main import StdoutRefactoringTool
from pacai.util.stack import Stack 
from pacai.util.queue import Queue


"""
------------------------------------------------------------------------
Krisha Sharma 
CRUZ ID: krvsharm
CSE 140 Prof. Leilani Gilpin 
PA1
search.py
------------------------------------------------------------------------
CREDIT: Please note, many of the online resources linked by Prof. Gilpin 
were refrenced throughout this programming assignment. The below code 
also makes use of starter code provided by Prof. Gilpin. Pusedocode for
this assignment was also found on the lecture slides and textbook. 
------------------------------------------------------------------------
"""

"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

# note to self: most of the search algorithms are the same, in that if you implement DFS first 
# most of the other algorithms should be relatively straightforward
# algorithms to implement checklist: 
    # Depth First Search (DFS)
    # Breadth First Search (BFS)
    # Uniform Cost Search (UCS)
    # A star search 

#for stack import Stack
#import pacai.util.stack



# define function for DEPTH FIRST SEARCH 
# use graoh search version of DFS; meaning that it aviods repeated states and redudant paths; CITE: Textbook pg.86 
# "searches the deepest nodes of the tree first"

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    '''
    notes/ pusedocode DFS: 
    initialize data structures 
        create a stack to maintain the search frontier. 
        create a set to track visited states. 
        create either a dictionary or another data structure to store the parent of each state to reconstruct the path later 
    push initial state to the stack 
        push the start state which in this case is pacmans current position to the stack
    implement DFS algorithm
        while the stack is not empty: 
            pop the top state from the stack, going to be current state. 
            if the current state is the goal state, a solution was found, reconstruct the path from the start state to the goal state using the parent dictionary and return it. 
            otherwise, expand the current state by generating its valid successor states (in this case legal moves). check for valid directions (no moves through walls) and ignore the states that have already been visited. 
            for each vaild successor state, mark it as visited, set its parent as the current state, and push it onto the stack. 
    termination of algo. 
        if the stack becomes empty and a solution has not been found, it means that no path exists
        from the start to the goal state. 
        in this case return failure or an empty list to indicate that no vaild path was found. 
    '''
    
    stack = Stack() # the stack for DFS 
    stack.push((problem.startingState(), [])) # utilize stack with LIFO policy 
    visited = set() # create a set to keep track of visited states

    while not stack.isEmpty(): 
        state, path = stack.pop() # pop the most recently pushed item from the stack
        problem._numExpanded += 1 # getExpandedCount returns self._numExpanded, increments the expanded node count 
        if problem.isGoal(state): # if the starting state is the goal 
            return path # DFS found a solution 
        if state not in visited: # if the stating state is not the goal or been visited
            visited.add(state) # mark as visited 
            successors = problem.successorStates(state) # find a successor state
            print(successors)
            for next_state, action, cost in successors: 
                if next_state not in visited: 
                    new_path = path + [action]
                    print("new path: ", new_path, " DONE.")
                    print("next state: ", next_state, " DONE.")
                    print("state, path: ", next_state, new_path)
                    stack.push((next_state, new_path))
                    
    #print("Start: %s" % (str(problem.startingState())))
    #print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    #print("Start's successors: %s" % (problem.successorStates(problem.startingState())))

    #return None # no solution was found; right now it is returning NONE we need it to return a path
    return path
    raise NotImplementedError()

    


# define function for BREATH FIRST SEARCH 
# BFS visits the root node and then recursively looks at all the children on that level 
# "searches the shallowest nodes first"
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    queue = Queue()  # the queue for BFS
    queue.push((problem.startingState(), []))  # initialize the queue with the starting state along w/ an empty list of actions 
    visited = set()  # create a set to keep track of visited states

    while not queue.isEmpty():
        state, actions = queue.pop()  # get the next state and its corresponding actions
        problem._numExpanded += 1  # increment the expanded node count
        if problem.isGoal(state):
            return actions  # found a solution when the goal state is reached
        if state not in visited:
            visited.add(state)  # mark the state as visited
            successors = problem.successorStates(state)
            for next_state, action, cost in successors:
                if next_state not in visited:
                    new_actions = actions + [action]  # create a new list of actions with the current action
                    queue.push((next_state, new_actions))  # add the next state and its actions to the queue

    return None  # no solution was found
    raise NotImplementedError()


import heapq
def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    '''
    pusedocode/ notes on UCS: CITE Textbook pg. 84
    '''

    priority_queue = []  # using a priority queue for UCS
    heapq.heappush(priority_queue, (0, (problem.startingState(), [])))  # initialize the queue with the starting state and an empty list of actions
    visited = {}  # create a dict. to keep track of visited states and their priorities

    while priority_queue:
        priority, (state, actions) = heapq.heappop(priority_queue)  # get the next state and the corresponding actions with the lowest priority
        if problem.isGoal(state):
            return actions  # found a solution when the goal state is reached
        if state in visited:
            continue  # skip if the state has been visited with a lower priority
        visited[state] = priority  # mark the state as visited
        successors = problem.successorStates(state)
        for next_state, action, cost in successors:
            if next_state not in visited:
                new_actions = actions + [action]  # create a new list of actions with the current action
                new_priority = priority + cost  # calculate the new priority
                heapq.heappush(priority_queue, (new_priority, (next_state, new_actions)))  # add the next state and its actions to the priority queue

    return None  # no solution was found
    raise NotImplementedError()

import heapq
def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    priority_queue = []  # use a priority queue for a star 
    heapq.heappush(priority_queue, (0 + heuristic(problem.startingState(), problem), (problem.startingState(), [])))  # initialize the queue with the starting state and an empty list of actions
    visited = {}  # create a dict to keep track of visited states and their priorities

    while priority_queue:
        priority, (state, actions) = heapq.heappop(priority_queue)  # get the next state and its corresponding actions with the lowest priority
        #problem._numExpanded += 1  # increment the expanded node count
        if problem.isGoal(state):
            return actions  # found a solution when the goal state is reached
        if state in visited and priority >= visited[state]:
            continue  # skip if the state has been visited with an equal or lower priority
        visited[state] = priority  # mark the state as visited
        successors = problem.successorStates(state)
        for next_state, action, cost in successors:
            new_actions = actions + [action]  # create a new list of actions with the current action
            new_priority = problem.actionsCost(new_actions) + heuristic(next_state, problem)  # calculate the new priority using the heuristic
            heapq.heappush(priority_queue, (new_priority, (next_state, new_actions)))  # add the next state and its actions to the priority queue

    return None  # no solution was found
    raise NotImplementedError()
