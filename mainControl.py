# Runs the Mercer program

# Imports
import mercer as mercerControl
import generalUtilities as utils

# Variables

# Main Thread
def main():
    # Startup Mercer in specified mode
    mercer = mercerControl.MERCER(utils.askUserYesNo("Start in Debug Mode?",True))

    # Welcome message
    print("\n<< Welcome to Mercer Main Control >>")

    # Enter menu functions
    options = ["Learning Menu","Generation Menu","Administration Menu"]
    utils.textMenu("Mercer Main Menu",options,"Save and Quit",mainMenuFunctions)

    # Exit Mercer safely
    mercer.exitMercer()

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
    # Because Python Switch statements don't exist
    if answer == "0":
        # Learn from File process
        print(answer)
    elif answer == "1":
        # Learn from Subreddit process
        print(answer)

# Functions for the learning menu
def generationMenuFunctions(answer):
    # Because Python Switch statements don't exist
    if answer == "0":
        # Generate Sentece process
        print(answer)
    elif answer == "1":
        # Write to file process
        print(answer)

# Functions for the learning menu
def adminMenuFunctions(answer):
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
