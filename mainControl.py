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

    # Present main menu
    utils.presentTextMenu("Mercer Main Menu",["Option A","Option B","Option C","Quit"])

    # Exit Mercer safely
    mercer.exitMercer()

# Execute Main Thread
main()
