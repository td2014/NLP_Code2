#!/usr/bin/python
##
##
## Function to compute the emission parameter for 
## use in HMM NLP application.
##
##
## Implemented by: Anthony L. Daniell, 5 March 2013
## Based on Coursera NLP Course, Programming Assignment 1 Instructions (ver h1-p.1.pdf). 
## 

import sys

#
#  Formula:
#   
#  emissionParamVal(x|y) =   Count( y~> x)/count(y)
#
#

def emissionParam( x, y, corpusFile ):

   inFile = open(corpusFile, "r")

#   print "emissionParam:"
#   print "x = ", x
#   print "y = ", y
#   print "corpusFile = ", corpusFile	
#   print "\n"    

#
# Need to determine how many times the word x gets tagged by y in the training corpus.
# Also need to count the number of times the tag y is present
#

   tagCount = 0
   xyCount = 0

#
# Read the corpus of tags and obtain the counts
#

   for stringIn in iter(inFile): 

#
# Read in each line and check for the WORDTAG keyword
# 

      stringSplit = stringIn.split()

      if stringSplit[1] == "WORDTAG":
         if stringSplit[2] == y:
            tagCount = tagCount + int(stringSplit[0])
            if stringSplit[3] == x:
               xyCount = xyCount + int(stringSplit[0])


#
# Compute the return value
#
   
#   print "Final emission parameters:"
#   print "tagCount = ", tagCount
#   print "xyCount = ", xyCount

   if tagCount > 0: 
      emissionParamVal = float(xyCount)/float(tagCount) 
   else:
      emissionParamVal = 0
#
# Clean up and return
#

   inFile.close() 
   return emissionParamVal

#
# End of program
#
