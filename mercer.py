# MERCER Control System

# Imports
import os
import json
import random

# Constants
DICTIONARY_FILE = "dictionary.mercer" # Name of the dictionary file
LOG_FILE = "mercerDebugLog.txt" # Name of the Debug log file
LOG_TAG = "Mercer" # Tag to put before Mercer system messages
NONE_TAG = "<NONE>" # Tag to denote when a string does not exist
MAX_ATTEMPTS = 10 # The maximum amount of attempts for various generations
MAX_COMMONALITY_DIFFERENCE = 3 # The maximum distance that a word can be from the most common recorded in terms of commonality
MIN_WORDS_IN_SENTENCE = 4 # The minimum number of words to be used in a sentence

# The MERCER Class structure
class MERCER:
    ## Constructor
    def __init__(self, debug = False):
        # Set debug mode
        self.debugMode = debug

        # Alert startup
        self.log("Initializing.")

        # Load brain data
        self.establishBrain()

        # Alert all set
        self.log("System Loaded.")

    ## Exit Protocol
    def exitMercer(self):
        # Save dictionary to file
        with open(DICTIONARY_FILE,"w") as brainFile:
            brainFile.write(json.dumps(self.dictionary, indent = 4))

        # Report exit
        self.log("Mercer ready to close.")

    ## Functional Methods
    # Establish the JSON formatted brain data
    def establishBrain(self):
        # Check if dictionary exists
        if not os.path.isfile(DICTIONARY_FILE):
            # Create it
            with open(DICTIONARY_FILE,"w") as brainFile:
                brainFile.write("{\n}")

        # Establish dictionary
        with open(DICTIONARY_FILE,"r") as brainFile:
            # Convert data to JSON
            self.dictionary = json.loads(brainFile.read())

    # Learn a plain text file like .txt or similar
    def learnTextFile(self, file):
        # Check if file exists
        if os.path.isfile(file):
            # Open and read file
            with open(file,"r") as fileRead:
                # Read line by line
                for line in fileRead:
                    # Loop through words to clean them
                    words = []
                    for wordPunc in line.strip().split(" "):
                        if wordPunc != "":
                            words.append(wordPunc.strip(".,;-!?'\"").strip(u'\u201c').strip(u'\u201d').strip(u'\u201c').strip(u'--').lower()) # Add more characters as applicable

                    # Make sure it's not empty
                    if len(words) > 0:
                        # Establish current word index
                        wordIndex = 0

                        # Loop through words
                        for word in words:
                            # Establish leading words
                            if wordIndex > 0:
                                leadingWord = words[wordIndex-1]
                            else:
                                # Default
                                leadingWord = NONE_TAG

                            # Establish trailing words
                            if (wordIndex+1) < len(words):
                                trailingWord = words[wordIndex+1]
                            else:
                                # Default
                                trailingWord = NONE_TAG

                            # Log information
                            self.learnWordRelation(leadingWord,word,trailingWord)

                            # Iterate
                            wordIndex += 1
        else:
            # Report file not found
            self.log("'"+file+"' does not exist.")

    # Learn the word's relationship
    def learnWordRelation(self,leadingWord,word,trailingWord):
        # Check for leading word to add
        leadText = None
        if leadingWord != NONE_TAG:
            leadText = {"word": leadingWord, "occurances": 1}
        
        # Check for trailing word to add
        trailText = None
        if trailingWord != NONE_TAG:
            trailText = {"word": trailingWord, "occurances": 1}

        # Look for parent word
        if word in self.dictionary:
            # Word found, add data to current knowlege
            # Check leading text
            if leadText != None:
                # Loop through attachment list
                index = 0
                found = False
                for part in self.dictionary[word]["leading"]:
                    # Find the part
                    if part["word"] == leadingWord:
                        # Set found
                        found = True

                        # Increase common count
                        self.dictionary[word]["leading"][index]["occurances"] += 1

                    # Iterate
                    index += 1

                # Check if word was found
                if not found:
                    # Add to dictionary
                    self.dictionary[word]["leading"].append(leadText)

            # Check trailing text
            if trailText != None:
                # Loop through attachment list
                index = 0
                found = False
                for part in self.dictionary[word]["trailing"]:
                    # Find the part
                    if part["word"] == trailingWord:
                        # Set found
                        found = True

                        # Increase common count
                        self.dictionary[word]["trailing"][index]["occurances"] += 1

                    # Iterate
                    index += 1

                # Check if word was found
                if not found:
                    # Add to dictionary
                    self.dictionary[word]["trailing"].append(trailText)

        else:
            # Word not found, create new entry
            wordData = None
            if leadText == None and trailText == None:
                # No lead or trail text
                wordData = {
                    "type": NONE_TAG,
                    "leading": [],
                    "trailing": []
                }
            elif leadText == None:
                # No lead text
                wordData = {
                    "type": NONE_TAG,
                    "leading": [],
                    "trailing": [trailText]
                }
            elif trailText == None:
                # No trail text
                wordData = {
                    "type": NONE_TAG,
                    "leading": [leadText],
                    "trailing": []
                }
            else:
                # Trail and Lead text are present
                wordData = {
                    "type": NONE_TAG,
                    "leading": [leadText],
                    "trailing": [trailText]
                }

            # Add word to dictionary
            self.dictionary[word] = wordData

    # Writes a specific length text block from dictionary
    def writeText(self,textLength,sentenceMaxLength):
        # Log
        self.log("Writing a "+str(textLength)+" text block.")

        # Etablish text block
        textBlock = ""

        # Write each sentence
        for sentenceNumber in range(0,textLength):
            # Choose sentence length
            sentenceLength = random.randint(MIN_WORDS_IN_SENTENCE,sentenceMaxLength)

            # Write and save sentence
            textBlock = (textBlock+(self.createSentence(sentenceLength))+"\n")

        # Return text block
        return textBlock

    # Writes a specific length text block from dictionary to a file. Be sure to include extension in file name
    def writeTextToFile(self,textLength,sentenceMaxLength,fileName):
        # Open the file
        with open(fileName,"w") as outFile:
            outFile.write(self.writeText(textLength,sentenceMaxLength))

        # Log
        self.log("Wrote text to '"+str(fileName)+"'.")

    # Writes a sentence using Mercer's loaded dictionary
    def createSentence(self,maxLength):
        # Log sentence creation
        self.log("Creating sentence.")

        # Create sentence variable
        sentence = ""

        # Pick seed word
        seed = list(self.dictionary.keys())[random.randint(0,len(self.dictionary))]

        # Add seed to sentence
        sentence = seed

        # Attempt to reach max length of words
        lastWord = seed
        for currentWord in range(0,(maxLength-1)):
            # Attempt for max attempts
            for attempts in range(0,MAX_ATTEMPTS):
                # Pick word to follow
                newWord = self.chooseWordToFollow(lastWord)

                # Check if word was found
                if newWord != NONE_TAG and newWord != None:
                    # Add to sentence
                    sentence = (sentence+" "+newWord)
                    lastWord = newWord
                    
                    # Break out
                    break

        # Log finish
        self.log("Sentence created.")

        # Return sentence
        return (sentence.capitalize()+".")

    # Attempts to find a word that follows the leading word
    def chooseWordToFollow(self,leadingWord):
        # Check if word is present in dictionary
        if leadingWord in self.dictionary:
            # Prep commonality list
            commonalities = {}

            # Build word options based on commonalities
            for part in self.dictionary[leadingWord]["trailing"]:
                # Check if node already present
                if part["occurances"] not in commonalities:
                    # Not present, create the list
                    commonalities[part["occurances"]] = []

                # Add to the commonality list
                commonalities[part["occurances"]].append(part["word"])

            # Return none on Index Errors
            try:
                # Choose commonality
                commonKey = random.choice(list(commonalities.keys()))

                # Pick and return word
                return commonalities[commonKey][random.randint(0,(len(commonalities[commonKey])-1))]
            except IndexError as err:
                # Failed, return None
                return NONE_TAG
        else:
            # Word not present
            return NONE_TAG

    ## Assistant Methods
    # Switch the debug mode
    def setDebug(self,isOn):
        self.debugMode = isOn

    # Logs the dictionary to the console
    def logDictionary(self):
        # Log the dictionary
        print(self.dictionary)

    # Sets the maximum attempts
    def setMaxGenerationAttempts(self,attempts):
        # Establish global for change
        global MAX_ATTEMPTS

        # Set attempts
        MAX_ATTEMPTS = attempts

    # Logs to the console and, if debug is on, to the debug log file
    def log(self,text):
        # Print to console
        print(LOG_TAG+": "+text)

        # Check if debug mode
        if self.debugMode:
            # Open the debug log file
            with open(LOG_FILE,"a") as logFile:
                logFile.write(LOG_TAG+": "+text+"\n")