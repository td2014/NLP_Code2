#!/usr/bin/python
#
# Routine to test the triQParam.py routine
#
# Implemented by:  Anthony L. Daniell, 10 March 2013
#
import sys
import qTriParam

#
# Set some calling arguments
#
y_i = "O"
y_im1 = "*"
y_im2 = "*"

corpusFile = "/Users/anthonydaniell/Desktop/OnlineCourses/naturalLanguageProcessing/programs/ProgrammingAssignment1/Part2/tagCorpusNGram.txt"

#
# Echo back the set parameters
# 

print "Main:"
print y_i 
print y_im1
print y_im2
print corpusFile
print "\n"

#
# Make the call
#
  
qTriVal = qTriParam.qTriParam( y_i, y_im1, y_im2,  corpusFile )

print "Returned Value =\n"
print qTriVal 

#
# Clean up and exit
#
