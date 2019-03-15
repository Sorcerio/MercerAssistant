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

    # Establish main loop variables
    answer = None
    options = ["Option A","Option B","Option C","Quit"]

    # Enter main loop
    while answer == None or answer != str(len(options)-1):
        # Present main menu and wait for input
        answer = utils.presentTextMenu("Mercer Main Menu",options)      

    # Exit Mercer safely
    mercer.exitMercer()

# Execute Main Thread
main()
