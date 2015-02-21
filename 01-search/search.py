# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import sets

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def solution(node):
    #print "the goal node is", node
    
    direction = []
    tmpNode=node
    while tmpNode[3]!=0:
        direction.insert(0,tmpNode[2])
	tmpNode=tmpNode[1]
    #print "direction is",direction
    return direction


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    start=problem.getStartState()
    startNode=(start,None,'',0)
    nodeStack=util.Stack()
    
    explored=sets.Set()
    explored.add(startNode[0])

    for element in problem.getSuccessors(problem.getStartState()):
        pushNode = (element[0],startNode,element[1],startNode[3]+element[2])
	nodeStack.push(pushNode)

    while not nodeStack.isEmpty():
	curNode=nodeStack.pop()
        if(not (curNode[0] in explored)):
		explored.add(curNode[0])
		if(problem.isGoalState(curNode[0])):
                        #print "goal state is",curNode[0]
			return solution(curNode)
                else:
    			for element in problem.getSuccessors(curNode[0]):
				nodeStack.push((element[0],curNode,element[1],curNode[3]+element[2]))
	


    return []
    "***util.raiseNotDefined()***"

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    start=problem.getStartState()
    startNode=(start,None,'',0)
    nodeQueue=util.Queue()
    
    explored=sets.Set()
    explored.add(startNode[0])

    for element in problem.getSuccessors(problem.getStartState()):
        pushNode = (element[0],startNode,element[1],startNode[3]+element[2])
	nodeQueue.push(pushNode)

    while not nodeQueue.isEmpty():
	curNode=nodeQueue.pop()
        if(not (curNode[0] in explored)):
	        #print "not explored"
		explored.add(curNode[0])
		if(problem.isGoalState(curNode[0])):
                        #print "goal state is",curNode[0]
			return solution(curNode)
                else:
    			for element in problem.getSuccessors(curNode[0]):
				nodeQueue.push((element[0],curNode,element[1],curNode[3]+element[2]))
	


    return []
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    start=problem.getStartState()
    startNode=(start,None,'',0)
    nodeQueue=util.PriorityQueue()
    
    explored=sets.Set()
    explored.add(startNode[0])

    for element in problem.getSuccessors(problem.getStartState()):
        pushNode = (element[0],startNode,element[1],startNode[3]+element[2])
	nodeQueue.push(pushNode,startNode[3]+element[2])

    while not nodeQueue.isEmpty():
	curNode=nodeQueue.pop()
        if(not (curNode[0] in explored)):
		explored.add(curNode[0])
		if(problem.isGoalState(curNode[0])):
                        #print "goal state is",curNode[0]
			return solution(curNode)
                else:
    			for element in problem.getSuccessors(curNode[0]):
				nodeQueue.push((element[0],curNode,element[1],curNode[3]+element[2]),curNode[3]+element[2])
	


    return []
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def generateFunction(problem,heuristic):
    return lambda (node): node[3]+heuristic(node[0],problem)

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    #print "begin search"
    start=problem.getStartState()
    startNode=(start,None,'',0)
    nodeQueue=util.PriorityQueueWithFunction(generateFunction(problem, heuristic))
    
    explored=sets.Set()
    explored.add(startNode[0])

    for element in problem.getSuccessors(problem.getStartState()):
        pushNode = (element[0],startNode,element[1],startNode[3]+element[2]) 
	nodeQueue.push(pushNode)

    while not nodeQueue.isEmpty():
	curNode=nodeQueue.pop()
        if(not (curNode[0] in explored)):
		explored.add(curNode[0])
		if(problem.isGoalState(curNode[0])):
                        #print "is a goal state"
			return solution(curNode)
                else:
    			for element in problem.getSuccessors(curNode[0]):
				nodeQueue.push((element[0],curNode,element[1],curNode[3]+element[2]))
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
