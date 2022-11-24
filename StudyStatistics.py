################################################################################
#   StudyStatistics.py
#
#   Description:
#       A data class which holds statistics about a study passage.
#   Author:
#       Andrew Huffman
################################################################################

import datetime

class StudyStatistics:
    """A data class which holds statistics about a study passage."""

    def __init__(self, passageID: int):
        self.passageID = passageID
        """The ID of the passage which this object tracks."""
        
        self.lastStudied = datetime.date.min
        """The last time this passage was studied."""

        self.studyCount = 0
        """The number of times this passage has been studied."""

        self.correctInARow = 0
        """The number of times this passage has been reproduced correctly in a row."""

        self.dueDate = datetime.date.today()
        '''This passage\'s "due date," or the next time it should be studied.'''
    
    def isDue(self) -> bool:
        """True if the passage is due today."""
        return self.dueDate == datetime.date.today()
    
    def updateDueDate(self, correct: bool):
        """Updates the due date after the passage has been studied."""
        if correct:
            self.correctInARow += 1
        else:
            self.correctInARow = 0
        
        self.dueDate = self._getNextDueDate()
    
    def _getNextDueDate(self) -> datetime.date:
        """Calculates the next due date, based on the number of correct
        reproductions in a row. Assumes this value has already been updated."""

        return datetime.timedelta(days=int(self.correctInARow * 1.5)) + datetime.date.today()