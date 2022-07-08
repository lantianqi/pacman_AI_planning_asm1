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
    node = (problem.getStartState(), '', [])
    state = problem.getStartState()
    counter = 0
    while not problem.isGoalState(state):
        queue = util.Queue()
        queue.push(node)
        # print("the queue "+str(queue.list))
        state, action, path = node
        visited = set()
        h = heuristic(state,problem)
        while not queue.isEmpty():
            lnode = queue.pop()
            lstate, laction, lpath = lnode
            if lstate not in visited :
                # print(len(visited))
                visited.add(lstate)
                if heuristic(lstate,problem) < h:
                    node = lnode
                    state = lstate
                    break
                succNodes = problem.getSuccessors(lstate)
                counter = counter +1
                for succNode in succNodes :
                    
                    succState, succAction, succCost = succNode
                    newstate = (succState, succAction, lpath + [(lstate, laction)])
                    queue.push(newstate)
    state, action, path = node
    path = path + [(state,action)]
    actions = [action[1] for action in path]
    # print(counter)
    del actions[0]
    return actions
    # util.raiseNotDefined()


        
def idaStarSearch(problem, heuristic=nullHeuristic):
    """
    Global search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second argument (heuristic).
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"
    startState = problem.getStartState()
    startNode = (startState, '',0, [])
    bound = heuristic(startState,problem)
    while True:
        print(f"bound: {bound}")
        min = 99999
        myStack = util.Stack()
        myStack.push(startNode)
        while not myStack.isEmpty() :
            node = myStack.pop()
            state, action, cost, path = node
            f = cost + heuristic(state,problem)
            if f < min and f > bound:
                min = f
            if problem.isGoalState(state):
                path = path + [(state, action)]
                actions = [action[1] for action in path]
                del actions[0]
                return actions
            if f <= bound:
                # print(state)
                succs = problem.getSuccessors(state)
                # succs .reverse()
                for succ in succs:
                    succState, succAction, succCost = succ
                    newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                    myStack.push(newNode)
        bound = min  
    util.raiseNotDefined()
    
def idaStarSearch2(problem, heuristic=nullHeuristic):
    """COMP90054 your solution to part 2 here """
    startState = problem.getStartState()
    bound = heuristic(startState,problem)
    startNode = (startState, '', [])
    
    stack = [startNode]
    while True:
        print(f"bound: {bound}")
        t = idaHelper(stack,0,bound,problem,heuristic)
        if type(t) == int:
            if t == -1:
                return False
            bound = t
        else:
            return t
        
def idaHelper(stack,g,bound,problem,heuristic):
    node = stack[-1]
    state,action,path = node
    f = g + heuristic(state,problem)
    if f > bound:
        return f
    if problem.isGoalState(state):
        actions = [action[1] for action in path]      
        return actions
    min = 999999
    for succ in problem.getSuccessors(state):
        succState,succAction,cost = succ
        succNode = (succState,succAction,path+[(succState,succAction)])
        t = idaHelper(path+[succNode],g+cost,bound,problem,heuristic)
        if not type(t) == int: return t 
        if t < min: min =t
    return min





# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ida = idaStarSearch
ida2 = idaStarSearch2
ehc = enforcedHillClimbing
