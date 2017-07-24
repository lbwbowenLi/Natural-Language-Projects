from __future__ import division
import sys
import getopt
import os
import math
import operator
import re
import nltk


class NaiveBayes:
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
    """NaiveBayes initialization"""
    self.negWords = []
    self.posWords = []
    self.numFolds = 10
    self.dicPos = {}    #this dictionary is used for store training result
    self.dicNeg = {}
  #############################################################################
  # TODO TODO TODO TODO TODO
  # Implement the Multinomial Naive Bayes classifier and the Naive Bayes Classifier with
  # Boolean (Binarized) features.
  # If the BOOLEAN_NB flag is true, your methods must implement Boolean (Binarized)
  # Naive Bayes (that relies on feature presence/absence) instead of the usual algorithm
  # that relies on feature counts.
  #
  #
  # If any one of the FILTER_STOP_WORDS and BOOLEAN_NB flags is on, the
  # other one is meant to be off.

  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    wordNum = len(self.dicPos) - 2
    for b in self.dicNeg.keys():
      if b not in self.dicPos:
        wordNum += 1
    pPos = math.log(self.dicPos['posDocNum'] / (self.dicNeg['negDocNum'] + self.dicPos['posDocNum']), 2)
    pNeg = math.log(self.dicNeg['negDocNum'] / (self.dicNeg['negDocNum'] + self.dicPos['posDocNum']), 2)
    phrases = self.extractPhrase(words)
    for tempWord in phrases:
      word = tempWord[0] + ' ' + tempWord[1]
      if word in self.dicPos:
        pPos = pPos + math.log((self.dicPos[word] + 1)/(self.dicPos['docLength'] + wordNum + 1), 2)
      else:
        pPos = pPos + math.log(1/(self.dicPos['docLength'] + wordNum + 1), 2)
      if word in self.dicNeg:
        pNeg = pNeg + math.log((self.dicNeg[word] + 1) / (self.dicNeg['docLength'] + wordNum + 1), 2)
      else:
        pNeg = pNeg + math.log(1 / (self.dicNeg['docLength'] + wordNum + 1), 2)
    #print pPos, pNeg
    if(pPos >= pNeg):
      #print 'pos'
      return 'pos'
    else:
      #print 'neg'
      return 'neg'

  def rate(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    wordNum = len(self.dicPos) - 2
    for b in self.dicNeg.keys():
      if b not in self.dicPos:
        wordNum += 1
    pPos = math.log(self.dicPos['posDocNum'] / (self.dicNeg['negDocNum'] + self.dicPos['posDocNum']), 2)+0.2
    pNeg = math.log(self.dicNeg['negDocNum'] / (self.dicNeg['negDocNum'] + self.dicPos['posDocNum']), 2)
    #print(type(words))
    text = nltk.word_tokenize(str(words))
    phrases = nltk.pos_tag(text)
    for tempWord in phrases:
      word = tempWord[0] + ' ' + tempWord[1]
      if word in self.dicPos:
        pPos = pPos + math.log((self.dicPos[word] + 1)/(self.dicPos['docLength'] + wordNum + 1), 2)
      else:
        pPos = pPos + math.log(1/(self.dicPos['docLength'] + wordNum + 1))
      if word in self.dicNeg:
        pNeg = pNeg + math.log((self.dicNeg[word] + 1) / (self.dicNeg['docLength'] + wordNum + 1), 2)
      else:
        pNeg = pNeg + math.log(1 / (self.dicNeg['docLength'] + wordNum + 1), 2)
    print (pPos, pNeg)
    rating = pPos - pNeg
    print(rating)
    if rating<=250:
        print("*")
    if rating<=350 and rating>250:
        print("**")
    if rating <=450 and rating>350:
        print("***")
    if rating<=600 and rating >450:
        print("****")
    if rating>600:
        print("*****")

  def addExample(self, klass, phrase):
    """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier 
     * in the NaiveBayes class.
     * Returns nothing
    """
    # Write code here
    words = self.extractPhrase(phrase)
    docLength = len(words)
    if klass == 'pos':
      if 'docLength' in self.dicPos:
        self.dicPos['docLength'] += docLength
      else:
        self.dicPos['docLength'] = docLength
      if 'posDocNum' in self.dicPos:
        self.dicPos['posDocNum'] += 1
      else:
        self.dicPos['posDocNum'] = 1
      for word in words:
        tempPhrase = word[0] + ' ' + word[1]
        if tempPhrase in self.dicPos:
          self.dicPos[tempPhrase] += 1
        else:
          self.dicPos[tempPhrase] = 1
    else:
      if 'docLength' in self.dicNeg:
        self.dicNeg['docLength'] += docLength
      else:
        self.dicNeg['docLength'] = docLength
      if 'negDocNum' in self.dicNeg:
        self.dicNeg['negDocNum'] += 1
      else:
        self.dicNeg['negDocNum'] = 1
      for word in words:
        tempPhrase = word[0] + ' ' + word[1]
        if tempPhrase in self.dicNeg:
          self.dicNeg[tempPhrase] += 1
        else:
          self.dicNeg[tempPhrase] = 1
    pass


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
      result = self.segmentWords(line.strip('\n'))
      for word in result:
        a = word.split('_')
        contents += [(a[0].lower(), a[1])]
    f.close()
    return contents


  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()


  def extractPhrase(self, wordTags):
    n = len(wordTags)-1
    wordTag = wordTags + [(' ',' ')]
    phrases = []
    for i in range(0, n):
      word = [wordTag[i], wordTag[i+1], wordTag[i+2]]
      if(self.rightPhrase(word)):
        phrases += [(word[0][0], word[1][0])]
    return phrases

  def rightPhrase(self, word):
   tag = [word[0][1],word[1][1],word[2][1]]
   i = 0
   jj = 'JJ'
   nn = '(NN\b)|(NNS)'
   rb = '(RB\b)|(RBR)|(RBS)'
   vb = '(VB\b)|(VBD)|(VBN)|(VBG)'
   if(re.match(jj, tag[0]) and re.match(nn, tag[1])):
     i = 1
   elif(re.match(rb, tag[0]) and re.match(jj, tag[1]) and not re.match(nn, tag[2]), 2):
     i = 1
   elif(re.match(jj, tag[0]) and re.match(jj, tag[1]) and not re.match(nn, tag[2]), 2):
     i = 1
   elif(re.match(nn, tag[0]) and re.match(jj, tag[1]) and not re.match(nn, tag[2]), 2):
     i = 1
   elif (re.match(nn, tag[0]) and re.match(vb, tag[1])):
     i = 1
   elif (re.match(nn, tag[0]) and re.match(rb, tag[1]) and re.match(vb, tag[2]), 2):
     i = 1
   elif(re.match(rb, tag[0]) and re.match(vb, tag[1]), 2):
     i = 1
   return i



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

def test10Fold(args):
  nb = NaiveBayes()
  splits = nb.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = NaiveBayes()
    accuracy = 0.0
    for example in split.train:
      words = example.words
      classifier.addExample(example.klass, words)

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


def test1Fold(args):
  trainDir = args[0]
  nb = NaiveBayes()
  posTrainFileNames = os.listdir('%s/pos/' % trainDir)
  negTrainFileNames = os.listdir('%s/neg/' % trainDir)
  split = nb.TrainSplit()
  for fileName in posTrainFileNames:
    example = nb.Example()
    example.words = nb.readFile('%s/pos/%s' % (trainDir, fileName))
    example.klass = 'pos'
    split.train.append(example)
  for fileName in negTrainFileNames:
    example = nb.Example()
    example.words = nb.readFile('%s/neg/%s' % (trainDir, fileName))
    example.klass = 'neg'
    split.train.append(example)
  for example in split.train:
    words = example.words
    nb.addExample(example.klass, words)
  while(1):
    input1 = input("Please input your review or input 'esc' to quit:").encode("utf-8")
    if(input1 == 'esc'):
      break
    else:
      nb.rate(input1)



def main(args):
  print ("Input '-m' to input your review, '-a' to show the result of reserved text")
  mode = input("Please choose mode:")
  if(mode=='-a'):
    test10Fold(args)
  elif(mode=='-m'):
    test1Fold(args)
  else:
    print ("Input Error!")

if __name__ == "__main__":
    main(sys.argv[1:])
