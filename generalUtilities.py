# General Utilities for Python [Maximombro/Brody Childs]
# Allows ease of use though providing generalized methods for commonly used Python code blocks.

# Methods
# Ask the user to input a valid answer and returns the choice once answered.
# query -> String to ask the user. Has ": " appened to its end
# validAnswers -> List of answer strings that are valid
def askUser(query,validAnswers,showChoices = True):
    # Build options string
    answers = str(validAnswers[0])
    for i in range(1,len(validAnswers)):
        answers += (", "+str(validAnswers[i]))
    
    # Show Options if applicable
    if showChoices:
        print("Choose one: "+answers)
    
    # Set to lowercase valid answers
    validAnswers = [str(answer).lower() for answer in validAnswers]

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

# Prints and retains a menu system based on provided information leaving the calling program to decide function.
# title -> The title of the menu
# choices -> List of choice titles for the menu
def presentTextMenu(title,choices):
    # Print title
    print(title)

    # Print Menu
    index = 0
    numberList = []
    for choice in choices:
        # Print choice
        print("["+str(index)+"] "+choice)

        # Add choice to number list
        numberList.append(index)

        # Iterate
        index += 1

    # Print instructions
    print("Select a number to choose the option.")
    
    # Ask user for choice and return
    return askUser("Choice",numberList,False)

# Prints a text menu and handles input between an accompanied execution function all within a handled loop.
# title -> The title of the menu
# choices -> List of choice titles for the menu
# lastOption -> Option to add to the last of the choices. Often 'Back' or 'Quit'
# func -> The function to call within the script that calls this function that uses the data gathered from this function
def textMenu(title,choices,lastOption,func):
    # Prep answer choice
    answer = None

    # Add last option to choices
    choices.append(lastOption)

    # Enter main loop
    while answer == None or answer != str(len(choices)-1):
        # Present main menu and wait for input
        answer = presentTextMenu(title,choices)

        # Apply answer to main menu functions
        func(answer)
