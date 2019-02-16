# MERCER Control System

# Imports
import os
import json

# Constants
DICTIONARY_FILE = "dictionary.mercer" # Name of the dictionary file
LOG_FILE = "mercerDebugLog.txt" # Name of the Debug log file
LOG_TAG = "Mercer" # Tag to put before Mercer system messages
NONE_TAG = "<NONE>" # Tag to denote when a string does not exist

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
                            words.append(wordPunc.strip(".,;-!?'\"").lower()) # Add more characters as applicable

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
                            print(str(leadingWord)+", "+word+", "+str(trailingWord))
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
                    if part == leadingWord:
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
                    if part == trailingWord:
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

    ## Assistant Methods
    # Switch the debug mode
    def setDebug(self,isOn):
        self.debugMode = isOn

    # Logs the dictionary to the console
    def logDictionary(self):
        # Log the dictionary
        print(self.dictionary)

    # Logs to the console and, if debug is on, to the debug log file
    def log(self,text):
        # Print to console
        print(LOG_TAG+": "+text)

        # Check if debug mode
        if self.debugMode:
            # Open the debug log file
            with open(LOG_FILE,"a") as logFile:
                logFile.write(LOG_TAG+": "+text+"\n")