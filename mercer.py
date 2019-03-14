# MERCER Control System

# Imports
import os
import json
import random
import importlib
import datetime

# Optional Imports Setup
praw = None # For Reddit connections (pip install praw)
requests = None # For general internet requests (pip install requests [or] pipenv install requests)
elementTree = None # For parsing XML data (Installed by default in Python 3)

# Constants
DICTIONARY_FILE = "dictionary.mercer" # Name of the dictionary file
LOG_FILE = "mercerDebugLog.txt" # Name of the Debug log file
LOG_TAG = "Mercer" # Tag to put before Mercer system messages
NONE_TAG = "<NONE>" # Tag to denote when a string does not exist
ADJ_TAG = "Adj" # Tag to denote when a word is a Adjective
NOUN_TAG = "Noun" # Tag to denote when a word is a Noun
VERB_TAG = "Verb" # Tag to denote when a word is a Verb
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

        # Check optional Imports
        self.checkOptionalImports()

        # Load brain data
        self.establishBrain()

        # Alert all set
        self.log("System Loaded.")

    ## Exit Protocol
    def exitMercer(self):
        # Save dictionary to file
        with open(DICTIONARY_FILE,"w") as brainFile:
            # Check debug mode
            if self.debugMode:
                # Debug mode, print dictionary fancy
                brainFile.write(json.dumps(self.dictionary, indent = 4))
            else:
                # Not debug mode, print dictionary smaller
                brainFile.write(json.dumps(self.dictionary))

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
        # Log
        self.log("Learning '"+file+"'.")

        # Check if file exists
        if os.path.isfile(file):
            # Open and read file
            with open(file,"r") as fileRead:
                # Read line by line
                for line in fileRead:
                    # Learn the line
                    self.learnTextBlock(line.strip("\n"))
        else:
            # Report file not found
            self.log("'"+file+"' does not exist.")

    # Splits and learns each sentence from a block of sentences.
    # *This is generally the function you want to start with when learning text.*
    def learnTextBlock(self,textBlock):
        # Split the sentences apart
        sentences = textBlock.split(".?!")

        # Check if empty
        if len(sentences) > 0:
            for sentence in sentences:
                # Learn the line
                self.learnLine(sentence)

    # Splits and learns the sentence that is fed to the function.
    def learnLine(self,line):
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
        self.log("Writing a "+str(textLength)+"x"+str(sentenceMaxLength)+" text block.")

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

    # Connect to Reddit via Reddit API and learn words from the specified subreddit
    # maxItems -> Max items to read from the subreddit's hot list
    # subreddit -> The name of the subreddit to search
    def learnFromSubReddit(self,maxItems,subreddit):
        # Check if dependencies are loaded
        if praw != None:
            # Set name variable
            subredditName = subreddit

            # Log
            self.log("Accessing the first "+str(maxItems)+" items on /r/"+subredditName+".")

            # Connect to Reddit
            reddit = praw.Reddit("mercer")

            # Connect to subreddit
            subreddit = reddit.subreddit(subreddit)

            # Loop through fetched submissions
            for post in subreddit.hot(limit=maxItems):
                # Make sure score is good
                if post.score > 0:
                    # Make sure body isn't empty
                    if post.selftext != None and post.selftext != "":
                        # Log
                        # self.log("Learning from post '"+post.title+"' on /r/"+subredditName+".")
                        self.log("Learning ~"+str(len(post.selftext.split(" ")))+" words from '"+post.title+"'.")

                        # Learn the words
                        self.learnTextBlock(post.selftext)
                    else:
                        # Log empty thing
                        self.log("'"+post.title+"' had no body text. Ignoring.")
        else:
            # praw not imported
            self.log("'praw' was not imported. Reddit features are disabled.")

    # Accesses and converts to an element tree a specified RSS Feed (or web page)
    # Returns 'None' if the proper imports are not avalible
    def pullRSSFeed(self,link):
        # Check if dependencies are loaded
        if requests != None and elementTree != None:
            # TODO: Write functionality

            # Return XML/HTML/etc data for parsing
            return "TEMP"
        else:
            # requests or elementTree are not loaded
            self.log("'requests' was not imported. Web connectivity features unavalible.")

            # Return a failure indicator
            return None

    # Pull the BBC News RSS Feed and skim the articles that are found on it.
    # maxItems -> Max items to skim. A value of -1 indicates no limit beyond that of the RSS feed's content
    def learnFromBBCNews(self,maxItems = -1):
        # Connect to RSS Feed
        feed = self.pullRSSFeed("http://feeds.bbci.co.uk/news/rss.xml")

        # Check if data is ok
        if feed != None:
            # TODO: Functionality
            pass

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
        # Build time stamp
        timeStamp = str(datetime.datetime.now()).split(".")[0]

        # Print to console
        print("("+timeStamp+") "+LOG_TAG+": "+text)

        # Check if debug mode
        if self.debugMode:
            # Open the debug log file
            with open(LOG_FILE,"a") as logFile:
                logFile.write("("+timeStamp+") "+LOG_TAG+": "+text+"\n")

    # Attempts to find and activate optional imports
    def checkOptionalImports(self):
        # Ensure globals
        global praw
        global requests
        global elementTree

        # Import praw
        if importlib.util.find_spec("praw") != None:
            # Import the module
            praw = importlib.import_module("praw")
        else:
            # Report
            self.log("'praw' was not imported. Reddit features unavalible.")

        # Import requests and elementTree
        if importlib.util.find_spec("requests") != None and importlib.util.find_spec("xml.etree.ElementTree") != None:
            # Import the modules
            requests = importlib.import_module("requests")
            elementTree = importlib.import_module("xml.etree.ElementTree")
        else:
            # Report
            self.log("'requests' was not imported. Web connectivity features unavalible.")

    # Calculates various statistics about the current dictionary possessed by Mercer
    # Either handles its own printing, or can be retrieved as a dictionary containing the data
    # Default functionality is to handle its own printing
    def getDictionaryStats(self,shouldPrint=True):
        # Prep word count
        wordCount = 0

        # Prep most common type
        typeCounter = {
            NOUN_TAG: 0,
            ADJ_TAG: 0,
            VERB_TAG: 0,
            NONE_TAG: 0
        }

        # Loop through dictionary
        for word in self.dictionary:
            # Get word type
            if self.dictionary[word]['type'] in typeCounter:
                # Iterate count
                typeCounter[self.dictionary[word]['type']] += 1
            else:
                # Add to count
                typeCounter[self.dictionary[word]['type']] = 0

            # Add word count
            wordCount += 1

        # Check mode
        if shouldPrint:
            # Print mode
            # Print the data
            print("Dictionary Statistics:")
            print("Total Word Count: "+str(wordCount)+",")
            print("Noun Count: "+str(typeCounter[NOUN_TAG])+",")
            print("Adjective Count: "+str(typeCounter[ADJ_TAG])+",")
            print("Verb Count: "+str(typeCounter[VERB_TAG])+",")
            print("Unknown Count: "+str(typeCounter[NONE_TAG]))

            # Return blank
            return None
        else:
            # Return mode
            # Translate
            typeCounter['Nouns'] = typeCounter.pop(NOUN_TAG)
            typeCounter['Adjectives'] = typeCounter.pop(ADJ_TAG)
            typeCounter['Verbs'] = typeCounter.pop(VERB_TAG)
            typeCounter['Unknown'] = typeCounter.pop(NONE_TAG)

            # Build Dictionary
            outData = {
                "totalWords": wordCount,
                "typeCounts": typeCounter
            }

            # Return data
            return outData
