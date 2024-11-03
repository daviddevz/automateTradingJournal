import csv
from typing import Optional  # Import Optional for handling potential errors

class UpdateTrades:
    def __init__(self, journalCopyFilePath: str, transCopyFilePath: str, brokerage: str) -> None:
        self.journalFilePath_ = journalCopyFilePath
        self.transFilePath_ = transCopyFilePath
        self.brokerage_ = brokerage #TT for Tastytrade, S for Schwab, RH for Robinhood
    
    #delete unnecessary columns in transaction file
    def removeTransCol(self) -> None:
        try:
            with open(self.)

        except FileNotFoundError:
            print("File Not Found While Removing Trans Cols")

    # Traverse journal csv file and update dict object with open trades
    # Return dictionary when traversing is completed
    def storeOpenTrades(self) -> dict:
        openTrades = {}
        return openTrades