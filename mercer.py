# MERCER Control System
# By: Brody Childs/Maximombro

# Imports
import os
import json
import random
import importlib
from importlib import util as importlibutil
import datetime
import math
import re

# Optional Imports Setup
praw = None # For Reddit connections (pip install praw)
requests = None # For general internet requests (pip install requests [or] pipenv install requests)
elementTree = None # For parsing XML data (Installed by default in Python 3)

# Constants
DICTIONARY_FILE = "dictionary.mercer" # Name of the dictionary file
LOG_FILE = "mercerDebugLog.txt" # Name of the Debug log file
LOG_TAG = "Mercer" # Tag to put before Mercer system messages
NONE_TAG = "<NONE>" # Tag to denote when a string does not exist
WORD_TYPE_TAGS = { # Tags to denote when a word is appropritate type. Format: [Type Name : Tag]
    "adjective":"Adj",
    "noun":"Noun",
    "verb":"Verb"
}
MAX_ATTEMPTS = 10 # The maximum amount of attempts for various generations
MAX_COMMONALITY_DIFFERENCE = 75 # What percentage (1 to 100) from the top of a word's commonality list should be considered when generating sentences
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

            # Return success
            return True
        else:
            # Report file not found
            self.log("'"+file+"' does not exist.")

            # Return failure
            return False

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
        sentence = self.cleanWord(seed)

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
                    sentence = (sentence+" "+self.cleanWord(newWord))
                    lastWord = newWord
                    
                    # Break out
                    break

        # Log finish
        self.log("Sentence created.")

        # Return the formated sentence
        return (sentence[0].capitalize()+sentence[1:]+".")

    # Ensures that a word fits the print standard and corrects capitolization on personal Is
    def cleanWord(self,word):
        # Prepare clean word
        cleanWord = ""

        # Remove Unicode characters
        cleanWord = re.sub(r'[^\x00-\x7f]', r'', word)

        # Remove bad tags
        cleanWord = cleanWord.replace("\n","")
        cleanWord = cleanWord.replace("\t","")

        # Check for personal I
        if cleanWord == "i":
            cleanWord = "I"

        # Send the cleaned one
        return cleanWord

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

            # Get highest commonality
            highestCommonality = max(list(commonalities.keys()))

            # Calculate minimum commonality
            minCommoness = math.floor(highestCommonality-(highestCommonality*(MAX_COMMONALITY_DIFFERENCE/100)))

            # Ensure at least one
            if minCommoness < 1:
                minCommoness = 1

            # Trim commonalities to only avalible keys
            validKeys = []
            for key in list(commonalities.keys()):
                # Check if key is higher than min
                if key >= minCommoness:
                    validKeys.append(key)

            # Log the keys
            self.log("Using "+str(len(validKeys))+"/"+str(len(list(commonalities.keys())))+" options for word to follow '"+str(leadingWord)+"'.")

            # Return none on Index Errors
            try:
                # Choose commonality
                commonKey = random.choice(validKeys)

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

            # Return success
            return True
        else:
            # praw not imported
            self.log("'praw' was not imported. Reddit features are disabled.")

            # Return failure
            return False

    # Accesses and converts to an element tree a specified RSS Feed (or web page)
    # Returns 'None' if the proper imports are not avalible
    def pullRSSFeed(self,link):
        # Check if dependencies are loaded
        if requests != None and elementTree != None:
            # Pull XML data
            data = requests.get(link)

            # Prepare root attempt
            root = None
            try:
                # Try to parse XML
                root = elementTree.fromstring(data.content)

                # Return XML/HTML/etc data for parsing
                return root
            except elementTree.ParseError as err:
                # Log inability to access
                self.log("Could not parse XML from '"+str(link)+"'.")

                # Return a failure indicator
                return None
        else:
            # requests or elementTree are not loaded
            self.log("'requests' was not imported. Web connectivity features unavalible.")

            # Return a failure indicator
            return None

    # Pull the BBC News RSS Feed and skim the articles that are found on it.
    # maxItems -> Max items to skim. A value of -1 indicates no limit beyond that of the RSS feed's content
    # def learnFromBBCNews(self,maxItems = -1):
    #     # Connect to RSS Feed
    #     feed = self.pullRSSFeed("http://feeds.bbci.co.uk/news/rss.xml")

    #     # Check if imports and data are ok
    #     if feed != None:
    #         # Loop through returned items
    #         i = 0
    #         for item in feed.find("channel").findall("item"):
    #             # Check if limit met
    #             if maxItems == -1 or i < maxItems:
    #                 # Pull title and link
    #                 itemTitle = item.find("title").text.lstrip("<![CDATA[").rstrip("]]>")
    #                 itemLink = item.find("guid").text
    #                 print(itemTitle,itemLink)

    #                 # Attempt to open article
    #                 # TODO: Try and fix the parsing of the website
    #                 article = self.pullRSSFeed(itemLink)

    #                 # Check if bad data
    #                 if article != None:
    #                     # Log
    #                     self.log("Learning from '"+itemTitle+"' on BBC.")

    #                     # Loop through paragraph elements in the article
    #                     for p in article.find("body").find("div[@class='direction']").find("div[@id='orb-modules']").find("div[@id='site-container']").find("div[@id='page']").find("div[@role='main']").find("div[@class='container']").find("div[@class='container--primary-and-secondary-columns']").find("div[@class='column--primary']").find("div[@class='story-body']").find("div[@class='story-body__inner']").findall("p"):
    #                         print(p.text)
                    
    #                 # Iterate
    #                 i += 1

    # Sets the type of the specified word within the dictionary
    def setWordType(self,word,wordType):
        # Check if type is a valid type
        if wordType.lower() in WORD_TYPE_TAGS or wordType == NONE_TAG:
            # Make sure word is in dictionary
            if word in self.dictionary:
                # Set the type
                self.dictionary[word]['type'] = wordType

                # Return success
                return True
            else:
                # Log word does not exist failure
                self.log(str(word)+" is not in the dictionary.")

                # Return failure
                return False
        else:
            # Word type is not valid
            self.log(str(wordType)+" is not a valid type of word.")

            # Return failure
            return False

    ## Assistant Methods
    # Switch the debug mode
    def setDebug(self,isOn):
        # Set debug mode
        self.debugMode = isOn

        # Log
        self.log("Set Debug Mode to "+str(isOn)+".")

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

        # Log
        self.log("Set Max Generation Attempts to "+str(attempts)+".")

    # Logs to the console and, if debug is on, to the debug log file
    def log(self,text):
        # Build time stamp
        timeStamp = str(datetime.datetime.now()).split(".")[0]

        # Open the log file
        with open(LOG_FILE,"a") as logFile:
            logFile.write("("+timeStamp+") "+LOG_TAG+": "+text+"\n")

        # Check if debug mode
        if self.debugMode:
            # Print to console
            print("("+timeStamp+") "+LOG_TAG+": "+text)  

    # Attempts to find and activate optional imports
    def checkOptionalImports(self):
        # Ensure globals
        global praw
        global requests
        global elementTree

        # Import praw
        if importlibutil.find_spec("praw") != None:
            # Import the module
            praw = importlib.import_module("praw")
        else:
            # Report
            self.log("'praw' was not imported. Reddit features unavalible.")

        # Import requests and elementTree
        if importlibutil.find_spec("requests") != None and importlibutil.find_spec("xml.etree.ElementTree") != None:
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
            WORD_TYPE_TAGS['noun']: 0,
            WORD_TYPE_TAGS['adjective']: 0,
            WORD_TYPE_TAGS['verb']: 0,
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
            # Print the title
            print("Dictionary Statistics:")

            # Print the word count
            print("Total Word Count: "+str(wordCount))

            # Print the data
            for wordType in WORD_TYPE_TAGS:
                print(wordType.capitalize()+" Count:"+str(typeCounter[WORD_TYPE_TAGS[wordType]]))

            # Print unknown
            print("Unknown Count: "+str(typeCounter[NONE_TAG]))

            # Return blank
            return None
        else:
            # Return mode
            # Translate data
            for wordType in WORD_TYPE_TAGS:
                typeCounter[wordType.capitalize()] = typeCounter.pop(WORD_TYPE_TAGS[wordType])

            # Build Dictionary
            outData = {
                "totalWords": wordCount,
                "typeCounts": typeCounter
            }

            # Return data
            return outData
    
    # Gets the dict of word types
    def getWordTypeTags(self):
        global WORD_TYPE_TAGS
        return WORD_TYPE_TAGS

    # Gets the NONE_TAG
    def getNoneTag(self):
        global NONE_TAG
        return NONE_TAG

    # Gets the Max Commonality Difference
    def getMaxCommonalityDifference(self):
        global MAX_COMMONALITY_DIFFERENCE
        return MAX_COMMONALITY_DIFFERENCE

    def setMaxCommonalityDifference(self,amount):
        # Establish global
        global MAX_COMMONALITY_DIFFERENCE

        # Asking forgiveness is the Python way
        try:
            # Make sure within bounds
            if amount > 100:
                amount = 100
            if amount < 1:
                amount = 1

            # Set amount
            MAX_COMMONALITY_DIFFERENCE = amount

            # Log
            self.log("Set Max Commonality Difference to top "+str(amount)+"%.")
        except TypeError as err:
            self.log(str(amount)+" is not a valid amount to set the Max Commonality Difference to.")
