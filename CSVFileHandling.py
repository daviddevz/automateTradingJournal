import csv
from typing import Optional  # Import Optional for handling potential errors

# Handle .csv file for Tastytrade, Robinhood and Schwab
class CSVFileHandling:
    def __init__(self, journalFilePath: str, transFilePath: str) -> None:
        self.journalFilePath_ = journalFilePath
        self.transFilePath_ = transFilePath
        self.copyFilename = self.journalFilePath_[:-4] + "Copy.csv"
    
    #create a copy of the csv file 
    def createCopy(self) -> None: #Optional[csv.writer]:
        try:
            with open(self.journalFilePath_,'r', newline='') as csvfileRead:
                readFile = csv.reader(csvfileRead, delimiter=',')
                with open(self.copyFilename, 'w', newline='') as csvfileWrite:
                    
                    writeFile = csv.writer(csvfileWrite, delimiter=',')
                    for row in readFile:
                        writeFile.writerow(row)
            print("Copy was successful")
            #return writeFile
        except FileNotFoundError:
            print("Files Not Found While Copying")
            #return None
    
    """ def createRef(self) -> Optional[csv.reader]:
        try:
            with open(self.transFilePath_, 'r', newline='') as csvfile:
                readFile = csv.reader(csvfile, delimiter=',')
            print("Reference was successful")
            return readFile
        except FileNotFoundError:
            print("Files Not Found While Referencing")
            return None """
    
    #create a csv file dictionary obect
    def createCSVDict(self) -> Optional[csv.DictReader]:
        try:
            with open(self.copyFilename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                return reader
        except FileNotFoundError:
            print("File Not Found While Reading")
            return None
        
