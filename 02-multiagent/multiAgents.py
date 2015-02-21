# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPositions=successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print "newPos",newPos
	#print "newFood",newFood
	#print "newGhoseStates",newGhostStates[0]
        
        gridWidth=newFood.width
	gridHeight=newFood.height
        
	foodDistance=gridWidth+gridHeight
	for foodPos in newFood.asList():
	  foodDistance=min(util.manhattanDistance(newPos,foodPos),foodDistance)

	ghostDistance=gridWidth+gridHeight
	for ghostPos in newGhostPositions:
	  ghostDistance=min(util.manhattanDistance(newPos,ghostPos),ghostDistance)
        scaredDistance=gridWidth+gridHeight

        evalValue=0
        if(ghostDistance<3):
	   evalValue-=1000
        evalValue+=1.0/foodDistance
        if(newFood[newPos[0]][newPos[1]]):
	   evalValue+=50
	evalValue+=successorGameState.getScore()  
	#print "evalValue",evalValue
        return evalValue

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
	self.numAgents=0
   
    def terminalTest(self,state,curDepth):
	#print "current Depth",curDepth
        #print "terminal Depth",self.depth
	return curDepth==self.numAgents*self.depth or state.isWin() or state.isLose()

    def utility(self,state):
	return self.evaluationFunction(state)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def miniMax(self,state,curIndex,curDepth):
        #print "curDepth",curDepth
	if(curIndex==self.numAgents):
		curIndex=0
	if(self.terminalTest(state,curDepth)):
		return self.utility(state)
	elif curIndex==0:
		return self.maxValue(state,curIndex,curDepth)
	else:
		return self.minValue(state,curIndex,curDepth)

   
    def maxValue(self,state,curIndex,curDepth):
	v=float('-inf')
        actions=state.getLegalActions(curIndex)
	for action in actions:
		resultState=state.generateSuccessor(curIndex,action)
		returnVal=self.miniMax(resultState,curIndex+1,curDepth+1)
    		#print "max",v
		#print "returnVal",returnVal
		v=max(v,returnVal)
		#print "max1",v
	
	return v

    def minValue(self,state,curIndex,curDepth):
	v=float('+inf')
        actions=state.getLegalActions(curIndex)
	for action in actions:
		resultState=state.generateSuccessor(curIndex,action)		
		returnVal=self.miniMax(resultState,curIndex+1,curDepth+1)
		#print "min",v
		#print "returnVal",returnVal
		v=min(v,returnVal)
	#print "min1",v
	return v
	
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #print "depth",self.depth
        #print "index",self.index
	self.numAgents=gameState.getNumAgents()
  	actions=gameState.getLegalActions(self.index)
        #if(actions.count('Stop')!=0):
	#	actions.remove('Stop')
        #print "actions",actions
        curDepth=0
	curIndex=self.index
	actionDic={}	
	for action in actions:
          resultState=gameState.generateSuccessor(curIndex,action)
	  val=self.miniMax(resultState,curIndex+1,curDepth+1)
	  actionDic[val]=action
	#print "minimax",max(actionDic)
	returnAction=actionDic[max(actionDic)]
	#print "return action and score",returnAction,max(actionDic) 
	return returnAction
        #util.raiseNotDefined()

class ActionObject():
    def __init__(self,value,action):
        self.action = action
        self.value = value
    
    def __repr__(self):
        return self.action + ": " + str(self.value)
    
    def __cmp__(self,other):
        if self.value == other.value:
            return 0
        elif self.value > other.value:
            return 1
        else:
            return -1

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphaBetaMiniMax(self,state,curIndex,curDepth,action,alpha,beta):
	if(curIndex==self.numAgents):
		curIndex=0
	if(self.terminalTest(state,curDepth)):
		returnObject=ActionObject(self.utility(state),action)
		return returnObject
	elif curIndex==0:
		return self.maxValue(state,curIndex,curDepth,alpha,beta)
	else:
		return self.minValue(state,curIndex,curDepth,alpha,beta)

   
    def maxValue(self,state,curIndex,curDepth,alpha,beta):
	v=ActionObject(float('-inf'),Directions.STOP)
        actions=state.getLegalActions(curIndex)
	for action in actions:
		resultState=state.generateSuccessor(curIndex,action)
		returnVal=self.alphaBetaMiniMax(resultState,curIndex+1,curDepth+1,action,alpha,beta)
		returnVal.action=action
		v=max(v,returnVal)
		if v.value>beta:
		  return v
		alpha=max(v.value,alpha)
	return v

    def minValue(self,state,curIndex,curDepth,alpha,beta):
	v=ActionObject(float('+inf'),Directions.STOP)
        actions=state.getLegalActions(curIndex)
	for action in actions:
		resultState=state.generateSuccessor(curIndex,action)		
		returnVal=self.alphaBetaMiniMax(resultState,curIndex+1,curDepth+1,action,alpha,beta)
		returnVal.action=action
		v=min(v,returnVal)
		if v.value<alpha:
		  return v
		beta=min(v.value,beta)
	return v
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
	#print "depth",self.depth
        #print "index",self.index
	self.numAgents=gameState.getNumAgents()
  	actions=gameState.getLegalActions(self.index)
        #if(actions.count('Stop')!=0):
	#	actions.remove('Stop')
        #print "actions",actions
        curDepth=0
	curIndex=self.index	
 	alpha=float('-inf')
	beta=float('+inf')
	action = Directions.STOP
    	actionObject = self.alphaBetaMiniMax(gameState,curIndex,curDepth,action,alpha,beta)
    	return actionObject.action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def miniMax(self,state,curIndex,curDepth):
        #print "curDepth",curDepth
	if(curIndex==self.numAgents):
		curIndex=0
	if(self.terminalTest(state,curDepth)):
		return self.utility(state)
	elif curIndex==0:
		return self.maxValue(state,curIndex,curDepth)
	else:
		return self.exMinValue(state,curIndex,curDepth)

   
    def maxValue(self,state,curIndex,curDepth):
	v=float('-inf')
        actions=state.getLegalActions(curIndex)
	for action in actions:
		resultState=state.generateSuccessor(curIndex,action)
		returnVal=self.miniMax(resultState,curIndex+1,curDepth+1)
    		#print "max",v
		#print "returnVal",returnVal
		v=max(v,returnVal)
		#print "max1",v
	
	return v

    def exMinValue(self,state,curIndex,curDepth):
	v=0.0
        actions=state.getLegalActions(curIndex)
	size=float(len(actions))
	prob=1.0/size
	for action in actions:
		resultState=state.generateSuccessor(curIndex,action)		
		returnVal=self.miniMax(resultState,curIndex+1,curDepth+1)
		#print "min",v
		#print "returnVal",returnVal
		v+=returnVal*prob
	#print "min1",v
	return v

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        #print "depth",self.depth
        #print "index",self.index
	self.numAgents=gameState.getNumAgents()
  	actions=gameState.getLegalActions(self.index)
        #if(actions.count('Stop')!=0):
	#	actions.remove('Stop')
        #print "actions",actions
        curDepth=0
	curIndex=self.index
	actionDic={}	
	for action in actions:
          resultState=gameState.generateSuccessor(curIndex,action)
	  val=self.miniMax(resultState,curIndex+1,curDepth+1)
	  actionDic[val]=action
	#print "minimax",max(actionDic)
	returnAction=actionDic[max(actionDic)]
	#print "return action and score",returnAction,max(actionDic) 
	return returnAction

def betterEvaluationFunction(currentGameState):
    	"""
      	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      	evaluation function (question 5).

      	DESCRIPTION: <write something here so we know what you did>
    	"""
        "This evaluation function evaluates several factors: score, nearest food, food on current position, and"
	"ghost scared times. If the distance between any ghost and pacman is less than 2, the return value will"
	"decrease 1000 unless the minimum ghost panic time is greater than that distance. Also it will evaluate"
	"food distance and the evaluation value will increase 1.0 over nearest food distance. If current position"
	"has food, the evaluation value will increase 50. The evaluation value will then add up the score value"
    	"*** YOUR CODE HERE ***"
	score=currentGameState.getScore()
    
	newPos = currentGameState.getPacmanPosition()
	newFood = currentGameState.getFood()
	newGhostStates = currentGameState.getGhostStates()
	newGhostPositions=currentGameState.getGhostPositions()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #print "ScaredTimes",newScaredTimes
	gridWidth=float(newFood.width)
	gridHeight=float(newFood.height)
        
	foodDistance=gridWidth+gridHeight
	for foodPos in newFood.asList():
	  foodDistance=min(float(util.manhattanDistance(newPos,foodPos)),foodDistance)

	ghostDistance=gridWidth+gridHeight
	ghostIndex=1;
	index=0
	for ghostPos in newGhostPositions:
	  index+=1
	  tmpGhostDistance=ghostDistance
	  ghostDistance=min(float(util.manhattanDistance(newPos,ghostPos)),ghostDistance)
	  if(tmpGhostDistance!=ghostDistance):
		ghostIndex=index

        evalValue=0
        if(ghostDistance<2):
	   if(ghostDistance>min(newScaredTimes)):
	     evalValue-=1000.00
	   else:
	     evalValue+=100
        evalValue+=1.0/foodDistance
        if(newFood[newPos[0]][newPos[1]]):
	   evalValue+=50.00
	evalValue+=score  
	return evalValue

    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

