import Passage
import consoleui

CONSOLE_UI = 1
"""Run code for the console UI."""

def loadPassages() -> list[Passage.Passage]:
    """Loads the passages which have been saved. TODO: implement."""
    return [] 

def main(mode: int):
    """Runs the program."""

    passages = loadPassages()

    if mode == CONSOLE_UI:
        consoleui.run(passages)

if __name__ == "__main__":
    main(CONSOLE_UI)