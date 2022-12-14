import Passage
import helpers
import random
import time
import datetime

def getPassage(passages: list[Passage.Passage], args: list[str], selectionArgLoc: int) -> Passage.Passage | None:
    """Gets a passage based on id (if the string is int-parsable) or name."""

    result = None

    if helpers.isInt(args[selectionArgLoc]):
        id = int(args[selectionArgLoc])

        for x in passages:
            if x.id == id:
                result = x
                break
    else:
        title = helpers.joinAfter(args, selectionArgLoc)

        for x in passages:
            if x.title == title:
                result = x
                break
    
    return result

def newCommand(args: list[str], passages: list[Passage.Passage]):
    done = False
    title: str
    text: str

    # Prompt for a title.
    while not done:
        title = input("title? >>> ")

        if title.lower() == "exit":
            print()
            return
        
        if helpers.isInt(title):
            print("The title of a passage cannot be an integer.")
            print()
        
        elif helpers.firstWordIsInteger(title):
            print("The first word of a title cannot be an integer.")
            print()
        
        elif not (title.isspace() or len(title) == 0):
            done = True
    
    # Prompt for text.
    done = False
    while not done:
        text = input("text? >>> ")

        if text.lower() == "exit":
            print()
            return
        
        if not (text.isspace() or len(text) == 0):
            done = True
    
    # Assign an id.
    id = 0
    for x in passages:
        if x.id > id:
            id = x.id
    id += 1
    
    # Create the passage.
    passages.append(Passage.Passage(title.strip(), text, id, []))
    print()

def printCommand(args: list[str], passages: list[Passage.Passage]):
    # If no args are given, print usage data.
    if len(args) == 1:
        print("usage: print <title | id>")
        print()
        return
    
    isId = False
    id: int
    title: str

    p = getPassage(passages, args, 1)
    
    # Print the passage if found
    if p == None:
        print(f'Passage "{args[1]}" not found')
        print()
    else:
        print(p.title)
        print()
        print(p.text)
        print()
    
def listCommand(args: list[str], passages: list[Passage.Passage]):
    for x in passages:
        print(f"{x.id}: {x.title}")
    print()

def exitCommand(args: list[str], passages: list[Passage.Passage]):
    exit()

def helpCommand(args: list[str], passages: list[Passage.Passage]):
    global COMMANDS

    for x in COMMANDS:
        print(f"{x}\t\t{COMMANDS[x]['help']}")
    print()

LEARN_EXIT_SIGNAL = 0
LEARN_OK_SIGNAL = 1
LEARN_ERROR_SIGNAL = 2

def learnCommand(args: list[str], passages: list[Passage.Passage]):
    """Plays a game with the selected passage."""

    # ALGORITHM:
    # 1. Input parse. If input wasn't sufficient, error and exit.
    # 2. Run the game until it has been completed (a fully blank passage has
    # been repeated.)

    SECS_BETWEEN_TURNS = 3
    """The number of seconds the program halts between turns."""

    # 1. Input parse. If input wasn't sufficient, error and exit.

    # If no args are given, print usage data.
    if len(args) == 1:
        print("usage: learn <title | id>")
        print()
        return LEARN_ERROR_SIGNAL

    p = getPassage(passages, args, 1)
    if p == None:
        print(f'Passage "{helpers.joinAfter(args, 1)}" not found')
        print()
        return LEARN_ERROR_SIGNAL

    helpers.clearConsole()

    # 2. Run the game until it has been completed (a fully blank passage has
    # been repeated.)

    done = False
    blanks = []
    for ignored in p:
        blanks.append(False)
    
    def fullyBlanked(b: list[bool]):
        """Helper internal method to check if the boolean list is all true."""
        for x in b:
            if not x:
                return False
        
        return True
    
    def blankRandom(b: list[bool]):
        """Blanks a random word in the boolean list."""

        if fullyBlanked(b):
            return

        updated = False
        while not updated:
            i = random.choice(range(0, len(b)))
            if not b[i]:
                b[i] = True
                updated = True

    while not done:
        # ALGORITHM:
        # 1. Print a blanked string, representing the passage.
        # 2. Get user input.
        # 3. If the input was correct and the passage is entirely blanks, complete.
        # 4. If the input was otherwise correct, blank a random word and continue.
        # 5. If the user was incorrect, continue.

        # 1. Print a blanked string, representing the passage.

        for (word, blank) in zip(p, blanks):
            if blank:
                for ignored in word:
                    print('_', end='')
                print(' ', end='')
            else:
                print(word, end=' ')
        print()
        print()

        # 2. Get user input.

        i = input(">>> ")

        if i.lower() == 'exit':
            return LEARN_EXIT_SIGNAL

        compareResult = p.compare(i)

        # 3. If the input was correct and the passage is entirely blanks, complete.

        if compareResult == (Passage.Passage.MATCH, Passage.Passage.MATCH) and fullyBlanked(blanks):
            print("Correct!")
            print()
            done = True

        # 4. If the input was otherwise correct, blank a random word and continue.

        elif compareResult == (Passage.Passage.MATCH, Passage.Passage.MATCH):
            print("Correct!")
            blankRandom(blanks)
            print()
            time.sleep(SECS_BETWEEN_TURNS)
            helpers.clearConsole()

        # 5. If the user was incorrect, continue.

        else:
            print("Sorry, that was incorrect.")
            print()

            if compareResult[0] == Passage.Passage.INPUT_TOO_SHORT:
                print('Input was too short.')
                print()
            elif compareResult[0] == Passage.Passage.INPUT_TOO_LONG:
                print('Input was too long.')
                print()
            else:
                wordNum = compareResult[0]
                pin = Passage.Passage('', i, -1, [])

                inWord = pin.getWord(wordNum)
                word = p.getWord(wordNum)
                print(f'Error at word {wordNum+1}, "{inWord}"')
                print(f'Should have been "{word}"')
                print()


            time.sleep(SECS_BETWEEN_TURNS)
            helpers.clearConsole()

    return LEARN_OK_SIGNAL

ROTE_EXIT_SIGNAL = 0
ROTE_CORRECT_SIGNAL = 1
ROTE_INCORRECT_SIGNAL = 2
ROTE_ERROR_SIGNAL = 3

def roteCommand(args: list[str], passages: list[Passage.Passage]):
    """Simple command to study a passage by rote typing it. Returns an exit code."""

    # ALGORITHM:
    # 1. Input parse. If input wasn't sufficient, error and exit.
    # 2. Ask the user to reproduce the passage.
    # 3. Notify the user whether they correctly reproduced the passage or not.

    # 1. Input parse. If input wasn't sufficient, error and exit.

    # If no args are given, print usage data.
    if len(args) == 1:
        print("usage: learn <title | id>")
        print()
        return ROTE_ERROR_SIGNAL

    p = getPassage(passages, args, 1)
    if p == None:
        print(f'Passage "{helpers.joinAfter(args, 1)}" not found')
        print()
        return ROTE_ERROR_SIGNAL

    helpers.clearConsole()

    # 2. Ask the user to reproduce the passage.

    print(f'Reproduce "{p.title}"')
    print()

    i = ''
    while i == '':
        i = input(">>> ").strip()

        # If 'exit' was input, exit.
        if i.lower() == 'exit':
            print()
            return ROTE_EXIT_SIGNAL

    # 3. Notify the user whether they correctly reproduced the passage or not.

    matchResult = p.compare(i)

    result = ROTE_ERROR_SIGNAL
    print()
    if matchResult[0] == Passage.Passage.MATCH and matchResult[1] == Passage.Passage.MATCH:
        print("Congratulations! That was correct.")
        result = ROTE_CORRECT_SIGNAL
    else:
        print("Sorry, that was incorrect.")
        print()

        result = ROTE_INCORRECT_SIGNAL

        if matchResult[0] == Passage.Passage.INPUT_TOO_SHORT:
            print("The input was too short.")
        elif matchResult[0] == Passage.Passage.INPUT_TOO_LONG:
            print("The input was too long.")
        else:
            pI = Passage.Passage("", i, -1, [])
            if matchResult[1] == Passage.Passage.INPUT_TOO_SHORT:
                print(f'Input word {matchResult[0]}, "{pI.getWord(matchResult[0])}", was too short (should have been "{p.getWord(matchResult[0])}")')
            elif matchResult[1] == Passage.Passage.INPUT_TOO_LONG:
                print(f'Input word {matchResult[0]}, "{pI.getWord(matchResult[0])}", was too long (should have been "{p.getWord(matchResult[0])}")')
            else:
                print(f'Input word {matchResult[0]}, "{pI.getWord(matchResult[0])}", character {matchResult[1]}, was incorrect (should have been "{p.getWord(matchResult[0])}")')
    print()
    return result

def saveCommand(args: list[str], passages: list[Passage.Passage]):
    """Saves the current passages list to a file."""

    # ALGORITHM:
    # 1. Check input for errors.
    # 2. Write to the file the JSON-serialized list.

    # 1. Check input for errors.

    if len(args) == 1:
        print("Usage: save <path>")
        print()
        return
    elif len(passages) == 0:
        print("Nothing to save.")
        print()
        return

    filepath = args[1]
    f = None

    try:
        f = open(filepath, 'w')
    except:
        print(f'Error opening "{filepath}" for writing.')
        print()
        return

    # 2. Write to the file the JSON-serialized list.

    j = '['
    for p in passages:
        j += p.toJSON()
        j += ','
    j = j[0:len(j)-1]
    j += ']'

    f.write(j)
    f.close()

def loadCommand(args: list[str], passages: list[Passage.Passage]):
    """Loads a list of passages from a file, and appends them to the current one."""

    # ALGORITHM:
    # 1. Check args for errors.
    # 2. Append the contents of the list from the file to the current list.

    # 1. Check args for errors.

    if len(args) == 1:
        print("Usage: load <path>")
        print()
        return
    
    filepath = args[1]
    f = None
    try:
        f = open(filepath, 'r')
    except:
        print(f'Error opening "{filepath}" for reading.')
        print()
        return
    
    j = f.read()

    # 2. Append the contents of the list from the file to the current list.

    l = Passage.Passage.fromJSONList(j)
    for x in l:
        passages.append(x)

def dueCommand(args: list[str], passages: list[Passage.Passage]):
    """Prints the due date of the selected passage."""

    # If no args are given, print usage data.
    if len(args) == 1:
        print("usage: due <title | id>")
        print()
        return

    p = getPassage(passages, args, 1)
    if p == None:
        print(f'Passage "{helpers.joinAfter(args, 1)}" not found')
        print()
        return
    
    fromNow = p.statistics.dueDate - datetime.date.today()
    parenthetical = ''

    if fromNow.days == 0:
        parenthetical = 'today'
    elif fromNow.days < 0:
        parenthetical = f'{fromNow.days * -1} day{"s" if fromNow.days < -1 else ""} ago'
    else:
        parenthetical = f'{fromNow.days} day{"s" if fromNow.days > 1 else ""} from now'
    print(f'{p.statistics.dueDate} ({parenthetical})')

    print()

def studyCommand(args: list[str], passages: list[Passage.Passage]):
    """Studies all due passages, and updates their statistics accordingly."""

    # ALGORITHM:
    # 1. Loop through the passages list, studying those that are due.

    # 1. Loop through the passages list, studying those that are due.
    studiedOne = False

    for p in passages:
        # ALGORITHM:
        # 1. If a passage has been studied before, "learn" it.
        # 2. Otherwise, "rote" it.
        # 3. Update statistics.

        if not p.statistics.isDue():
            continue
        
        studiedOne = True

        correctInARow = p.statistics.correctInARow

        # 1. If a passage has been studied before, "learn" it.

        if p.statistics.studyCount == 0:
            cmd = ["learn", p.title]
            sg = learnCommand(cmd, passages)

            # If the user sent an exit signal, exit the study command.
            if sg == LEARN_EXIT_SIGNAL:
                return
            else:
                correctInARow += 1

        # 2. Otherwise, "rote" it.

        else:
            cmd = ["rote", p.title]
            sg = roteCommand(cmd, passages)

            # If the user sent an exit signal, exit the study command.
            if sg == ROTE_EXIT_SIGNAL:
                return
            
            # If the user was incorrect, relearn.
            if sg == ROTE_INCORRECT_SIGNAL:
                correctInARow = 0
                cmd2 = ["learn", p.id]
                sg = learnCommand(cmd2, passages)

                # If the user sent an exit signal, exit the study command.
                if sg == LEARN_EXIT_SIGNAL:
                    return
                else:
                    correctInARow += 1

        # 3. Update statistics.

        p.statistics.correctInARow = correctInARow
        p.statistics.studyCount += 1
        p.statistics.updateDueDate()

    if studiedOne:
        print("Study session complete.")
        print()
    else:
        print("Nothing to study right now.")
        print()

COMMANDS = {
    "new" : {
        "help" : "creates a new passage.",
        "method" : newCommand
    },
    "print" : {
        "help" : "prints a passage",
        "method" : printCommand
    },
    "list" : {
        "help" : "lists passages.",
        "method" : listCommand
    },
    "study" : {
        "help" : "studies all new commands while updating study statistics.",
        "method" : studyCommand
    },
    "learn" : {
        "help" : "plays a memorization game with the provided passage.",
        "method" : learnCommand
    },
    "rote" : {
        "help" : "tests a provided passage by asking for its content without hints.",
        "method" : roteCommand
    },
    "due" : {
        "help" : "prints the due date of a passage.",
        "method" : dueCommand
    },
    "save" : {
        "help" : "saves the current passages list to a file.",
        "method" : saveCommand
    },
    "load" : {
        "help" : "loads passages from a file.",
        "method" : loadCommand
    },
    "exit" : {
        "help" : "exits the program.",
        "method" : exitCommand
    },
    "help" : {
        "help" : "prints a short description of all UI commands.",
        "method" : helpCommand
    }
}

def run(passages: list[Passage.Passage]):
    """Runs the console UI."""

    while True:
        # Get user input.
        i = input(">> ")
        command = i.split(None)

        # If the user input something,
        if not len(command) == 0:

            # Run the given command.
            commandName = command[0].lower()
            if commandName in COMMANDS:
                COMMANDS[commandName]["method"](command, passages)
            else:
                print(f"Unrecognized command \"{commandName}\"")
                print()

run([])