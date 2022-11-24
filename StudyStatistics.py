################################################################################
#   StudyStatistics.py
#
#   Description:
#       A data class which holds statistics about a study passage.
#   Author:
#       Andrew Huffman
################################################################################

import datetime
import json

class StudyStatistics:
    """A data class which holds statistics about a study passage."""

    def __init__(self, passageID: int, lastStudied = datetime.date.min, studyCount = 0, correctInARow = 0, dueDate = datetime.date.today()):
        self.passageID = passageID
        """The ID of the passage which this object tracks."""
        
        self.lastStudied = lastStudied
        """The last time this passage was studied."""

        self.studyCount = studyCount
        """The number of times this passage has been studied."""

        self.correctInARow = correctInARow
        """The number of times this passage has been reproduced correctly in a row."""

        self.dueDate = dueDate
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
    
    def toJSON(self) -> str:
        """Creates a JSON string from the StudyStatistics instance."""

        def json_default(x):
            if isinstance(x, datetime.date):
                return {'day':x.day, 'month':x.month, 'year':x.year}
            else:
                return x.__dict__

        return json.dumps(self, default=lambda o: json_default(o))
    
    def fromDict(d: dict):
        """Builds a StudyStatistics instance from a dictionary."""

        def dateFromDict(d):
            return datetime.date(d['year'], d['month'], d['day'])

        return StudyStatistics(d["passageID"], dateFromDict(d["lastStudied"]), d["studyCount"], d["correctInARow"], dateFromDict(d["dueDate"]))
    
    def fromJSON(s: str):
        """Builds a StudyStatistics instance from a json string."""
        d = json.loads(s)
        return StudyStatistics.fromDict(d)