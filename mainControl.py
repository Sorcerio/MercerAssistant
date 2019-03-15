# Runs the Mercer program

# Imports
import mercer as mercerControl
import generalUtilities as utils

# Variables
MERCER = None

# Main Thread
def main():
    # Indicate global
    global MERCER

    # Startup Mercer in specified mode
    mode = utils.askUserYesNo("Start in Debug Mode?",True)
    MERCER = mercerControl.MERCER(mode)

    # Welcome message
    print("\n<< Welcome to Mercer Main Control >>")

    # Enter menu functions
    options = ["Learning Menu","Generation Menu","Administration Menu"]
    utils.textMenu("Mercer Main Menu",options,"Save and Quit",mainMenuFunctions)

    # Exit Mercer safely
    MERCER.exitMercer()

    # Safe to exit message
    print("\nMercer has shutdown successfully.\nIt is now safe to close this window.")

# Functions for the main menu
def mainMenuFunctions(answer):
    # Because Python Switch statements don't exist
    if answer == "0":
        # Open Learning Menu
        options = ["Learn from File","Learn from Subreddit"]
        utils.textMenu("Learning Menu",options,"Back to Main Menu",learningMenuFunctions)
    elif answer == "1":
        # Open Generation Menu
        options = ["Generate Sentence","Write to File"]
        utils.textMenu("Generation Menu",options,"Back to Main Menu",generationMenuFunctions)
    elif answer == "2":
        # Open Admin Menu
        options = ["Log Dictionary","Show Dictionary Statistics","Toggle Debug Mode","Set Max Generation Attempts"]
        utils.textMenu("Administration Menu",options,"Back to Main Menu",adminMenuFunctions)

# Functions for the learning menu
def learningMenuFunctions(answer):
    # Indicate global
    global MERCER

    # Because Python Switch statements don't exist
    if answer == "0":
        # Learn from File process
        # Get filename from user
        fileName = utils.managedInput("Enter the file path to the .txt file","Cancel")

        # Check if response valid
        if fileName != None:
            # Learn from the file
            print("")
            learned = MERCER.learnTextFile(fileName)

            # Check if success
            if not learned:
                print("'"+fileName+"' could not be read.")
    elif answer == "1":
        # Learn from Subreddit process
        # Get subreddit
        subreddit = utils.managedInput("Enter the subreddit to skim","Cancel")

        # Check if valid
        if subreddit != None:
            # Get the post limit
            postLimit = utils.managedInputNumber("Max number of posts to read in /r/"+subreddit,"Cancel")

            # Check if valid
            if postLimit != None:
                # Learn from the subreddit
                learned = MERCER.learnFromSubReddit(postLimit,subreddit)

                # Check if success
                if not learned:
                    print("/r/"+subreddit+" could not be read. Check the log for details.")

# Functions for the generation menu
def generationMenuFunctions(answer):
    # Indicate global
    global MERCER

    # Because Python Switch statements don't exist
    if answer == "0":
        # Generate Sentence process
        print("Generating Sentence.")
        print(MERCER.createSentence(7))
    elif answer == "1":
        # Write to file process
        # Ask where
        path = utils.managedInput("Output file path","Cancel")

        # Check if valid
        if path != None:
            # Ask for file length
            length = utils.managedInputNumber("Max number of lines to generate","Cancel")

            # Check if valid
            if length != None:
                # Generate the file
                MERCER.writeTextToFile(length,7,path)

                # Report done
                print("File at '"+path+"' has been generated.")

# Functions for the admin menu
def adminMenuFunctions(answer):
    # Indicate global
    global MERCER

    # Because Python Switch statements don't exist
    if answer == "0":
        # Log dictionary process
        # Ask if user is sure
        print("This is a massive text dump that is often not human readable.")
        shouldContinue = utils.askUserYesNo("Are you sure you want to continue?",True)

        # Check if should continue
        if shouldContinue:
            print(MERCER.logDictionary())
    elif answer == "1":
        # Show dictionary statistics process
        MERCER.getDictionaryStats()
    elif answer == "2":
        # Show toggle debug mode process
        # Ask for mode to switch
        mode = utils.askUserYesNo("Enable Debug Mode?",True)

        # Set the mode
        MERCER.setDebug(mode)
        
        # Choose print
        if mode:
            print("Debug Mode has been enabled.")
        else:
            print("Debug Mode has been disabled.")
    elif answer == "3":
        # Show set max generation attempts process
        # Enter number
        maxNum = utils.managedInputNumber("Set max generation attempts to","Cancel")

        # Check
        minLimit = 1
        if maxNum != None and maxNum >= minLimit:
            MERCER.setMaxGenerationAttempts(maxNum)
        elif maxNum < minLimit:
            print(str(minLimit)+" is minimum max generation attempts that can be set.")

# Execute Main Thread
main()
