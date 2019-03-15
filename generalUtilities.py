# General Utilities for Python [Maximombro/Brody Childs]
# Allows ease of use though providing generalized methods for commonly used Python code blocks.

# Methods
# Ask the user to input a valid answer and returns the choice once answered.
# query -> String to ask the user. Has ": " appened to its end
# validAnswers -> List of answer strings that are valid
def askUser(query,validAnswers):
    # Build options string
    answers = validAnswers[0]
    for i in range(1,len(validAnswers)):
        answers += (", "+validAnswers[i])
    
    # Show Options
    print("Choose one: "+answers)
    
    # Set to lowercase valid answers
    validAnswers = [answer.lower() for answer in validAnswers]

    # Enter query loop
    answer = None
    while answer == None or answer.lower() not in validAnswers:
        # Ask user for input
        answer = input(query+": ")

    # Return answer
    return answer

# Asks the user a yes or no question.
# query -> String to ask the user. Has ": " appened to its end
def askUserYesNo(query,boolean = False):
    # Check what mode
    if boolean:
        # Ask user
        answer = askUser(query,["Yes","No"])

        # Check answer
        if answer == "yes":
            return True
        else:
            return False
    else:
        # Run standard questioning
        return askUser(query,["Yes","No"])