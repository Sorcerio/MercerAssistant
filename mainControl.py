# Runs the Mercer program

# Imports
import mercer as mercerControl

# Variables

# Main Thread
def main():
    # Startup Mercer in Debug Mode
    mercer = mercerControl.MERCER(True)

    # # Learn test text
    # mercer.learnTextFile("learn/test.txt")
    # mercer.learnTextFile("learn/2049.txt")
    # mercer.learnTextFile("learn/PrideAndPrejudice.txt")

    # Learn from Reddit skimming
    mercer.learnFromReddit(10,"learnPython")

    # # Log the dictionary
    # mercer.logDictionary()

    # # Print sentence
    # print(mercer.createSentence(5))

    # # Write text to file
    # mercer.writeTextToFile(7,7,"testText.txt")

    # Exit the dictionary
    mercer.exitMercer()

# Execute Main Thread
main()
