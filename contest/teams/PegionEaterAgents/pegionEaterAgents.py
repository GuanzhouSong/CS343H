# baselineAgents.py
# -----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
from captureAgents import AgentFactory
import distanceCalculator
import random, time, util
from game import Directions,Actions
import keyboardAgents
import game
from util import nearestPoint

#############
# FACTORIES #
#############

NUM_KEYBOARD_AGENTS = 0
class PegionEaterAgents(AgentFactory):
  "Returns one keyboard agent and offensive reflex agents"

  def __init__(self, isRed, first='offense', second='defense', rest='offense'):
    AgentFactory.__init__(self, isRed)
    self.agents = [first, second]
    self.rest = rest

  def getAgent(self, index):
    if len(self.agents) > 0:
      return self.choose(self.agents.pop(0), index)
    else:
      return self.choose(self.rest, index)

  def choose(self, agentStr, index):
    print "agentStr:",agentStr
    if agentStr == 'keys':
      global NUM_KEYBOARD_AGENTS
      NUM_KEYBOARD_AGENTS += 1
      if NUM_KEYBOARD_AGENTS == 1:
        return keyboardAgents.KeyboardAgent(index)
      elif NUM_KEYBOARD_AGENTS == 2:
        return keyboardAgents.KeyboardAgent2(index)
      else:
        raise Exception('Max of two keyboard agents supported')
    elif agentStr == 'offense':
      return AttackReflexAgent(index)
    elif agentStr == 'defense':
      return InferenceDefenseAgent(index)
    #elif agentStr =='router':
   #   return RoutingAgent(index)
    else:
      raise Exception("No staff agent identified by " + agentStr)

class AllOffenseAgents(AgentFactory):
  "Returns one keyboard agent and offensive reflex agents"

  def __init__(self, **args):
    AgentFactory.__init__(self, **args)

  def getAgent(self, index):
    return OffensiveReflexAgent(index)

class OffenseDefenseAgents(AgentFactory):
  "Returns one keyboard agent and offensive reflex agents"

  def __init__(self, **args):
    AgentFactory.__init__(self, **args)
    self.offense = False

  def getAgent(self, index):
    self.offense = not self.offense
    if self.offense:
      return OffensiveReflexAgent(index)
    else:
      return DefensiveReflexAgent(index)

##########
# Agents #
##########

class InferenceCaptureAgent(CaptureAgent):
  
  def __init__(self,index,timeForComputing=.1):
    CaptureAgent.__init__(self,index,timeForComputing)
    self.beliefDistributions=util.Counter()

  def registerInitialState(self,gameState):
    CaptureAgent.registerInitialState(self,gameState)
    self.setLegalPositions(gameState)
    self.initialDistributions(gameState)
    
  def setLegalPositions(self,gameState):
    walls=gameState.getWalls()
    positions=[]
    for x in range(walls.width):
        for y in range(walls.height):
	    if not walls[x][y]:
		positions.append((x,y))
    self.legalPositions=positions

  def initialDistributions(self,gameState):
    for opponentIndex in self.getOpponents(gameState):
	self.initialDistribution(gameState,opponentIndex)

  def initialDistribution(self,gameState,opponent):
    allPossible=util.Counter()
    #isPacman=gameState.getAgentState(opponent).isPacman
    #isRed=gameState.isOnRedTeam(opponent)
    threshold=gameState.getWalls().width/2
    #for position in self.legalPositions:
#	x=position[0]
#	if (isRed and isPacman and x>threshold) or \
#	 (isRed and (not isPacman) and x<=threshold) or \
#	 ((not isRed) and isPacman and x<=threshold) or \
#	 ((not isRed) and (not isPacman) and x>threshold):
#		allPossible[position]+=1
    for position in self.legalPositions:
	if (gameState.isOnRedTeam(opponent) and position[0]<=threshold) or \
	    (not gameState.isOnRedTeam(opponent) and position[0]>threshold): 
            allPossible[position]+=1
    allPossible.normalize()
    self.beliefDistributions[opponent]=allPossible

  def reInitialDistribution(self,threshold,opponent,isRed,isPacman):
    allPossible=util.Counter()
    for position in self.legalPositions:
	x=position[0]
	if (isRed and isPacman and x>threshold) or \
	 (isRed and (not isPacman) and x<=threshold) or \
	 ((not isRed) and isPacman and x<=threshold) or \
	 ((not isRed) and (not isPacman) and x>threshold):
		allPossible[position]+=1
    allPossible.normalize()
    self.beliefDistributions[opponent]=allPossible
    


  def observe(self,gameState):
    agentPosition=gameState.getAgentPosition(self.index)
    noisyDistances=gameState.getAgentDistances()
    threshold=gameState.getWalls().width/2
    opponents=self.getOpponents(gameState)

    for opponent in opponents:
	belief=self.beliefDistributions[opponent]
	if belief.totalCount()==0:
	    self.initialDistribution(gameState,opponent)
	    belief=self.beliefDistributions[opponent]
	allPossible=util.Counter()
	if gameState.getAgentState(opponent).configuration!=None:
	    allPossible[gameState.getAgentState(opponent).configuration.getPosition()]=1
	else:
	    isPacman=gameState.getAgentState(opponent).isPacman
            isRed=gameState.isOnRedTeam(opponent)
	    preGameState=self.getPreviousObservation()
	    preIsPacman=isPacman
	    if preGameState!=None:
	        preIsPacman=preGameState.getAgentState(opponent).isPacman
	    if isPacman!=preIsPacman:
	#	print "redo"
		self.reInitialDistribution(threshold,opponent,isRed,isPacman)
		belief=self.beliefDistributions[opponent]
	    for position in self.legalPositions:
		x=position[0]
		if (isRed and isPacman and x>threshold) or \
		 (isRed and (not isPacman) and x<=threshold) or \
		 ((not isRed) and isPacman and x<=threshold) or \
		 ((not isRed) and (not isPacman) and x>threshold):
		    distance=util.manhattanDistance(agentPosition,position)
		    allPossible[position]=belief[position]*gameState.getDistanceProb(distance,noisyDistances[opponent])
	allPossible.normalize()
	self.beliefDistributions[opponent]=allPossible
	

  
  def elapseTime(self,gameState):
    agentPosition=gameState.getAgentPosition(self.index)
    opponents=self.getOpponents(gameState)
    for opponent in opponents:
	belief=self.beliefDistributions[opponent]
	allPossible=util.Counter()
	for position in self.legalPositions:
	    neighborDist=util.Counter()
	    for neighborPos in self.getNeighborPositions(gameState,position):
	        neighborDist[neighborPos]=1
	    neighborDist.normalize()
	    for newPos in neighborDist:
		allPossible[newPos]+=belief[position]*neighborDist[newPos]
	allPossible.normalize()
	self.beliefDistributions[opponent]=allPossible
    
    #util.raiseNotDefined()
  
  def getNeighborPositions(self,gameState, (x,y)):
	walls = gameState.getWalls()
	positions=[(x,y)]
	if x-1>=0 and not walls[x-1][y]: 
	    positions.append((x-1,y))
	if x+1<walls.width and not walls[x+1][y]:
	    positions.append((x+1,y))
	if y-1>=0 and not walls[x][y-1]:
	    positions.append((x,y-1))
	if y+1<walls.height and not walls[x][y+1]:
	    positions.append((x,y+1))
	
	return positions
	

  def chooseAction(self,gameState):
    util.raiseNotDefined()

 
  def getMostPossiblePosition(self,opponent):
    return self.beliefDistributions[opponent].argMax()

  def getClosestPacman(self,gameState):
    agentPosition=gameState.getAgentPosition(self.index)
    hasPacman=False
    closestPacman=None
    minDistance=float('+inf')

    for opponent in self.getOpponents(gameState):
        agentIsPacman=gameState.getAgentState(opponent).isPacman
#	print "opponent",opponent,"is pacman",agentIsPacman
	attackerPos=gameState.getAgentPosition(opponent)
	if attackerPos==None:
	    attackerPos=self.getMostPossiblePosition(opponent)
	attackerDistance=self.getMazeDistance(agentPosition,attackerPos)
	if not hasPacman and agentIsPacman:
	    minDistance=attackerDistance
	    closestPacman=opponent
	    hasPacman=True
	else:
	    if (hasPacman and agentIsPacman) or (not hasPacman and not agentIsPacman):
		if attackerDistance<minDistance:
		    minDistance=attackerDistance
		    closestPacman=opponent
 #   print "closest pacman is:",closestPacman
    return closestPacman

  def getEatingTargets(self,gameState):
    list=[]
    quote='''
    for opponent in self.getOpponents(gameState):
	opponentPosition=gameState.getAgentPosition(opponent)
	if opponentPosition==None:
	    opponentPosition=self.getMostPossiblePosition(opponent)
	#print opponentPosition
  	x=opponentPosition[0]
	for i in range(0,len(list)):
	    (x1,agent)=list[i]
	    if (x<x1 and self.red) or (x>x1 and not self.red):
		list.insert(i,(x,opponent))
	    elif i==len(list)-1:
		list.append((x,opponent))
	if len(list)==0:
	    list.append((x,opponent))
    targets=[]
    for x,target in list:
	targets.append(target)
    return targets
    '''
    width=gameState.getWalls().width
    threshold=width/2
    for opponent in self.getOpponents(gameState):
	opponentPosition=gameState.getAgentPosition(opponent)
	if opponentPosition==None:
	    opponentPosition=self.getMostPossiblePosition(opponent)
        x=opponentPosition[0]
	if (x<=threshold and self.red) or (x>threshold and not self.red):
	    list.append(opponent)
    return list


class InferenceDefenseAgent(InferenceCaptureAgent):
  
  def chooseAction(self,gameState):
    observedState=self.getCurrentObservation()
    self.observe(observedState)
    self.elapseTime(observedState)


    actions=gameState.getLegalActions(self.index)
    agentPosition=gameState.getAgentPosition(self.index)
    bestAction=Directions.STOP
    actions.remove(Directions.STOP)

    if gameState.getAgentState(self.index).scaredTimer>0:
	closestAttacker=self.getClosestPacman(gameState)
	attackerPosition=gameState.getAgentPosition(closestAttacker)
	if attackerPosition==None:
	    attackerPosition=self.getMostPossiblePosition(closestAttacker)
	maxDistance=float('-inf')
	for action in actions:
	    successor=gameState.generateSuccessor(self.index,action)
	    newPos=successor.getAgentPosition(self.index)
	    newDistance=self.getMazeDistance(attackerPosition,newPos)
	    if newDistance>maxDistance and ((not successor.getAgentState(self.index).isPacman)  or successor.getAngentState(closestAttacker).isPacman):
		maxDistance=newDistance
		bestAction=action
    else:
	attackerPosition=None
	target=None
	targets=self.getEatingTargets(gameState)
	if len(targets)==0:
	    target=self.getClosestPacman(gameState)
	elif len(targets)==1:
	    target=targets[0]
	elif len(targets)==2:
	    distance=util.Counter()
	    for tmpTarget in targets:
	        tempPosition=gameState.getAgentPosition(tmpTarget)
	        if tempPosition==None:
	            tempPosition=self.getMostPossiblePosition(tmpTarget)
		distance[tmpTarget]=-(self.getMazeDistance(tempPosition,gameState.getAgentPosition(self.index)))
	    target=distance.argMax()

#	if not self.red:
#	    print "START1"
#	    print targets
#	    print target
#	    print "END1"
	attackerPosition=gameState.getAgentPosition(target)
	if attackerPosition==None:
	    attackerPosition=self.getMostPossiblePosition(target)
#	    if not self.red:
#		print "START2"
#		print "RED attacker approximate position:", attackerPosition
#		print "END2"
#	if not self.red:
#	    print "target is", target
#	    print "RED ATTACKER POSITION",attackerPosition
#	    print "NOISY DISTANCES:",gameState.getAgentDistances()
#	    print "probability is",self.beliefDistributions[target][attackerPosition]
	minDistance=float('+inf')
	for action in actions:
	    #print "ACTION"
	    successor=gameState.generateSuccessor(self.index,action)
	    newPos=successor.getAgentPosition(self.index)
	    newDistance=self.getMazeDistance(attackerPosition,newPos)
	    #newDistance=util.manhattanDistance(attackerPosition,newPos)
	    #print attackerPosition,newPos
	    threshold=gameState.getWalls().width/2
	    if newDistance<minDistance and (not successor.getAgentState(self.index).isPacman):
	#	print action
	#	print minDistance,newDistance
		minDistance=newDistance
	#	print minDistance
		bestAction=action
    
    return bestAction
	

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)
    #print gameState.getAgentDistances(),self.index
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}


class AttackReflexAgent(ReflexCaptureAgent):
  def getFeatures(self,gameState,action):
    foods=self.getFood(gameState).asList()
    walls = gameState.getWalls()
    nextState=self.getSuccessor(gameState,action)
    isPacman=nextState.getAgentState(self.index).isPacman
    
    attackBase=(self.index-self.index%2)/2
    buddies=[]
    opponents=self.getOpponents(gameState)
    for i in range(gameState.getNumAgents()):
	if not (i in opponents):
	    buddies.append(i)
    targets=[]
    preys=[]
    for opponent in opponents:
	agentState=gameState.getAgentState(opponent)
	if (not agentState.isPacman) and agentState.getPosition()!=None:
	    targets.append(opponent)
	elif agentState.isPacman and agentState.getPosition!=None:
	    preys.append(opponent)

    features=util.Counter()

    if action==Directions.STOP:
	features['stop-action']=1.0

    x,y=gameState.getAgentState(self.index).getPosition()
    dx,dy = Actions.directionToVector(action)
    xp,yp=int(x+dx),int(y+dy)

    for target in targets:
	if (xp,yp)==gameState.getAgentState(target).getPosition():
	    if gameState.getAgentState(target).scaredTimer>0:
		features['eat-target']+=1.0
		features['eat-food']+=2.0
	    else:
		features['danger-ghosts']=3.0
		features['no-danger-ghosts']=0
	elif gameState.getAgentState(target).getPosition()!=None:
            if (xp,yp) in Actions.getLegalNeighbors(gameState.getAgentState(target).getPosition(),walls):
	        if gameState.getAgentState(target).scaredTimer>0:
		    features['no-danger-ghosts']+=3.0
	        elif isPacman:
		    features['danger-ghosts']+=2.0
		    features['no-danger-ghosts']=0
	    elif self.getMazeDistance((xp,yp),gameState.getAgentState(target).getPosition())<=3:
	        if gameState.getAgentState(target).scaredTimer>0:
		    features['no-danger-ghosts']+=3.0
	        elif isPacman:
		    features['danger-ghosts']+=1.0
		    features['no-danger-ghosts']=0
	
    if gameState.getAgentState(self.index).scaredTimer==0:
	for prey in preys:
            if gameState.getAgentState(prey).getPosition()!=None:
	        if (xp,yp)==gameState.getAgentState(prey).getPosition():
	            features['eat-invador']=1
	        elif (xp,yp) in Actions.getLegalNeighbors(gameState.getAgentState(prey).getPosition(),walls):
		    features['next-to-invador']+=5.0
    for capPositions in gameState.getCapsules():
	if capPositions==(xp,yp) and isPacman:
	    features['capsules']=1.0
    if features['danger-ghosts']==0:
	if (xp,yp) in foods:
	    features['eat-food']=1.0
        myFood=[]
	for food in foods:
	    x,y=food
	    if(y>attackBase*walls.height/3 and y<(attackBase+1)*walls.height/3):
	         myFood.append(food)  
	
	if len(myFood)==0:
  	    myFood=foods
	myMinDist = min([self.getMazeDistance((xp, yp), food) for food in myFood])
	if myMinDist is not None:
	    features["closest-food"] = float(myMinDist) / (walls.width * walls.height) 	
   
    features.divideAll(1.0)
    return features   
    
    
	
    #util.raiseNotDefined()

  def getWeights(self,gameState,action):
    return {'eat-invader':5, 'next-to-invader':1,  'closest-food': -1, 'capsules': 10.0, 'danger-ghosts': -50.0, 'eat-target': 2.0, 'no-danger-ghosts': 0.1, 'stop-action': -5, 'eat-food': 1}
    #util.raiseNotDefined()



#######################################
########  default code below   ########
#######################################

class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1}

class DefensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}


