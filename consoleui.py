import Passage
import helpers

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

    try:
        id = int(args[1])
        isId = True
    except:
        title = helpers.joinAfter(args, 1)
    
    # Find the passage
    p: Passage.Passage = None

    for x in passages:
        if isId and x.id == id:
            p = x
        elif not isId and x.title == title:
            p = x
    
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

def learnCommand(args: list[str], passages: list[Passage.Passage]):
    """Plays a game with the selected passage."""

    # ALGORITHM:
    # 1. Input parse. If input wasn't sufficient, error and exit.
    # 2. Run the game until it has been completed (a fully blank passage has
    # been repeated.)

    # 1. Input parse. If input wasn't sufficient, error and exit.

    # If no args are given, print usage data.
    if len(args) == 1:
        print("usage: learn <title | id>")
        print()
        return


    # 2. Run the game until it has been completed (a fully blank passage has
    # been repeated.)

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
    "learn" : {
        "help" : "plays a memorization game with the provided passage.",
        "method" : learnCommand
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