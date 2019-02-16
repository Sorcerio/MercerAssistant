# Runs the Mercer program

# Imports
import mercer as mercerControl

# Variables

# Main Thread
def main():
    # Startup Mercer
    mercer = mercerControl.MERCER()

    # Learn test text
    mercer.learnTextFile("learn/2049.txt")

# Execute Main Thread
main()