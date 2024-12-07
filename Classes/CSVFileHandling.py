import csv
from Classes.Utility import Utility

class CSVFileHandling:
    def __init__(self, csvFilePath: str, colToRemove: list = []) -> None:
        self.csvFilePath_ = csvFilePath
        self.colToRemove_ = colToRemove
        self.copyFilename = self.csvFilePath_[:-4] + "Copy.csv"
    
    #Create a copy of the csv file 
    def createCopy(self) -> None:
        with open(self.csvFilePath_,'r', newline='') as csvfileRead:
            readFile = csv.reader(csvfileRead, delimiter=',')
            with open(self.copyFilename, 'w', newline='') as csvfileWrite:
                writeFile = csv.writer(csvfileWrite, delimiter=',')
                for row in readFile:
                    writeFile.writerow(row)
    
    #Create dictionary from a csv dictReader
    def createCSVDict(self, convertDate: bool) -> dict:
        with open(self.copyFilename, newline='') as csvfile:
            header = next(csv.reader(csvfile))
            reader = csv.DictReader(csvfile, fieldnames= header)
            csvDict = {}

            #Creating the dictionary
            for dictRow in reader:
                
                #Remove empty keys, add keys and update value list
                for key in dictRow:
                    if key == '' or key in self.colToRemove_:
                        continue
                    elif key not in csvDict:
                        csvDict[key] = []
                        csvDict[key].append(dictRow[key])
                    elif type(csvDict[key]) == list:
                        csvDict[key].append(dictRow[key])
            
            # YYYY-MM-DDTHH:MM:SSZ to YYYY-MM-DD example 2024-11-07T11:40:48-0600 to 2024-11-07
            if convertDate: 
                return Utility.dateTimeToDate(csvDict, 'Date') #self.dateTimeToDateTrans(csvDict)
            else:
                return csvDict
    
    #Rewrite a csv file copy 
    def rewriteCopy(self, dictCopy) -> None:
        with open(self.copyFilename,'w', newline='') as csvfileWrite:
            writeFile = csv.writer(csvfileWrite, delimiter=',')
            header = []

            #Create a list of the header
            for key in dictCopy:
                header.append(key)
            writeFile.writerow(header)

            #Write the rest of the rows from dictCopy
            lengthOfIt = len(dictCopy[header[0]])
            row = []
            for idx in range(lengthOfIt):
                for col in header:
                    row.append(dictCopy[col][idx])
                writeFile.writerow(row)
                row.clear()
        
