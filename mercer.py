# MERCER Control System

# Imports
import os
import json

# Constants
DICTIONARY_FILE = "dictionary.mercer" # Name of the dictionary file
LOG_FILE = "mercerDebugLog.txt" # Name of the Debug log file
LOG_TAG = "Mercer" # Tag to put before Mercer system messages

# The MERCER Class structure
class MERCER:
    ## Constructor
    def __init__(self,debug = False):
        # Set debug mode
        self.debugMode = debug

        # Alert startup
        self.log("Initializing.")

        # Load brain data
        self.establishBrain()

        # Alert all set
        self.log("System Loaded.")

    ## Functional Methods
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

    ## Assistant Methods
    def log(self,text):
        # Print to console
        print(LOG_TAG+": "+text)

        # Check if debug mode
        if self.debugMode:
            # Open the debug log file
            with open(LOG_FILE,"a") as logFile:
                logFile.write(LOG_TAG+": "+text+"\n")