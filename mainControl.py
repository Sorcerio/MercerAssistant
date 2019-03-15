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
    MERCER = mercerControl.MERCER(utils.askUserYesNo("Start in Debug Mode?",True))

    # Welcome message
    print("\n<< Welcome to Mercer Main Control >>")

    # Enter menu functions
    options = ["Learning Menu","Generation Menu","Administration Menu"]
    utils.textMenu("Mercer Main Menu",options,"Save and Quit",mainMenuFunctions)

    # Exit Mercer safely
    MERCER.exitMercer()

    # Safe to exit message
    print("Mercer has shutdown successfully.\nIt is now safe to close this window.")

# Functions for the main menu
def mainMenuFunctions(answer):
    # Because Python Switch statements don't exist
    if answer == "0":
        # Open Learning Menu
        options = ["Learn from File","Learn from Subreddit"]
        utils.textMenu("Learning Menu",options,"Back",learningMenuFunctions)
    elif answer == "1":
        # Open Generation Menu
        options = ["Generate Sentence","Write to File"]
        utils.textMenu("Generation Menu",options,"Back",generationMenuFunctions)
    elif answer == "2":
        # Open Admin Menu
        options = ["Log Dictionary","Show Dictionary Statistics","Toggle Debug Mode","Set Max Generation Attempts"]
        utils.textMenu("Administration Menu",options,"Back",adminMenuFunctions)

# Functions for the learning menu
def learningMenuFunctions(answer):
    # Indicate global
    global MERCER

    # Because Python Switch statements don't exist
    if answer == "0":
        # Learn from File process
        # Get filename from user
        fileName = utils.managedInput("Enter the filename here.","Cancel")

        # Check if response valid
        if fileName != None:
            # Learn from the file
            pass
    elif answer == "1":
        # Learn from Subreddit process
        print(answer)

# Functions for the learning menu
def generationMenuFunctions(answer):
    # Indicate global
    global MERCER

    # Because Python Switch statements don't exist
    if answer == "0":
        # Generate Sentece process
        print(answer)
    elif answer == "1":
        # Write to file process
        print(answer)

# Functions for the learning menu
def adminMenuFunctions(answer):
    # Indicate global
    global MERCER

    # Because Python Switch statements don't exist
    if answer == "0":
        # Log dictionary process
        print(answer)
    elif answer == "1":
        # Show dictionary statistics process
        print(answer)
    elif answer == "1":
        # Show toggle debug mode process
        print(answer)
    elif answer == "1":
        # Show set max generation attempts process
        print(answer)

# Execute Main Thread
main()
