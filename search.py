# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from fileinput import close
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    myQ = util.Queue()
    startNode = (startState,[])
    myQ.push(startNode)
    generated = set()
    generated.add(startState)
    while not myQ.isEmpty():
        node = myQ.pop()
        state, actionList = node
        if problem.isGoalState(state):
            return actionList
        else:
            for successor in problem.getSuccessors(state):
                nextState, action, _ = successor
                if not nextState in generated:
                    nextNode = (nextState,actionList+[action])
                    generated.add(nextState)
                    myQ.push(nextNode)


    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Please DO NOT change the following code, we will use it to 
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    startNode = (startState, '',0, [])
    myPQ.push(startNode,heuristic(startState,problem))
    visited = set()
    best_g = dict()
    while not myPQ.isEmpty():
        node = myPQ.pop()
        state, action, cost, path = node
        if (not state in visited) or cost < best_g.get(state):
            visited.add(state)
            best_g[state]=cost
            if problem.isGoalState(state):
                path = path + [(state, action)]
                actions = [action[1] for action in path]
                del actions[0]
                return actions
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [(node, action)])
                myPQ.push(newNode,heuristic(succState,problem)+cost+succCost)
    util.raiseNotDefined()


def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """
    Local search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second argument (heuristic).
    """
    "*** YOUR CODE HERE FOR TASK 1 ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    node_0 = (problem.getStartState(), [])

    while True:
        state_0, action_list_0 = node_0
        if problem.isGoalState(state_0):
            # if state_0 is goal state, return action_list_0
            return action_list_0
        else:
            # state_0 is not goal state, improve to find new node/state with strictly smaller h-value (bfs)
            queue = util.Queue()
            queue.push(node_0)
            close_set = set()
            while not queue.isEmpty():
                node = queue.pop()
                state, action_list = node
                if state not in close_set:
                    close_set.add(state)
                    if heuristic(state, problem) < heuristic(state_0, problem):
                        node_0 = node
                        break
                    for succ in problem.getSuccessors(state):
                        new_state, new_action, _step_cost = succ
                        new_node = (new_state, action_list+[new_action])
                        queue.push(new_node)


def idaStarSearch(problem, heuristic=nullHeuristic):
    """
    this is the version without cycle check 
    (not checking if a node is in close_set)
    more nodes will be expanded
    the grader is looking for this solution
    """

    """
    Global search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second argument (heuristic).
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"
    start_state = problem.getStartState()
    # root_node has start_state, action_list [], and g_cost 0
    root_node = (start_state, [], 0)
    bound = 0 + heuristic(start_state, problem)

    while True:
        # do a dfs with depth limit = bound
        min = float('inf')
        stack = util.Stack()
        stack.push(root_node)
        close_set = set()
        while not stack.isEmpty():
            node = stack.pop()
            state, action_list, g_cost = node
            close_set.add(state)
            f = g_cost + heuristic(state, problem)
            if f < min and f > bound:
                min = f
            if problem.isGoalState(state):
                return action_list
            elif f <= bound:
                for succ in problem.getSuccessors(state):
                    new_state, new_action, step_cost = succ
                    # if new_state not in close_set:
                    new_node = (new_state, action_list+[new_action], g_cost+step_cost)
                    stack.push(new_node)
        bound = min


def idaStarNoDupSearch(problem, heuristic=nullHeuristic):
    """
    this is the version with cycle check
    so only expand the nodes not in close_set
    """

    """
    Global search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second argument (heuristic).
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"
    start_state = problem.getStartState()
    # root_node has start_state, action_list [], and g_cost 0
    root_node = (start_state, [], 0)
    bound = 0 + heuristic(start_state, problem)


    while True:
        # do a dfs with depth limit = bound
        min = float('inf')
        stack = util.Stack()
        stack.push(root_node)
        close_set = set()
        while not stack.isEmpty():
            node = stack.pop()
            state, action_list, g_cost = node
            close_set.add(state)
            f = g_cost + heuristic(state, problem)
            if f < min and f > bound:
                min = f
            if problem.isGoalState(state):
                return action_list
            elif f <= bound:
                for succ in problem.getSuccessors(state):
                    new_state, new_action, step_cost = succ
                    if new_state not in close_set:
                        new_node = (new_state, action_list+[new_action], g_cost+step_cost)
                        stack.push(new_node)
        bound = min



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ida = idaStarSearch
ehc = enforcedHillClimbing

ida2 = idaStarNoDupSearch