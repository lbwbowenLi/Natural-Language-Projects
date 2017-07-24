import sys
import getopt
import os
import math
import operator

class Perceptron:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """Perceptron initialization"""
    #in case you found removing stop words helps.
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    self.negativeWords = ['no', 'not', 'Not', 'No', 'didn\'t', 'Didn\'t', 'don\'t', 'Don\'t', 'wasn\'t', 'weren\'t']
    self.count=[0,0,0,0,0,0,0,0,0,0]
    self.weights = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    self.max_iterations =0
    self.posText = {}
    self.negText = {}
    self.text = {}
    self.numPoswords = 0.0
    self.numNegwords = 0.0
    self.numPosReviews = 0.0
    self.numNegReviews = 0.0

  #############################################################################
  # TODO TODO TODO TODO TODO 
  # Implement the Perceptron classifier with
  # the best set of features you found through your experiments with Naive Bayes.

  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
"""
    score=0
    for word in words:
      if word in self.negativeWords:
        score+=-1
    if score<0:
      return 'neg'
    else:
      return 'pos'


  def addExample(self, klass, words):
    """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier 
     * in the Perceptron class.
     * Returns nothing
"""
    for word in words:
      i=0
      while (i<10):
        if(word==self.negativeWords[i]):
          self.count[i]+=1
        i+=1
    j=0
    while(j<10):
      if klass=='neg':
        if self.weights[j]>0:
          self.weights[j]-=self.count[j]
      elif klass=='pos':
        if self.weights[j]<0:
          self.weights[j]+=1
      j+=1



    # Write code here

    pass
  
  def train(self, split, iterations):
      """
      * TODO 
      * iterates through data examples
      * TODO 
      * use weight averages instead of final iteration weights
      """
      count=0
      while (count<iterations):
        for example in split.train:
          word=example.words
          self.addExample(example.klass,word)
        count+=1
      #for example in split.train:
        #words = example.words
        #self.addExample(example.klass, words)
      

  # END TODO (Modify code beyond here with caution)
  #############################################################################
  
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  
  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  
  def trainSplit(self, trainDir,iter):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits
  
  
  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
    return filtered

def test10Fold(args):
  pt = Perceptron()
  
  iterations = int(args[1])
  splits = pt.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = Perceptron()
    accuracy = 0.0
    classifier.train(split,iterations)
  
    for example in split.test:
      words = example.words
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0

    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print ('[INFO]\tFold %d Accuracy: %f' % (fold, accuracy))
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print ('[INFO]\tAccuracy: %f' % avgAccuracy)
    
    
def classifyDir(trainDir, testDir,iter):
  classifier = Perceptron()
  trainSplit = classifier.trainSplit(trainDir)
  iterations = int(iter)
  classifier.train(trainSplit,iterations)
  testSplit = classifier.trainSplit(testDir)
  #testFile = classifier.readFile(testFilePath)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print ('[INFO]\tAccuracy: %f' % accuracy)
    
def main():
  (options, args) = getopt.getopt(sys.argv[1:], '')
  
  if len(args) == 3:
    classifyDir(args[0], args[1], args[2])
  elif len(args) == 2:
    test10Fold(args)

if __name__ == "__main__":
    main()
