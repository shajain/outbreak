import re

import nltk
import json
import langchain as lc
import numpy
import numpy as np
import os
import pandas as pd
import glob
import pdb


class ProMed:
    FIELDS = {'ID': 'Int64', 'archiveNumber': 'string[pyarrow]', 'outbreakName': 'string[pyarrow]', 'outbreakNameStd': 'string[pyarrow]',
              'countries': 'string[pyarrow]', 'states': 'string[pyarrow]',
              'datePublished': 'datetime64[ns]'}

    def __init__(self, dir):
        #pdb.set_trace()
        self.dir = dir
        self.dirArchive = os.path.join(dir, 'extractions')
        self.rawFileNames = ['promed_' + str(i) + '.json' for i in np.arange(1, 14, 1)]
        self.nRecordsPerfile = [len(json.load(open(os.path.join(dir,fileName)))) for fileName in self.rawFileNames]
        self.nRecords = np.sum(self.nRecordsPerfile)
        self.extractionFile = 'extraction'
        if not self.extractionFileExists():
            #self.df = pd.DataFrame({k: np.array(self.nRecords, dtype=object) for k, dt in ProMed.FIELDS.items()})

            self.df = pd.DataFrame({k: [None if not pd.api.types.is_numeric_dtype(dt) else np.nan]*self.nRecords for k, dt in ProMed.FIELDS.items()})
            #pdb.set_trace()
            self.df['ID'] = np.arange(self.nRecords)
            self.df.astype(dtype=ProMed.FIELDS)
            self.overwriteExtractions(self.df)
        else:
            self.df = self.readExtractionFile()
            fields = ProMed.FIELDS.keys()
            absent = np.where(np.array([f not in self.df.columns for f in fields]))[0]
            if absent.size > 0:
                for a in absent:
                    dt = ProMed.FIELDS[fields[a]]
                    self.df[fields[a]] = [None if not pd.api.types.is_numeric_dtype(dt) else np.nan] * self.nRecords
                self.df.astype(dtype=ProMed.FIELDS)
                self.overwriteExtractions(self.df)



    def readExtractionFile(self, archive=False):
        if not archive:
            df = pd.read_json(self.getExtractionFileName())
        else:
            df = pd.read_json(self.getLatestArchiveFileName())
        return df

    def getExtractionFileName(self):
        fName = self.extractionFile + '.json'
        return fName

    def extractionFileExists(self):
        return os.path.isfile(self.getExtractionFileName())

    def archiveFileExists(self):
        files = glob.glob(os.path.join(self.dirArchive, '*'))
        exists = True
        if len(files) == 0:
            exists = False
        return exists

    def getLatestArchiveFileName(self):
        files = glob.glob(os.path.join(self.dirArchive, '*'))
        if len(files) == 0:
            return False
        else:
            ix = np.argmax([int(re.findall(r'\d+', file)[0]) for file in files])
            fileName = files[ix]
            fileName = os.path.join(self.dirArchive,fileName)
            return fileName


    def overwriteExtractions(self, df):
        fName = self.getExtractionFileName()
        #pdb.set_trace()
        if self.extractionFileExists():
            self.add2Archive()
        with open(fName, 'w') as file:
            df.to_json(file)
        return

    def add2Archive(self):
        df = pd.read_json(self.extractionFile + '.json')
        files = glob.glob(os.path.join(self.dirArchive, '*'))
        suffix = max([int(re.findall(r'\d+', file)[0]) for file in files]+[0]) + 1
        outFile = os.path.join(self.dirArchive, self.extractionFile + str(suffix) + '.json')
        df.to_json(open(outFile, 'w'))
        return

    def getAlertsBy(self, val, match_keys=[] , sortbyDate=False):
        # If 'IDs' is numeric it gives the indices of the alert. The first alert in set 1 is indexed as 1, the second
        # alert as 2 and so on. The first alert in set 2 is length of first set + 1.
        # If 'IDs' is not numeric it is list of values for 'keys' to be matched to the structured extractions.
        # Returns a dictionary {'raw': list, 'structured': list} containing a list of matching
        # raw alerts within the 'raw' and a list of structured extractions in the 'structured' list. If structured
        # extractions are not available for a given key leave the corresponding dictionary entry as empty string ('')
        # if 'sortByDate' is true sort the entries in 'raw' and 'structured' lists by the 'datePublished'.
        return

    def getSubject(self, IDs):

        return

    def getBody(self, IDs):

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




