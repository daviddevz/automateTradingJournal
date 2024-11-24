import copy
from datetime import datetime

class UpdateTrades:
    def __init__(self, journalDict: dict, transDict: dict) -> None:
        self.journalDict_ = journalDict
        self.transDict_ = transDict
        self.tradeIdx = None
    
    # Determine opened trades from the journal dict and return an opened trades dict
    def getOpenTrades(self) -> dict:
        journDictCopy = copy.deepcopy(self.journalDict_) # Deep copy

        # Delete values with closed trade progress in reverse order
        for idx in range(len(journDictCopy['Progress']) -1, -1, -1):
            if journDictCopy['Progress'][idx] == 'Close':
                for key in journDictCopy.keys():
                    journDictCopy[key].pop(idx)
        return journDictCopy
    
    # Splice trade description based on trade action
    def spliceTradeDes(self, tradeDescription, tradeAction) -> str:
        print("Trade description in splice ", tradeDescription)
        # +5 skips  "SOLD # SPY..." to # SPY
        if tradeAction == 'SELL_TO_CLOSE' or tradeAction == 'SELL_TO_OPEN':
            return tradeDescription[tradeDescription.index('Sold') +5 : tradeDescription.index('@') -1]
        
        # +7 skips  "BOUGHT # SPY..." to # SPY
        elif tradeAction == 'BUY_TO_CLOSE' or tradeAction == 'BUY_TO_OPEN':
            return tradeDescription[tradeDescription.index('Bought') +7 : tradeDescription.index('@') -1]
    
    # Convert "MMM DD YYYY" to "YYYY-MM-DD"
    def wordDateToNumDate(self, dateStr: str) -> str:
        dateTimeObj = datetime.strptime(dateStr, "%b %d %Y")
        return dateTimeObj.strftime("%Y-%m-%d")

    # Convert "YYYY-MM-DD" to "MMM DD YYY"
    def numDateToWordDate(self, dateStr: str) -> str:
        dateTimeObj = datetime.strptime(dateStr, "%Y-%m-%d")
        return dateTimeObj.strftime("%b %d %Y")
    
    # Determines if compare date is greater than or equal to  initial date
    def isDateGreaterEqual(self, initialDate: str, compareDate: str) -> bool:
        initialDateObj = datetime.strptime(initialDate, "%Y-%m-%d")
        compareDateObj = datetime.strptime(compareDate, "%Y-%m-%d")
        return compareDateObj >= initialDateObj
    
    # Determines if compare date is greater than initial date
    def isDateGreater(self, initialDate: str, compareDate: str) -> bool:
        initialDateObj = datetime.strptime(initialDate, "%Y-%m-%d")
        compareDateObj = datetime.strptime(compareDate, "%Y-%m-%d")
        return compareDateObj > initialDateObj
    
    # Determines if compare date is equal to initial date
    def isEqual(self, initialDate: str, compareDate: str) -> bool:
        initialDateObj = datetime.strptime(initialDate, "%Y-%m-%d")
        compareDateObj = datetime.strptime(compareDate, "%Y-%m-%d")
        return compareDateObj == initialDateObj
    
    # Search to verify opened trades in openTradesJournDict
    # Return tuple of tradeExit/skipTrade boolean var and tradeIdx var
    def validateTrades(self, openTradesJournDict: dict, tradeDes: str, tradeDate: str) -> tuple:
        tradeExist = False # True: trade exist and False trade does not exit
        skipTrade = False # True: add new trade
        
        # Performs linear search in openTradesJournDict to search for the trade
        # Returns (True, False): trade exit (closed trades) and should be updated in openTradeJournDict
        # Returns (False, False): trade doesn't exit (new trades) and should be added in openTradesJournDict
        # Returns (False, True) trade doesn't exist (old trades) and should not be added in openTradesJornDict
        
        # JournDict increasing date order
        # TransDict decreasing date order
        for idx in range(len(openTradesJournDict["Entry Date"])):
            # Compare trade description to trade description in openTradeJournDict
            if (self.isDateGreaterEqual(self.wordDateToNumDate(openTradesJournDict["Entry Date"][idx]), tradeDate)
                and tradeDes in openTradesJournDict["Trade Description"][idx]):
                tradeIdx = idx # Index in list of value of key in openTradesJournDict
                tradeExist = True # Flag that trade exist in openTradesJournDict
                return (tradeExist, skipTrade, tradeIdx)
            
            # No match in openTradesJournDict but trade is within time constraint, so it should be a new trade
            elif self.isDateGreaterEqual(self.wordDateToNumDate(openTradesJournDict["Entry Date"][idx]), tradeDate):
                tradeIdx = None
                return (tradeExist, skipTrade, tradeIdx)
            
            # No match in openTradesJournDict but trade is outside time constraint, so it is an old trade
            tradeIdx = None
            skipTrade = True
            return (tradeExist, skipTrade, tradeIdx)

    # Performs binary search to verify multilegged trade and return tuple of int tradeIdx and boolean addTradeLine variable 
    def validateMultlgTrades(self, openTradesJourDict: dict, tradesTransDict: dict, tradeDes: str) -> int:
        tradeEntryDate = tradesTransDict['Date'][self.tradeIdx]
        tradeEntryDate = self.numDateToWordDate(tradeEntryDate) # Convert to word date

        low = 0
        high = len(openTradesJourDict['Entry Date']) - 1

        while low <= high:
            mid = (low + high) // 2
            midDate = openTradesJourDict['Entry Date'][mid]
            midDate = self.wordDateToNumDate(midDate) # Convert to num date

            if self.isEqual(midDate, tradeEntryDate):
                pass
            if self.isDateGreater(midDate, tradeEntryDate):
                high = mid - 1
            else:
                high = 

    # Determine how trades are added/updated in openTradesJournDict
    def addTradesPrecursor(self, openTradesjournDict: dict, tradesTransDict: dict, tradeDes: str, tradeDate: str, tradeAction: str) -> None:
        # Return index in list of value of key in openTradesJournDict and bool value to for tradeExit and skipTrade
        precursorResult = self.validateTrades(openTradesjournDict, tradeDes, tradeDate)

        # Condition that determines how journDict is updated
        # True: updates exit date, close price, comm & fees
        if precursorResult == (True, False):
            self.addTrades(openTradesjournDict, tradesTransDict, tradeDes, precursorResult, tradeAction)

        # True: updates entry date, exit date, trade description, open price, close price, comm & fees
        elif precursorResult[:2] == (False, False):
            self.addTrades(openTradesjournDict, tradesTransDict, tradeDes, precursorResult, tradeAction)

    # Remove specific character in string object
    def removeChar(self, strObj: str, character: str) -> str:
        strIdx = strObj.index(character)

        # Check if character is the first element in str obj
        if strIdx == 0:
            return strObj[strIdx +1:]
        
        # Check if character is the last element in str obj
        elif strIdx == len(strObj) -1:
            return strObj[:strIdx]
        else:
            return strObj[:strIdx] + strObj[strIdx +1:]
    
    # Add specific character to string object in a specific index
    def addChar(self, strObj: str, character: str, idx: int) -> str:
        newStrObj = strObj[:idx] + character + strObj[idx:]
        return newStrObj

    
    # Add new trades chronologically based on entry dates in the journal dictionary
    # Update exit date, close price, comm & fees in the journal dictionary
    # Closed trades: updates exit date, close price, progress, comm & fees
    # New trades: updates entry date, exit date, trade description, open price, close price, progress, comm & fees
    def addTrades(self, openTradesJournDict: dict, tradesTransDict: dict, tradeDes: str, precusorResult: tuple, tradeAction) -> None:
        tradeExist = precusorResult[0] # Flag to determine if trade exist in openTradesJournDict. True: trade exist and False trade does not exit
        tradeIdx = precusorResult[2] # Index in list of value of key in openTradesJournDict
        if tradeExist:
            # Exit date
            openTradesJournDict["Exit Date"][tradeIdx] = self.numDateToWordDate(tradesTransDict['Date'][tradeIdx])
            
            # Close price
            # Check if the close price value is empty before performing string to float operation
            if openTradesJournDict["Close Price"][tradeIdx] == '':
                openTradesJournDict["Close Price"][tradeIdx] = f"{float(tradesTransDict['Value'][tradeIdx])}"

                # Add $ since trans dict doesn't add $
                openTradesJournDict["Close Price"][tradeIdx] = self.addChar(openTradesJournDict["Close Price"][tradeIdx], '$', 0) 
            else:
                openTradesJournDict["Close Price"][tradeIdx] = f"{float(self.removeChar(openTradesJournDict["Close Price"][tradeIdx], '$'))
                                                                       + float(tradesTransDict['Value'][tradeIdx])}"

                # Check if close price is negative or positive
                if openTradesJournDict["Close Price"][tradeIdx][0] == '-':
                    openTradesJournDict["Close Price"][tradeIdx] = self.addChar(openTradesJournDict["Close Price"][tradeIdx], '$', 1)
                    print("Close Price -: ", openTradesJournDict["Close Price"][tradeIdx])
                else:
                    openTradesJournDict["Close Price"][tradeIdx] = self.addChar(openTradesJournDict["Close Price"][tradeIdx], '$', 0)
                    print("Close Price +: ", openTradesJournDict["Close Price"][tradeIdx])

            # Comm & fees
            # Check if the comm & fees value is empty before performing string to float operation
            if openTradesJournDict["Comm & Fees"][tradeIdx] == '':
                openTradesJournDict["Comm & Fees"][tradeIdx] = f"{float(tradesTransDict['Commissions'][tradeIdx]) + 
                                                                    float(tradesTransDict['Fees'][tradeIdx])}"
                
                # Add $ since trans dict doesn't add $
                openTradesJournDict["Comm & Fees"][tradeIdx] = self.addChar(openTradesJournDict["Comm & Fees"][tradeIdx], '$', 0) 
                print("Comm & Fees empty", openTradesJournDict["Comm & Fees"][tradeIdx])
            else:
                openTradesJournDict["Comm & Fees"][tradeIdx] = f"{float(self.removeChar(openTradesJournDict["Comm & Fees"][tradeIdx], '$'))
                                                                    + float(tradesTransDict['Commissions'][tradeIdx])
                                                                    + float(tradesTransDict['Fees'][tradeIdx])}"
                
                # Comm & Fees is always negative, so idx at 1
                openTradesJournDict["Comm & Fees"][tradeIdx] = self.addChar(openTradesJournDict["Comm & Fees"][tradeIdx], '$', 1) 
                print("Comm & Fees not empty", openTradesJournDict["Comm & Fees"][tradeIdx])
        else:
            # Entry date 
            validateResult = self.validateMultlgTrades(openTradesJournDict, tradesTransDict, tradeDes)
            tradeIdx = validateResult[0] # Index in list of value of key in openTradesJournDict
            addTradeLine = validateResult[1] # Flag to determine if trade line needs to be added
            pass
        self.journalDict_ = openTradesJournDict
    
    # Merges updates done on openTradeJournDict to the JournalDict that contain closed trades
    def mergeOpenTradeJournDictToJournalDict(openTradesjournDict) -> None:
        pass

    # Search for new trades and closed trades from the transaction dictionary
    # Update the journal dictionary and return dictionary.
    def updateJournDict(self, openTradesjournDict: dict) -> None:
        transDictCopy = copy.deepcopy(self.transDict_) # Deep copy
        tradeDes = '' # Trade description

        # Traverse action key in transactional dict  in reverse order, validate and update journDict
        for idx in range(len(transDictCopy['Action']) -1, -1, -1):
            tradeDate = transDictCopy['Date'][idx]
            tradeAction = transDictCopy['Action'][idx]
            self.tradeIdx = idx # Trade index in trans dict

            if tradeAction == 'SELL_TO_CLOSE':
                tradeDes = self.spliceTradeDes(transDictCopy['Description'][idx], 'SELL_TO_CLOSE')
                
                self.addTradesPrecursor(openTradesjournDict, transDictCopy, tradeDes, tradeDate, tradeAction)

            elif tradeAction == 'BUY_TO_CLOSE':
                tradeDes = self.spliceTradeDes(transDictCopy['Description'][idx], 'BUY_TO_CLOSE')

                self.addTradesPrecursor(openTradesjournDict, transDictCopy, tradeDes, tradeDate, tradeAction)

            elif tradeAction == 'SELL_TO_OPEN':
                tradeDes = self.spliceTradeDes(transDictCopy['Description'][idx], 'SELL_TO_OPEN')
                
                self.addTradesPrecursor(openTradesjournDict, transDictCopy, tradeDes, tradeDate, tradeAction)

            elif tradeAction == 'BUY_TO_OPEN':
                tradeDes = self.spliceTradeDes(transDictCopy['Description'][idx], 'BUY_TO_OPEN')
                
                self.addTradesPrecursor(openTradesjournDict, transDictCopy, tradeDes, tradeDate, tradeAction)
        
        self.mergeOpenTradeJournDictToJournalDict(openTradesjournDict)
        return self.journalDict_