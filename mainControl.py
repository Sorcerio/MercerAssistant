# Runs the Mercer program

# Imports
import mercer as mercerControl

# Variables

# Main Thread
def main():
    # Startup Mercer
    mercer = mercerControl.MERCER()

    # Learn test text
    mercer.learnTextFile("learn/test.txt")

    # Log the dictionary
    mercer.logDictionary()

    # Exit the dictionary
    mercer.exitMercer()

# Execute Main Thread
main()