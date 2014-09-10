#!/usr/bin/python
#
# Viterbi tagger routine
#
# Implemented by:  Anthony L. Daniell, 10 March 2013
#
#
#

import sys
import emissionParam
import qTriParam

#
# Set some calling arguments
#

#corpusFile = "/Users/anthonydaniell/Desktop/OnlineCourses/naturalLanguageProcessing/programs/ProgrammingAssignment1/Part2/viterbiInputCorpus.txt"
corpusFile = "/Users/anthonydaniell/Desktop/OnlineCourses/naturalLanguageProcessing/programs/ProgrammingAssignment1/Part2/gene.test"

#countFile = "/Users/anthonydaniell/Desktop/OnlineCourses/naturalLanguageProcessing/programs/ProgrammingAssignment1/Part2/tagCorpusNGram.txt"
countFile = "/Users/anthonydaniell/Desktop/OnlineCourses/naturalLanguageProcessing/programs/ProgrammingAssignment1/Part2/gene.train.rare.count"

#tagFile = "/Users/anthonydaniell/Desktop/OnlineCourses/naturalLanguageProcessing/programs/ProgrammingAssignment1/Part2/viterbiOutput.out"
tagFile = "/Users/anthonydaniell/Desktop/OnlineCourses/naturalLanguageProcessing/programs/ProgrammingAssignment1/Part2/gene_test.p2.out"

tagFileDiag = "/Users/anthonydaniell/Desktop/OnlineCourses/naturalLanguageProcessing/programs/ProgrammingAssignment1/Part2/viterbiOutputDiag.out"
#tagFileDiag = "/Users/anthonydaniell/Desktop/OnlineCourses/naturalLanguageProcessing/programs/ProgrammingAssignment1/Part2/gen_test.p1.diag.out"

#
# open the files and loop over the lines 
#

inFileCorpus = open( corpusFile, "r" )
outFileTag = open( tagFile, "w" )
outFileTagDiag = open( tagFileDiag, "w" )

#
# Figure out the possible Tags
#

tagList = ['O', 'I-GENE']

#   inFileCount = open(countFile, "r")

#   for tagString in iter(inFileCount):

#      tagStringSplit = tagString.split()
#      if tagStringSplit[1] == "WORDTAG":
#         for tag in tagList:
#            if tag == tagStringSplit[2]:
#               break
#            else:
#               taglist.append(tagStringSplit[2])

#   inFileCount.close()

#
# Main Vertibi Algorithm with Backpointers
#

#
# Read in first sentence - Look for blank line as STOP/break symbol.
#

startOfSentence = 1 

for currString in iter(inFileCorpus):

   if startOfSentence == 1:
      sentencePos = 1
      startOfSentence = 0
      pie = ['0 * *']
      pieValList = [1]
      bp = ['#'] 
      wordSequence = []
      tagSequence = []

#
# regular line.  Branch out if we hit the space (sentence separator)
#


   if currString <> "\n":
      currStringSplit = currString.split()
      currWord = currStringSplit[0] 
      wordSequence.append(currWord)

#
# Loop through count File to see if currWord is rare
# if so, set it to the _RARE_ flag and process as normal
#

      inFileCount = open(countFile, "r")
      rareTest = 1
      for rareTestString in iter(inFileCount):
         rareTestStringSplit = rareTestString.split()
         if rareTestStringSplit[1] == "WORDTAG":
            if currWord == rareTestStringSplit[3]:
               rareTest = 0
               break
      inFileCount.close()

      if rareTest == 1:
         currWord = "_RARE_"

#
# Compute pie and bp on the fly
#

      if sentencePos == 1:
         S_km2 = ['*']
         S_km1 = ['*']
         S_k = tagList
      elif sentencePos == 2:
         S_km2 = ['*']
         S_km1 = tagList
         S_k = tagList
      else:
         S_km2 = tagList
         S_km1 = tagList
         S_k = tagList

#
#  Do the triple loop to find the max at the current sentence position
#
#      print "Top of loop"
#      print "sentencePos = ", sentencePos
#      print "currWord = ", currWord
      for u in S_km1:
         for v in S_k:
            pieMax = 0
            wMax = ''
            for w in S_km2:

#
# Find the previous sentence position pieMax corresponding
# to w and u.  Note the search string decoding order of
# arguments (k-1, w, u) is different than the encoding order
# below for the present sentence position, (k, u, v) 
#


               searchStr = str(sentencePos-1) + " " + w + " " + u
#               print "new search:"
#               print "w, u, v = " + w + " " + u + " " + v 
               searchIndex = pie.index(searchStr)
               priorPieMax = pieValList[searchIndex]
#               print "searchStr = ", searchStr
#               print "searchIndex = ", searchIndex
#               print "priorPieMax = ", priorPieMax

#
# Encode the max results in the pie list
#

               em = emissionParam.emissionParam ( currWord, v, countFile)
#               print "\n"
               qT = qTriParam.qTriParam( v, w, u, countFile )
               pieVal = priorPieMax * qT * em

#               print "qTriParam = ", qT
#               print "emissionParam = ", em
#               print "pieVal = ", pieVal

               if pieVal >= pieMax:
                  pieMax = pieVal
                  wMax = w

#
# Populate the pieList with the max value for u,v
# 
            addString = str(sentencePos) + " " + u + " " + v
            pie.append(addString)
            pieValList.append(pieMax) 
            bp.append(wMax)
#            print "w = ", w
#            print "u = ", u
#            print "v = ", v
#            print "pie = ", pie
#            print "pieValList = ", pieValList
#            print "bp = ", bp
#            print "\n"               

#      print "End of Loop"
#      print "\n"
      sentencePos = sentencePos+1
   else:
      startOfSentence = 1
#      print "End of sentence."
#      print "\n"

#
# Now do the end of sentence tag processing
#

#      print "Sentence tag decoding section:"
#
# Set (y_nm1, y_n) = arg max(u,v) [ pie(n,u,v) x q(STOP|u,v) ]
#
# Initialize the tag sequence with the wordSequence just to have the correct length.
#
      sentencePos = sentencePos - 1
      for ii in range(0,sentencePos):
         tagSequence.append('X') 
      
#      print "SentencePos = ", sentencePos
#      print "tagSequence before bp processing = ", tagSequence

      pieMax = 0.0
      for u in S_k:
         for v in S_k:   
            searchStr = str(sentencePos) + " " + u + " " + v 
#            print "new search:"
#            print "searchStr = " + searchStr
#            print " u, v = "  + u + " " + v 
            searchIndex = pie.index(searchStr)
            priorPieMax = pieValList[searchIndex]
            qT = qTriParam.qTriParam( 'STOP', u, v, countFile ) 
            finalProduct = priorPieMax * qT

#            print "searchIndex = ", searchIndex
#            print "priorPieMax = ", priorPieMax
#            print "qT = ", qT
#            print "finalProduct = ", finalProduct
#            print "pieMax = ", pieMax

            if finalProduct >= pieMax:
               tagSequence[sentencePos-1] = v
               tagSequence[sentencePos-2] = u
               pieMax = finalProduct 
            
#            print "updated pieMax = ", pieMax
      
#      print "tagSequence = ", tagSequence      

#
# for k = (n-2)...1,
#
# y_k = bp(k+2, y_kp1, y_kp2) 
#
# recall that pie has the same structure as bp (backpointer)
# so we search bp to find the index for the tag
#

#      print "Second part of tag construction."
      for k in range(sentencePos-2, 0, -1):

#         print "k = ", k
	 searchStr = str(k+2) + " " + tagSequence[k] + " " + tagSequence[k+1] 
#         print "searchStr = ", searchStr
         searchIndex = pie.index(searchStr)
         foundTag = bp[searchIndex]
         tagSequence[k-1] = foundTag
         
#         print "searchIndex = ", searchIndex
#         print "foundTag = ", foundTag
#         print "tagSequence = ", tagSequence
#
# When we have sentence, then dump out to tagFile
#

#      print "Final Result:"
#      print "Word Sequence =  ", wordSequence
#      print "Tag Sequence = ", tagSequence

      for k in range(0,sentencePos):
         outString = wordSequence[k] + " " + tagSequence[k] + "\n"
         outFileTag.write(outString)

#   outStringDiag = currStringSplit[0] + " " + yMax + " " + str(eMax) + "\n"
#   outFileTagDiag.write(outStringDiag)

#
# Put the blank line separator at the end of each sentence
#
      outFileTag.write("\n")
#
# Clean up and exit
#

inFileCorpus.close()
outFileTag.close()
outFileTagDiag.close()

#
# End of program
#
