#!/usr/bin/python
##
##
## Function to compute the q trigram  parameter for 
## use in HMM NLP application.
##
## q(y_i | y_im2, y_im1) = count(y_im2, y_im1, y_i)/count(y_im2, y_im1)
##
## Implemented by: Anthony L. Daniell, 10 March 2013
## Based on Coursera NLP Course, Programming Assignment 1 Instructions (ver h1-p.2.pdf). 
## 

import sys

def qTriParam( y_i, y_im2, y_im1, countFile ):

   inFile = open(countFile, "r")

#   print "qTriParam:"
#   print "y_i = " , y_i 
#   print "y_im1 = ", y_im1
#   print "y_im2 = ", y_im2
#   print countFile	
#   print "\n"    

   triCount = 0
   biCount = 0

#
# Read the corpus of tags and obtain the counts
#

   for stringIn in iter(inFile): 

#
# Read in each line and check for the n-GRAM keyword
# 

#
# Do the bigram count first, then trigram
#

      stringSplit = stringIn.split()

      if stringSplit[1] == "2-GRAM":
         if stringSplit[2] == y_im2:
            if stringSplit[3] == y_im1:
               biCount = biCount + int(stringSplit[0])

      elif stringSplit[1] == "3-GRAM":
         if stringSplit[2] == y_im2:
            if stringSplit[3] == y_im1:
               if stringSplit[4] == y_i:
                  triCount = triCount + int(stringSplit[0]) 

#
# Compute the return value
#
   
#   print "Final qTri parameters:"
#   print "biCount = ", biCount
#   print "triCount = ", triCount
#   print "\n"

   if biCount > 0: 
      qTriParamVal = float(triCount)/float(biCount) 
   else:
      qTriParamVal = 0

#
# Clean up and return
#

   inFile.close() 
   return qTriParamVal

#
# End of program
#
