################################################################################
#   helpers.py
#   Description
#       Some helper functions, used across the app.
#   Author
#       Andrew H
################################################################################

def joinAfter(args: list[str], start: int) -> str:
    """Joins the strings in the list at and after the start value with a space."""

    output = ""
    oneIterRun = False
    for i in range(start, len(args)):
        oneIterRun = True
        output = f"{output}{args[i]} "
    
    if oneIterRun:
        return output[0:(len(output) - 1)]
    else:
        return output

def isInt(x: str) -> bool:
    """True if the given string is an integer."""

    try:
        int(x)
        return True
    except:
        return False

def firstWordIsInteger(x: str) -> bool:
    """True if the first space-delineated token is an integer."""

    tokens = x.split(None)

    if len(tokens) == 0:
        return False
    
    firstWord = tokens[0]

    if isInt(firstWord):
        return True
    else:
        return False