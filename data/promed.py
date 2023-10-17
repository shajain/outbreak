import nltk
import json
import langchain as lc
import numpy
import numpy as np
import os
import pandas as pd


class ProMed:
    KEYS = ['ID', 'outbreakName', 'outbreakNameStd', 'countries', 'states', 'datePublished']
    TYPES = ['int64', 'string[pyarrow]', 'string[pyarrow]', 'string[pyarrow]','string[pyarrow]', 'datetime']
    def __int__(self, dir):
        self.dir = dir
        self.rawFiles = ['promed_'+ str(i) +'.json' for i in np.arange(1,14,1)]
        self.nRecordsPerfile = [len(json.load(open(dir+fileName))) for fileName  in self.rawFiles]
        self.nRecords = np.sum(self.nRecordsPerfile)
        self.extractionFile = 'extractions.json'
        if not os.path.isfile(dir+self.extractionFile):
            
            pd.DataFrame()



    def getAlertsBy(self, IDs, keys=[], sortbyDate=False):
        # If 'IDs' is numeric it gives the indices of the alert. The first alert in set 1 is indexed as 1, the second
        # alert as 2 and so on. The first alert in set 2 is length of first set + 1.
        # If 'IDs' is not numeric it is list of values for 'keys' to be matched to the structured extractions.
        # Returns a dictionary {'raw': list, 'structured': list} containing a list of matching
        # raw alerts within the 'raw' and a list of structured extractions in the 'structured' list. If structured
        # extractions are not available for a given key leave the corresponding dictionary entry as empty string ('')
        # if 'sortByDate' is true sort the entries in 'raw' and 'structured' lists by the 'datePublished'.
        return

    def getAllOutBreakNames(self):
        # returns a list of all outBreakNames
        return

    def standardizeOutbreakNames(self):
        # Update the file with structured information by updating 'outbreakNameStd' entry.
        return

    def updateStructuredExtractions(self, ID, dct):
        # Update the structured extraction file for the entry having index 'ID' with values in the 'dct'
        return




