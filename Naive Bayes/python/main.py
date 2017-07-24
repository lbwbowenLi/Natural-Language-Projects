from __future__ import division
import sys
import getopt
import os
import math
import operator
import numpy as np
import nltk
import re
from nltk.tokenize import word_tokenize 



# use a part-of-speech tagger to identify phrases in the in- put text that contain adjectives or adverbs (Brill, 1994)   nltk.pos_tag
# 

class Senti:
 

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
    self.numFolds = 10 
    self.SO = {}
    self.phrases = [] 
    self.hits = {}

  def classify(self, words):
    pha,index = self.extractPharses(words)
    emotion = 0
    for i in pha:
      if i in self.SO:
        emotion += self.SO[i]
    emotion /= len(pha) 
    if(emotion>0):
      return 'pos'    
    return 'neg'

  def append_hits(self,e):
    if(e not in self.hits):
      self.hits[e] = 1.0001
    else:
      self.hits[e]+= 1
  
  def getPolarity(self):     
    for p in self.phrases:
      pe = 'pos: '+ p[0]+' '+p[1]
      pp = 'neg: '+ p[0]+' '+p[1]

      if(pe in self.hits):
        he = self.hits[pe]
      else:
        he = 0.01 

      if(pp in self.hits):
        hp = self.hits[pp]
      else:
        hp = 0.01 

      if(he <3 and hp < 3):
        self.SO[p] = 0.0 
      else:
        self.SO[p] = math.log( (he* self.hits['poor'])/ (self.hits['excellent'] * hp) ,2)
 
   
    
  
 

  def addExample(self, klass, word_tag):   

    phrase, index = self.extractPharses(word_tag) 
    self.phrases += list(set(phrase))

    pos_words = ['excellent']#,'perfect','outstanding','fabulous','wonderful','magnificent','good']
    neg_words = ['poor']#,'worst','worse','inferior','bad']

    n = len(word_tag)
 
    Near = 50

    for i in range(0,n):
      if(word_tag[i][0] in pos_words):# and klass=='pos'):
        self.append_hits('excellent')
        for j in range(0,len(phrase)-1):
          if( index[j] < i and index[j+1]>i):
            s = int(max([j-Near/2,0]))
            t = int(min([s+Near,len(phrase)])) 
            for k in range(s,t):
              self.append_hits('pos: ' + phrase[k][0]+ ' '+phrase[k][1]) 
            break

      elif(word_tag[i][0] in neg_words):# and klass=='neg'):
        self.append_hits('poor')
        for j in range(0,len(phrase)-1):
          if( index[j] < i and index[j+1]>i):
            s = int(max([j-Near/2,0]))
            t = int(min([s+Near,len(phrase)]))  
            for k in range(s,t):
              self.append_hits('neg: ' + phrase[k][0]+ ' '+phrase[k][1]) 
            break
        
    return 0

  def isPharse(self,word_tag):

    word = (word_tag[0][1],word_tag[1][1],word_tag[2][1])
        
    pj = r'JJ'
    pr = r'(RB\b)|(RBR\b)|(RBS\b)'
    pn = r'(NN\b)|(NNS\b)'
    pv = r'(VB\b)|(VBN\b)|(VBG\b)|(VBD\b)'

    if(re.match(pj,word[0]) and re.match(pn,word[1])):
      return 1
    elif(re.match(pj,word[0]) and re.match(pj,word[1]) and not re.match(pn,word[2])):
      return 1
    elif(re.match(pr,word[0]) and re.match(pv,word[1])):
      return 1
    elif(re.match(pr,word[0]) and re.match(pj,word[1]) and not re.match(pn,word[2])):
      return 1
    elif(re.match(pn,word[0]) and re.match(pj,word[1])  and not re.match(pn,word[2])):
      return 1

    return 0  


  def extractPharses(self,word_tag): 
    n = len(word_tag)
    word_tags = word_tag + [('*','*'),('*','*')]
    phrases = []
    index = []
    for i in range(0,n):
      word = [word_tags[i],word_tags[i+1],word_tags[i+2]]
      if(self.isPharse(word)):
        phrases += [(word[0][0],word[1][0])]
        index += [i]
    return phrases,index


  def readFile(self, fileName): 
    word_tags = []
    f = open(fileName,'r')
    for line in f:
      p = line.strip('\n').split()
      for word in p:
        w = word.split('_')
        word_tags += [(w[0].lower(),w[1])] 
    f.close() 
 
    return word_tags
  


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        if(fileName =='.DS_Store'):
          continue
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        if(fileName =='.DS_Store'):
          continue
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
  nb = Senti()
  splits = nb.crossValidationSplits(args[0])
  print ('Read file finished.')
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = Senti() 
    accuracy = 0.0
    for example in split.train:
      words = example.words
      classifier.addExample(example.klass, words) 

    classifier.getPolarity()

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
 


def main(args):   
  test10Fold(args)
  #a = Senti()
  #w = a.readFile('data/imdb2/pos/cv000_29590.txt')
  #print w
  #p = a.extractPharses(w)
  #print p
  #print a.getNearPhrase(p,200)
  #print a.extractPharses(w)
  #print w
  #print a.extractPharses(w)

if __name__ == "__main__":
    main(sys.argv[1:])
