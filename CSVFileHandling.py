import csv
from typing import Optional  # Import Optional for handling potential errors

# Handle .csv file for Tastytrade, Robinhood and Schwab
class CSVFileHandling:
    def __init__(self, csvFilePath: str, colToRemove: list = []) -> None:
        self.csvFilePath_ = csvFilePath
        self.colToRemove_ = colToRemove
        self.copyFilename = self.csvFilePath_[:-4] + "Copy.csv"
    
    #Create a copy of the csv file 
    def createCopy(self) -> None:
        try:
            with open(self.csvFilePath_,'r', newline='') as csvfileRead:
                readFile = csv.reader(csvfileRead, delimiter=',')
                with open(self.copyFilename, 'w', newline='') as csvfileWrite:
                    writeFile = csv.writer(csvfileWrite, delimiter=',')
                    for row in readFile:
                        writeFile.writerow(row)
            #print("Copy was successful")
            #return writeFile
        except FileNotFoundError:
            print("Files Not Found While Copying")
    
    #Create dictionary from a csv dictReader
    def createCSVDict(self) -> Optional[dict]:
        try:
            with open(self.copyFilename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                csvDict = {}
                for dictRow in reader:
                    #print(dictRow)
                    for key in dictRow:
                        #print("Hello World")
                        if key == '' or key in self.colToRemove_:
                            continue
                        elif key not in csvDict:
                            csvDict[key] = []
                        elif type(csvDict[key]) == list:
                            csvDict[key].append(dictRow[key])
                           
                #print("Creating dict from csv file is successful")
                return dict(csvDict)
        except FileNotFoundError:
            print("File Not Found While Creating Dictionary")
            return None
        
    #Rewrite a csv file copy 
    def rewriteCopy(self, dictCopy) -> None:
        try:
            with open(self.copyFilename,'w', newline='') as csvfileWrite:
                writeFile = csv.writer(csvfileWrite, delimiter=',')
                header = []

                #Create a list of the header
                for key in dictCopy:
                    header.append(key)
                print(header)
                writeFile.writerow(header)
        except FileNotFoundError:
            print("Files Not Found While Copying")
        
