import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    self.features = trainingData[0].keys() # this could be useful for your code later...
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"
    #print trainingData[0]
    self.priorDis=util.Counter()
    self.bestCondition=util.Counter()
    conditionDisByK=util.Counter()
    for label in trainingLabels:
	self.priorDis[label]+=1
    self.priorDis.normalize()
    for k in kgrid:
	numerator=util.Counter()
	denominator=util.Counter()
	condDis=util.Counter()
	for i in range(0,len(trainingData)):
	    trainingCounter=trainingData[i]
            label=trainingLabels[i]
	    for pixel in trainingCounter:
		value=trainingCounter[pixel]
		numerator[(pixel,label,value)]+=1
		denominator[(pixel,label)]+=1
	for pixel,label in denominator:
	    condDis[(pixel,label,0)]=float(numerator[(pixel,label,0)]+k)/float(denominator[(pixel,label)]+k)
	    condDis[(pixel,label,1)]=float(numerator[(pixel,label,1)]+k)/float(denominator[(pixel,label)]+k)
	conditionDisByK[k]=condDis
    bestK=kgrid[0]
    bestNumCorrect=-1
    for k in kgrid:
	numCorrect=0
	self.bestCondition=conditionDisByK[k]
	gusses=self.classify(validationData)
	for i in range(len(gusses)):
	    if gusses[i]==validationLabels[i]:
		numCorrect+=1
	if numCorrect>=bestNumCorrect:
	    if numCorrect==bestNumCorrect:
		bestK=min(k,bestK)
	    else:
		bestK=k
		bestNumCorrect=numCorrect
    self.bestCondition=conditionDisByK[bestK]	
    #print self.priorDis
    #util.raiseNotDefined()
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    """
    logJoint = util.Counter()
    
    "*** YOUR CODE HERE ***"
    logProb=util.Counter()
    for label in self.legalLabels:
	logProb[label]=math.log(self.priorDis[label])
	#print logProb[label]
	for pixel in datum:
	    value=datum[pixel]
	    #if self.testCondition[(pixel,label,value)]==0.0:
	    #    print pixel,label,value
	    logProb[label]+=math.log(self.bestCondition[(pixel,label,value)])
    return logProb 
    #util.raiseNotDefined()
    
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    """
    featuresOdds = []
        
    "*** YOUR CODE HERE ***"
    featureVal=util.Counter()
    for pixel in self.features:
	featureVal[pixel]=float(self.bestCondition[(pixel,label1,1)])/float(self.bestCondition[(pixel,label2,1)])
    features=featureVal.sortedKeys()
    for i in range(0,100):
	featuresOdds.append(features[i])
    
    #util.raiseNotDefined()

    return featuresOdds
    

    
      
