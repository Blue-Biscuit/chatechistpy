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

        self.dueDate = datetime.date.today()
        '''This passage\'s "due date," or the next time it should be studied.'''