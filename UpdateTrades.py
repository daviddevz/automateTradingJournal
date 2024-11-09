import csv
from typing import Optional  # Import Optional for handling potential errors

class UpdateTrades:
    def __init__(self, journalCopyFilePath: str, transCopyFilePath: str, brokerage: str) -> None:
        self.journalFilePath_ = journalCopyFilePath
        self.transFilePath_ = transCopyFilePath
        self.brokerage_ = brokerage #TT for Tastytrade, S for Schwab, RH for Robinhood
    
    
    #delete unnecessary columns in transaction file
    def removeTransCol(self) -> None:
        #For tastytrade
        if self.brokerage_ == "TT":
            try:
                with open(self.transFilePath_, 'r', newlone='') as csvfileRead:
                    readFile = csv.reader(csvfileRead, delimiter=',')
                    header = next(readFile)

                    colToRemove = ["Sub Type", "Symbol", "Instrument Type", "Quantity", 
                                "Average Price", "Multiplier", "Underling", "Order",
                                "Currency"]
                    
                    #Get the indices of columns to delete
                    deleteIndices = []
                    for colName in colToRemove:
                        deleteIndices.append(header.index(colName))
                    
                    newTransFilePath = "new"+ self.transFilePath_

                    #Iterate over rows and exclude the specified columns
                    with open(newTransFilePath, 'w', newline='') as newTransFile:
                        writer = csv.writer(newTransFile)

                        #Write the first row of the new csv trans file
                        for idx in range(len(header)):
                            if idx not in deleteIndices:
                                writer.writerow([header[idx]])

                        #Write the remaining rows
                        for row in readFile:
                            for idx in range(len(row)):
                                if idx not in deleteIndices:
                                    writer.writerow([row[idx]])

            except FileNotFoundError:
                print("File Not Found While Removing Trans Cols")
        #For Schwab
        elif self.brokerage_ == "S":
            pass
        #For Robinhood
        elif self.brokerage_ == "RH":
            pass

    # Traverse journal csv file and update dict object with open trades
    # Return dictionary when traversing is completed
    def storeOpenTrades(self) -> dict:
        openTrades = {}
        return openTrades