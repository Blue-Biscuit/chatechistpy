################################################################################
#   Passage.py
#   Description:
#       A passage to be memorized.
#   Author:
#       Andrew Huffman
################################################################################

import json

class Passage:
    """A passage to be memorized."""
    def __init__(self, title: str, text: str, id: int, tagIDs: list[int]):
        """Creates a passage to be memorized based on the string."""
        self.title = title
        self.id = id
        self.tagIDs = tagIDs
        self._text = text
        self._passage = Passage._makePassage(text)

    def __str__(self):
        return self.text
    
    def __iter__(self):
        return iter(self._passage)
    
    @property
    def text(self) -> str:
        """The full text of the passage."""
        return self._text

    def getWord(self, index: int):
        """Gets the word at an index in the passage."""
        return self._passage[index]
    
    MATCH = -1
    """Compare method return code for a match."""
    INPUT_TOO_SHORT = -2
    """Compare method return code for len(input) < len(passage)."""
    INPUT_TOO_LONG = -3
    """Compare method return code for len(input) < len(passage)."""

    def compare(self, text: str) -> tuple[int,int]:
        """Compares the two strings, and returns (word of difference, char of
        difference). Uses the MATCH, INPUT_TOO_SHORT, and INPUT_TOO_LONG
        codes to flag these situations, where either the passed-in passage
        is too short/long (with no other difference), or the passages match."""

        # ALGORITHM:
        # 1. Split the passed-in text into a passage.
        # 2. Compare the internal list with the created list.

        # 1. Split the passed-in text into a passage.

        op = Passage._makePassage(text)

        # 2. Compare the internal list with the created list.

        pLen = len(self._passage)
        oLen = len(op)

        for i in range(0, pLen):
            # If current index >= length of input, the input is too short.
            if i >= oLen:
                return (Passage.INPUT_TOO_SHORT, Passage.INPUT_TOO_SHORT)
            
            # Compare the word at i in both passages.
            pWord = self._passage[i]
            oWord = op[i]
            pWordLen = len(pWord)
            oWordLen = len(oWord)

            for j in range(0, pWordLen):
                # If the current index >= length of input word, the input is
                # too short.
                if j >= oWordLen:
                    return (i, Passage.INPUT_TOO_SHORT)
                
                # Compare the characters at j in both passages.
                pChar = pWord[j]
                oChar = oWord[j]

                if not pChar == oChar:
                    return (i, j)
            
            # If the lengths of the words are not equal, the input is too long.
            if not pWordLen == oWordLen:
                return (i, Passage.INPUT_TOO_LONG)
        
        # If the lengths are not equal, the input passage is too long.
        if not pLen == oLen:
            return (Passage.INPUT_TOO_LONG, Passage.INPUT_TOO_LONG)
        
        return (Passage.MATCH, Passage.MATCH)
    
    def toJSON(self) -> str:
        """Creates a JSON string from the Passage instance."""

        return json.dumps(self, default=lambda o: o.__dict__)
    
    def fromDict(d: dict):
        """Builds a passage from a dictionary."""

        return Passage(d['title'], d['_text'], d['id'], d['tagIDs'])
    
    def fromJSON(j: str):
        return Passage.fromDict(json.loads(j))

    def _makePassage(text: str) -> list[str]:
        """Splits a string into a list of words."""
        return text.split(None)