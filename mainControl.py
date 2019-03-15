# Runs the Mercer program

# Imports
import mercer as mercerControl
import generalUtilities as utils

# Variables

# Main Thread
def main():
    # Welcome message
    print("Welcome to Mercer Main Control.\n")

    # Startup Mercer in specified mode
    mercer = mercerControl.MERCER(utils.askUserYesNo("Start in Debug Mode?",True))

    # Enter menu functions
    options = ["Learning Menu","Generation Menu","Administration Menu"]
    utils.textMenu("Mercer Main Menu",options,"Save and Quit",mainMenuFunctions)

    # Exit Mercer safely
    mercer.exitMercer()

# Functions of the options in the main menu
def mainMenuFunctions(answer):
    # Because Python Switch statements don't exist
    if answer == "0":
        # Open Learning Menu
        learningMenu()
    elif answer == "1":
        # Open Generation Menu
        generationMenu()
    elif answer == "2":
        # Open Admin Menu
        adminMenu()

# Ask for information in the Learning Menu
def learningMenu():
    print("Learning Menu!")

# Ask for information in the Learning Menu
def generationMenu():
    print("Gen Menu!")

# Ask for information in the Learning Menu
def adminMenu():
    print("Admin Menu!")

# Execute Main Thread
main()
