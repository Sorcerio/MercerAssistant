# Runs the Mercer program

# Imports
import mercer as mercerControl
import generalUtilities as utils

# Variables

# Main Thread
def main():
    a = utils.askUser("What's the answer dog?",["Answer1","AnSwEr2","REAOR","wow"])
    print(a)
    b = utils.askUserYesNo("What that bool?",True)
    print(b)

# Execute Main Thread
main()
