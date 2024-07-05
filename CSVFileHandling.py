import csv
from typing import Optional  # Import Optional for handling potential errors

# Handle .csv file for Tastytrade, Robinhood and Schwab
class CSVFileHandling:
    def __init__(self, journalFilePath: str, transFilePath: str) -> None:
        self.journalFilePath_ = journalFilePath
        self.transFilePath_ = transFilePath
    
    def createCopy(self) -> Optional[csv.writer]:
        try:
            with open(self.journalFilePath_,'r', newline='') as csvfileRead:
                readFile = csv.reader(csvfileRead, delimiter=',')
                copyFilename = self.journalFilePath_[:-4] + "Copy.csv"
                with open(copyFilename, 'w', newline='') as csvfileWrite:
                    
                    writeFile = csv.writer(csvfileWrite, delimiter=',')
                    for row in readFile:
                        writeFile.writerow(row)
            print("Copy was successful")
            return writeFile
        except FileNotFoundError:
            print("Files Not Found while copying")
            return None
    
    def createRef(self) -> Optional[csv.reader]:
        try:
            with open(self.transFilePath_, 'r', newline='') as csvfile:
                readFile = csv.reader(csvfile, delimiter=',')
            print("Reference was successful")
            return readFile
        except FileNotFoundError:
            print("Files Not Found while referencing")
            return None
        
