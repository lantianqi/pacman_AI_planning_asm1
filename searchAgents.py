# searchAgents.py
# ---------------
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


"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

from game import Directions
from game import Agent
from game import Actions
from game import Grid
from searchAgents_hints import cPH1, cPH2, cPH3
import util
import time
import search

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            next_x, next_y = int(x + dx), int(y + dy)
            if not self.walls[next_x][next_y]:
                nextState = (next_x, next_y)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0 # DO NOT CHANGE; Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   next_x, next_y = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[next_x][next_y]

            "*** YOUR CODE HERE ***"

        self._expanded += 1 # DO NOT CHANGE
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)

    "*** YOUR CODE HERE ***"
    return 0 # Default to trivial solution

class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            next_x, next_y = int(x + dx), int(y + dy)
            if not self.walls[next_x][next_y]:
                nextFood = state[1].copy()
                nextFood[next_x][next_y] = False
                successors.append( ( ((next_x, next_y), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    # return 0
    x, y = position
    food_list = foodGrid.asList()
    h = 0
    # goal aware
    if len(food_list) == 0:
        return h
    for food in food_list:
        h = max(mazeDistance(position, food, problem.startingGameState), h)

    return h
    # return 0

class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.food[x][y]

def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))


class CapsuleSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    pass


class CapsuleSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    startingGameState contains:
    getPacmanPosition() : a tuple (x,y) of integers specifying Pacman's position
    getFood()           : a Grid (see game.py) of either True or False, indicating food
    getWalls()          : a Grid (see game.py) of either True or False, indicating wall
    getCapsules()       : a list of position that contains a capsule
    """
    def __init__(self, startingGameState):
        self._expanded = 0 # DO NOT CHANGE

        "You might need to use the following variables"
        self.init_pos = startingGameState.getPacmanPosition()
        self.foodGrid = startingGameState.getFood()
        self.walls = startingGameState.getWalls()
        self.capsulesGrid = Grid(self.foodGrid.width,self.foodGrid.height)
        for x,y in startingGameState.getCapsules():
            self.capsulesGrid[x][y] = True

        # If you have anything else want to initialize
        "*** YOUR CODE HERE for Task 3 (optional) ***"
        self.costFn = lambda x: 1
        self.startingGameState = startingGameState
        self.currentGameState = startingGameState
        self.heuristicInfo = {}

    def getStartState(self):
        # You MUST implement this function to return the initial state
        "*** YOUR CODE HERE for Task 3 ***"
        return (self.init_pos, self.foodGrid.deepCopy(), self.capsulesGrid.deepCopy())

    def isGoalState(self, state):
        # You MUST implement this function to return True or False
        # to indicate whether the give state is one of the goal state or not
        "*** YOUR CODE HERE for Task 3 ***"
        pacman_pos, food_grid, capsules_grid = state
        # if food_grid.count() == 0:
        #     print("food count == 0")
        return food_grid.count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of ?."
        # You MUST implement this function to return a list of successors
        # A successor is in the format of (next_state, action, cost)
        successors = []
        self._expanded += 1 # DO NOT CHANGE

        "*** YOUR CODE HERE for Task 3 ***"
        pacman_pos, food_grid, capsules_grid = state
        x, y = pacman_pos

        # There are four actions might be available
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(direction)
            next_x, next_y = int(x + dx), int(y + dy)

            if not self.walls[next_x][next_y]:
                new_pacman_pos = (next_x, next_y)
                new_food_grid = food_grid.deepCopy()
                new_capsules_grid = capsules_grid.deepCopy()
                if food_grid[next_x][next_y]:
                    new_food_grid[next_x][next_y] = False
                cost = self.costFn(new_pacman_pos)
                if capsules_grid[next_x][next_y]:
                    new_capsules_grid[next_x][next_y] = False
                    cost = 0
                new_state = (new_pacman_pos, new_food_grid, new_capsules_grid)
                successors.append( ( new_state, direction, cost) )

        return successors


    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""

        # this function will return the cost only for display purpose when you run your own test.
        "*** YOUR CODE HERE for Task 3 (optional) ***"
        cost = 0
        x,y = self.init_pos
        capsule = self.capsulesGrid.copy()
        # print(actions)
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            elif capsule[x][y]:
                capsule[x][y]=False
            else: cost += 1
        return cost

# def capsuleProblemHeuristic(state, problem):
#     # return 0
#     if state in problem.heuristicInfo:
#         return problem.heuristicInfo[state]
#     pacman_pos, food_grid, capsules_grid = state
#     # print(state)
#     startingGameState = problem.startingGameState
#     # return food_grid.count()
#     max_dist = 0
#     for food in food_grid.asList():
#         # food_dist = mazeDistance(pacman_pos, food, startingGameState)
#         food_dist = mazeDistance3(pacman_pos, food, startingGameState, problem)
#         max_dist = max(food_dist, max_dist)

#     # print(max(max_dist, food_grid.count()))
#     problem.heuristicInfo[state] = max(max_dist, food_grid.count())
#     return max(max_dist, food_grid.count())


def capsuleProblemHeuristic(state, problem):
    """
    Your heuristic for the CapsuleSearchProblem goes here.
    """
    "*** YOUR CODE HERE for Task 3 ***"
    # pacman_pos, food_grid, capsules_grid = state

    # h = 0
    # # farthest_food = (999,999)
    # # path_to_farthest_food = []
    # path_to_farthest_food = []
    # for food in food_grid.asList():
    #     prob = PositionSearchProblem(problem.startingGameState, start=pacman_pos, goal=food, warn=False, visualize=False)
    #     actions = search.bfs(prob)
    #     # h += problem.getCostOfActions(actions)
    #     # h += len(actions)
    #     # h = max(h, len(actions))
    #     if len(actions) > h:
    #         h = len(actions)
    #         path_to_farthest_food = actions
    #         # path_to_farthest_food = actions
    #         # farthest_food = food

    # cells_on_path = [pacman_pos]
    # x, y = pacman_pos
    # for action in path_to_farthest_food:
    #     dx, dy = Actions.directionToVector(action)
    #     next_x, next_y = int(x+dx), int(y+dy)
    #     cells_on_path += [(next_x, next_y)]
    #     x, y = next_x, next_y

    # capsule_count = 0
    # for cell in cells_on_path:
    #     cell_x, cell_y = cell
    #     if capsules_grid[cell_x][cell_y]:
    #         capsule_count += 1

    # h -= capsule_count
    # return h
    # return cPH2(state, problem)
    if state in problem.heuristicInfo:
        return problem.heuristicInfo[state]
    else:
        h = cPH3(state, problem)
        problem.heuristicInfo[state] = h
    return h


class CapsuleAvoidSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    pass


class CapsuleAvoidSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    startingGameState contains:
    getPacmanPosition() : a tuple (x,y) of integers specifying Pacman's position
    getFood()           : a Grid (see game.py) of either True or False, indicating food
    getWalls()          : a Grid (see game.py) of either True or False, indicating wall
    getCapsules()       : a list of position that contains a capsule
    """
    def __init__(self, startingGameState):
        self._expanded = 0 # DO NOT CHANGE

        "You might need to use the following variables"
        self.init_pos = startingGameState.getPacmanPosition()
        self.foodGrid = startingGameState.getFood()
        self.walls = startingGameState.getWalls()
        self.capsulesGrid = Grid(self.foodGrid.width,self.foodGrid.height)
        for x,y in startingGameState.getCapsules():
            self.capsulesGrid[x][y] = True

        # If you have anything else want to initialize
        "*** YOUR CODE HERE for Task 4 (optional) ***"
        self.startingGameState = startingGameState

        def capsuleAvoidCostFn(pacman_pos, capsules_grid):
            x, y = pacman_pos
            if capsules_grid[x][y]:
                return 2
            return 1


        # self.costFn = capsuleAvoidCostFn
        self.costFn = lambda x : 1
        self.heuristicInfo = {}

    def getStartState(self):
        # You MUST implement this function to return the initial state
        "*** YOUR CODE HERE for Task 4 ***"
        return (self.init_pos, self.foodGrid.copy(), self.capsulesGrid.copy())

    def isGoalState(self, state):
        # You MUST implement this function to return True or False
        # to indicate whether the give state is one of the goal state or not
        "*** YOUR CODE HERE for Task 4 ***"
        pacman_pos, food_grid, capsules_grid = state
        return food_grid.count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of ?."
        # You MUST implement this function to return a list of successors
        # A successor is in the format of (next_state, action, cost)
        successors = []
        self._expanded += 1 # DO NOT CHANGE

        "*** YOUR CODE HERE for Task 4 ***"
        pacman_pos, food_grid, capsules_grid = state
        x, y = pacman_pos

        # There are four actions might be available
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(direction)
            next_x, next_y = int(x+dx), int(y+dy)

            if not self.walls[next_x][next_y]:
                new_pacman_pos = (next_x, next_y)
                new_food_grid = food_grid.deepCopy()
                new_capsules_grid = capsules_grid.deepCopy()
                if food_grid[next_x][next_y]:
                    new_food_grid[next_x][next_y] = False
                # cost = self.costFn(new_pacman_pos, new_capsules_grid)
                cost = self.costFn(new_pacman_pos)

                if capsules_grid[next_x][next_y]:
                    new_capsules_grid[next_x][next_y] = False
                    cost = 2
                new_state = (new_pacman_pos, new_food_grid, new_capsules_grid)
                successors.append( ( new_state, direction, cost) )

        return successors


    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""

        # this function will return the cost only for display purpose when you run your own test.
        "*** YOUR CODE HERE for Task 4 (optional) ***"
        cost = 0
        x, y = self.init_pos
        capsules = self.capsulesGrid.copy()

        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x+dx), int(y+dy)
            if self.walls[x][y]:
                return 999999
            elif capsules[x][y]:
                capsules[x][y] = False
                cost += 2
            else:
                cost += 1

        return cost


def capsuleAvoidProblemHeuristic(state, problem):
    # return 0
    if state in problem.heuristicInfo:
        return problem.heuristicInfo[state]
    pacman_pos, food_grid, capsules_grid = state
    # print(state)
    startingGameState = problem.startingGameState
    # return food_grid.count()
    max_dist = 0
    for food in food_grid.asList():
        # food_dist = mazeDistance(pacman_pos, food, startingGameState)
        food_dist = mazeDistance2(pacman_pos, food, startingGameState, problem)
        max_dist = max(food_dist, max_dist)

    # print(max(max_dist, food_grid.count()))
    problem.heuristicInfo[state] = max(max_dist, food_grid.count())
    return max(max_dist, food_grid.count())


def mazeDistance2(point1, point2, gameState, problem):
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    # prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    # prob = AnyFoodSearchProblem(gameState)
    prob = AvoidCapsulesPositionSearchProblem(gameState, costFn=avoidCapCostFn, start=point1, goal=point2, warn=False, visualize=False)
    actions = uniformCostCapAvoidSearch(prob)
    # print(actions)
    # print(prob.getCostOfActions(actions))
    return prob.getCostOfActions(actions)


def mazeDistance3(point1, point2, gameState, problem):
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    # prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    # prob = AnyFoodSearchProblem(gameState)
    prob = AvoidCapsulesPositionSearchProblem(gameState, costFn=encourageCapCostFn, start=point1, goal=point2, warn=False, visualize=False)
    actions = uniformCostCapAvoidSearch(prob)
    # actions = search.bfs(prob)
    # print(actions)
    # print(prob.getCostOfActions(actions))
    return prob.getCostOfActions(actions)


def uniformCostCapAvoidSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    """
    expansion check
    """
    pQueue = util.PriorityQueue()
    start_state = problem.getStartState()
    init_pos, capsules_grid = start_state
    x, y = init_pos
    # root_node has start_state, action_list [], and g_cost value 0
    root_node = (start_state, [], 0)
    # push root_node into pQueue, priority will be 0, which is the g_cost value
    pQueue.push(root_node, 0)
    expanded = set()

    while not pQueue.isEmpty():
        node = pQueue.pop()
        state, action_list, g_cost = node
        pacman_pos, capsules_grid = state
        if state not in expanded:
            # expand
            expanded.add(state)
            if problem.isGoalState(state):
                return action_list
            else:
                for succ in problem.getSuccessors(state):
                    new_state, new_action, step_cost = succ
                    new_node = (new_state, action_list + [new_action], g_cost + step_cost)
                    pQueue.push(new_node, g_cost + step_cost)


# def uniformCostCapAvoidSearch(problem):
#     """Search the node of least total cost first."""
#     "*** YOUR CODE HERE ***"
#     # util.raiseNotDefined()
#     """
#     expansion check
#     """
#     pQueue = util.PriorityQueue()
#     start_state = problem.getStartState()
#     init_pos, capsules_grid = start_state
#     x, y = init_pos
#     # root_node has start_state, action_list [], and g_cost value 0
#     root_node = (start_state, [], 0)
#     # push root_node into pQueue, priority will be 0, which is the g_cost value
#     pQueue.push(root_node, 0)
#     # expanded = set()
#     generated = set()
#     generated.add(start_state)

#     while not pQueue.isEmpty():
#         node = pQueue.pop()
#         state, action_list, g_cost = node
#         pacman_pos, capsules_grid = state
#         if problem.isGoalState(state):
#             return action_list
#         else:
#             for succ in problem.getSuccessors(state):
#                 new_state, new_action, step_cost = succ
#                 if not new_state in generated:
#                     new_node = (new_state, action_list + [new_action], g_cost + step_cost)
#                     pQueue.push(new_node, g_cost + step_cost)
#                     generated.add(new_state)


def encourageCapCostFn(pos, eat_capsule):
    x, y = pos
    if eat_capsule:
        return 0
    return 1

def avoidCapCostFn(pos, eat_capsule):
    x, y = pos
    if eat_capsule:
        return 2
    return 1

class AvoidCapsulesPositionSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to a given food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, costFn = avoidCapCostFn, goal=(1,1), start=None, warn=True, visualize=True):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference

        self.start = start
        self.goal = goal
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

        "You might need to use the following variables"
        self.walls = gameState.getWalls()
        self.capsulesGrid = Grid(self.walls.width,self.walls.height)
        for x,y in gameState.getCapsules():
            self.capsulesGrid[x][y] = True

        self.costFn = costFn
        # self.costFn = avoidCapCostFn
        self.heuristicInfo = {}
        self.warn = warn
        self.visualize = visualize


    def getStartState(self):
        # a state includes the current pacman_pos and the capsulesGrid before pacman enters that pos
        return (self.start, self.capsulesGrid)

    def isGoalState(self, state):
        pacman_pos, capsules_grid = state
        isGoal = pacman_pos == self.goal

        # # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        pacman_pos, capsules_grid = state

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = pacman_pos
            dx, dy = Actions.directionToVector(action)
            next_x, next_y = int(x + dx), int(y + dy)
            if not self.walls[next_x][next_y]:
                next_capsules_grid = capsules_grid.copy()
                eat_capsule = capsules_grid[next_x][next_y]
                if capsules_grid[next_x][next_y]:
                    next_capsules_grid[next_x][next_y] = False
                cost = self.costFn((next_x, next_y), eat_capsule)
                nextState = ((next_x, next_y), next_capsules_grid)
                # cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        # print(successors)
        return successors


    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""

        # this function will return the cost only for display purpose when you run your own test.
        "*** YOUR CODE HERE for Task 4 (optional) ***"
        cost = 0
        x, y = self.start
        capsules = self.capsulesGrid.copy()

        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x+dx), int(y+dy)
            if self.walls[x][y]:
                return 999999
            # elif capsules[x][y]:
            #     capsules[x][y] = False
            #     cost += 2
            # else:
            #     cost += 1
            else:
                eat_capsule = capsules[x][y]
                if capsules[x][y]:
                    capsules[x][y] = False
                next_state = ((x, y), capsules)
                cost += self.costFn(next_state, eat_capsule)
                
        return cost
