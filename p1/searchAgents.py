import logging
from pacai.core.actions import Actions
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent
from pacai.core.directions import Directions
from pacai.core.distance import manhattan, maze
from pacai.student import search
# from pacai.core.search import heuristic
# from pacai.core.distance import euclidean

"""
------------------------------------------------------------------------
Krisha Sharma
CRUZ ID: krvsharm
CSE 140 Prof. Leilani Gilpin
PA1
searchAgents.py
------------------------------------------------------------------------
CREDIT: Please note, many of the online resources linked by Prof. Gilpin
were refrenced throughout this programming assignment. The below code
also makes use of starter code provided by Prof. Gilpin. Pusedocode for
this assignment was also found on the lecture slides and textbook.
Credit is also given to TA's Batu, Fariha, Evan, Joshua, and Camden who
helped during
------------------------------------------------------------------------
"""
"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""


class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.
    You must select a suitable state space and successor function.
    See the `pacai.core.search.position.PositionSearchProblem` class for an example of
    a working SearchProblem.
    Additional methods to implement:
    `pacai.core.search.problem.SearchProblem.startingState`:
    Returns the start state (in your search space,
    NOT a `pacai.core.gamestate.AbstractGameState`).
    `pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.
    `pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    ```
        successors = []
        for action in Directions.CARDINAL:
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            if (not hitsWall):
                # Construct the successor.
        return successors
    ```
    """

    def __init__(self, startingGameState):
        super().__init__()
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))
        # *** Your Code Here ***

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """
        if (actions is None):
            return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
        return len(actions)
    
    '''
    pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.
    '''
    def isGoal(self, state):
        # point is current pos on map,
        point, corners = state
        # corners is list of remaining coord's
        # if current position is in corners list
        if point in self.corners:
            # if the corners list is empty
            if not corners:
                # return bool true
                return True
        # else return bool false
        return False
    '''
    pacai.core.search.problem.SearchProblem.startingState:
    Returns the start state (in your search space,
    NOT a pacai.core.gamestate.AbstractGameState).
    '''
    def startingState(self):
        # initialize self as the starting position,
        start = self.startingPosition
        # need to remember in order to return
        # put corners in a list to call later
        corners = list(self.corners)
        # return the starting postion and the corners list
        return start, corners
    
    '''
    pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    '''
    def successorStates(self, state):
        # empty sucessors list
        successors = []
        coordinate, corners = state
        for action in Directions.CARDINAL:
            # current position x y
            x, y = coordinate
            # directional position
            dx, dy = Actions.directionToVector(action)
            # sucessor coord
            nextx, nexty = int(x + dx), int(y + dy)
            # check to see if it hits wall
            hitsWall = self.walls[nextx][nexty]
            # coordinate = nextx, nexty
            # coord is x, y where pac curr is, corners, state is initalized
            # coordinate list
            newcoord = nextx, nexty
            # if it is not hitting a wall
            if (not hitsWall):
                # Construct the successor.
                # check if potential move in self.corners
                if newcoord in corners:
                    # construct child (state, action, cost)
                    # copy the corners list into duplicate list
                    newcorners = corners.copy()
                    # removing the coordinate list from new corners list
                    newcorners.remove(newcoord)
                    # creating a new state,
                    newstate = (newcoord, newcorners)
                    # state takes in corners and coord, do accordingly
                    # construct the child using, newstate, action, and cost
                    child = (newstate, action, 1)
                    # append the child to the list of successors
                    successors.append(child)
                    # print("new:", "%s") # error testing
                # still append the coord to sucessors list
                else:
                    # still create the new state
                    newstate = (newcoord, corners)
                    # still construct the child, its still a successor
                    child = (newstate, action, 1)
                    # append the successor to successor list
                    successors.append(child)
        # iterate the node count
        self._numExpanded += 1
        return successors

def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.
    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)
    """
    '''
    puedocode/ notes: CITE: BATU 10/19
    maze distance is the best method to find the distnace, its the one that actually does
    but maze is more costly than euclidean or manhattan
    use state which has coord and corners, coord being current pos
    use manhattan or euclidean to calculate the distance
    they arent going to be accurate enough but it gives u a good estimate
    find the min
    '''
    # Useful information.
    # corners = problem.corners
    # These are the corner coordinates
    # walls = problem.walls
    # These are the walls of the maze, as a Grid.
    # *** Your Code Here ***
    # are the walls of the maze, in grid
    # the current state
    # did not have function def for getWalls()
    def getWalls():
        walls = problem.walls
        return walls
    # point problem to getWalls CITE: Camden group tutor
    problem.getWalls = getWalls
    
    current_position, unvisited_corners = state
    # if there are no unvisited corners,
    if not unvisited_corners:
        # we have already reached the goal state
        return 0
    # initialize a dict
    distances = {}
    # use to store distances from the current position to unvisited corners
    # while the corners list is not empty? alt way??
    for corner in unvisited_corners:
        # calculate the manhattan distance
        distance = manhattan(current_position, corner)
        # manhattan from the current position to each unvisited corner
        distances[corner] = distance
        # print(max(distance))
    # return the maximum distance
    # return max(distances)
    # it's a lower bound on the shortest path
    # return heuristic.null(state, problem)  # Default to trivial solution
    return maze(state[0], max(distances, key=distances.get), problem)

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.
    This heuristic must be consistent to ensure correctness.
    First, try to come up with an admissible heuristic;
    almost all admissible heuristics will be consistent as well.
    If using A* ever finds a solution that is worse than what uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!
    On the other hand, inadmissible or inconsistent heuristics may find optimal solutions,
    so be careful.
    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a
    `pacai.core.grid.Grid` of either True or False.
    You can call `foodGrid.asList()` to get a list of food coordinates instead.
    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, `problem.walls` gives you a Grid of where the walls are.
    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use.
    For example, if you only want to count the walls once and store that value, try:
    ```
    problem.heuristicInfo['wallCount'] = problem.walls.count()
    ```
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount'].
    """
    # *** Your Code Here ***
    position, foodGrid = state
    # if there is no food left, we are already at the goal state
    if not foodGrid.asList():
        return 0
    # initialize a dict to store distances
    distances = {}
    # stores distances from the current position to uneaten food pellets
    # so that we can access the coord when looking at the manhattan distances
    for food in foodGrid.asList():
        # calculate the manhattan distance
        distance = manhattan(position, food)
        # max distance from the current position to each uneaten food pellet
        # using dict
        distances[food] = distance
    # call maze on position and poition your trying to get to game state
    return maze(state[0], max(distances, key=distances.get), problem.startingGameState)
    # return max(distances)
    # return the maximum distance, as it's a lower bound on the shortest path
    # return heuristic.null(state, problem)
    # default to the null heuristic

class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0
        currentState = state
        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))
                currentState = currentState.generateSuccessor(0, action)
        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """
        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        problem = AnyFoodSearchProblem(gameState)
        return search.breadthFirstSearch(problem)
        '''
        startState = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)
        # initialize data structure for BFS
        visited = set()
        queue = Queue()
        # add the start state to the queue with an empty path
        queue.put((startState, []))
        # while the queue exists
        while queue:
            currstate, actions = queue.get()
            # if the current state is a food dot
            if food[currstate[0]][currstate[1]]:
                # return the path
                return actions
            if currstate in visited:
                continue
            visited.add(currstate)
            # generate successor states and add them to the queue
            for action in problem.successorStates(currstate):
                # unpack the state, _ as placehonder for cost
                successorstate, actiontosuccessor, _ = action
                if successorstate not in visited:
                    if successorstate not in walls[successorstate[0]][successorstate[1]]:
                        queue.put((successorstate, actions + [actiontosuccessor]))
        # if no path is found
        # return an empty list
        return []
        '''
        raise NotImplementedError()


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.
    This search problem is just like the PositionSearchProblem,
    but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.
    The class definition above, `AnyFoodSearchProblem(PositionSearchProblem)`,
    inherits the methods of `pacai.core.search.position.PositionSearchProblem`.
    You can use this search problem to help you fill in
    the `ClosestDotSearchAgent.findPathToClosestDot` method.
    Additional methods to implement:
    `pacai.core.search.position.PositionSearchProblem.isGoal`:
    The state is Pacman's position.
    Fill this in with a goal test that will complete the problem definition.
    """

    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)
        # Store the food for later reference.
        self.food = gameState.getFood()

    def isGoal(self, state):
        return state in self.food.asList()


class ApproximateSearchAgent(BaseAgent):
    """
    Implement your contest entry here.
    Additional methods to implement:
    `pacai.agents.base.BaseAgent.getAction`:
    Get a `pacai.bin.pacman.PacmanGameState`
    and return a `pacai.core.directions.Directions`.
    `pacai.agents.base.BaseAgent.registerInitialState`:
    This method is called before any moves are made.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
