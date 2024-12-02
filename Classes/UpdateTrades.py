import copy
from datetime import datetime
from Classes.Utility import Utility

class UpdateTrades:
    def __init__(self, journalDict: dict, transDict: dict) -> None:
        self.journalDict_ = journalDict
        self.transDict_ = transDict
        self.tradeIdx = None # Trade index in trans dict
        self.progressDict = {} # Stores the progress of opened and closed trades
    
    # Initial progress dictionary run through opened trades, determine keys (root symbol, expiration date)
    # and value list of tradeIdx, number of trades open, zero for closed trades
    def initialProgressDict(self, journDict: dict) -> dict:
        progressDict = {}
        for idx in range(len(journDict['Entry Date'])):
            rootSymbol = Utility.getTicker(None, journDict, idx, 'openTradesJournDict', None)
            expDate = self.getExpDate(None, journDict, idx, 'openTradesJournDict')
            progressDict[(rootSymbol, expDate)] = [idx]

            numTradesOpen = 0 # Number of trades open
            # Loop that goes up to the second to last index to avoid index out of range
            for idx2 in range(len(journDict["Trade Description"][idx]) -1):
                if journDict["Trade Description"][idx][idx2:idx2+2] == '\r\n':
                    numTradesOpen += 1
            progressDict[(rootSymbol, expDate)].append(numTradesOpen +1)
            progressDict[(rootSymbol, expDate)].append(0)
            
        return progressDict
     
    # Determine opened trades from the journal dict and return an opened trades dict
    def getOpenTrades(self) -> dict:
        journDictCopy = copy.deepcopy(self.journalDict_) # Deep copy

        # Delete values with closed trade progress in reverse order
        for idx in range(len(journDictCopy['Progress']) -1, -1, -1):
            if journDictCopy['Progress'][idx] == 'Close':
                for key in journDictCopy.keys():
                    journDictCopy[key].pop(idx)
        self.progressDict = self.initialProgressDict(journDictCopy)
        return journDictCopy
    
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
            if (Utility.isDateGreaterEqual(Utility.wordDateToNumDate(openTradesJournDict["Entry Date"][idx]), tradeDate)
                and tradeDes in openTradesJournDict["Trade Description"][idx]):
                tradeIdx = idx # Index in list of value of key in openTradesJournDict
                tradeExist = True # Flag that trade exist in openTradesJournDict
                return (tradeExist, skipTrade, tradeIdx)
            
            # No match in openTradesJournDict but trade is within time constraint, so it should be a new trade
            elif Utility.isDateGreaterEqual(Utility.wordDateToNumDate(openTradesJournDict["Entry Date"][idx]), tradeDate):
                tradeIdx = None
                return (tradeExist, skipTrade, tradeIdx)
            
            # No match in openTradesJournDict but trade is outside time constraint, so it is an old trade
            tradeIdx = None
            skipTrade = True
            return (tradeExist, skipTrade, tradeIdx)
    
    # Function to get the expiration date from tradesTransDict
    def getExpDate(self, tradesTransDict: dict, openTradesJournDict: dict, tradeIdx: int, dictVar: str) -> str:
        if dictVar == 'tradesTransDict':
            expDate = tradesTransDict["Expiration Date"][self.tradeIdx]
            return expDate

        elif dictVar == 'openTradesJournDict':
            # Check for futures and exclude trade descriptions with no expiration date
            if '/' in openTradesJournDict["Trade Description"][tradeIdx]:
                firstIdx = openTradesJournDict["Trade Description"][tradeIdx].index('/')

                # Check for futures expiration
                if openTradesJournDict["Trade Description"][tradeIdx][firstIdx - 1] == ' ':
                    secondIdx = openTradesJournDict["Trade Description"][tradeIdx].index('/', firstIdx + 1)
                    thirdIdx = openTradesJournDict["Trade Description"][tradeIdx].index(' ', secondIdx + 1)
                    expDate = openTradesJournDict["Trade Description"][tradeIdx][secondIdx - 2:thirdIdx]
                    return expDate
                
                else:
                    secondIdx = openTradesJournDict["Trade Description"][tradeIdx].index(' ', firstIdx + 1)
                    expDate = openTradesJournDict["Trade Description"][tradeIdx][firstIdx - 2:secondIdx]
                    return expDate
    
    # Performs binary search to verify multilegged trade and return tuple of int tradeIdx and boolean addTradeLine variable 
    def validateMultlgTrades(self, openTradesJourDict: dict, tradesTransDict: dict) -> tuple:
        tradeEntryDate = tradesTransDict['Date'][self.tradeIdx] # Convert to word date
        tradeIdx = None
        addTradeLine = False

        low = 0
        high = len(openTradesJourDict['Entry Date']) - 1

        while low <= high:
            mid = (low + high) // 2
            midDate = openTradesJourDict['Entry Date'][mid]
            midDate = Utility.wordDateToNumDate(midDate) # Convert to num date

            # True if trade entry date is equal to mid date, expiration date and security are equal
            if (Utility.isEqual(midDate, tradeEntryDate) and Utility.getTicker(tradesTransDict, None, None, 'tradesTransDict', self.tradeIdx) in openTradesJourDict["Trade Description"][mid]
            and self.getExpDate(tradesTransDict, None, None, 'tradesTransDict') in openTradesJourDict["Trade Description"][mid]):
                tradeIdx = mid
                return (tradeIdx, addTradeLine)
            
            # True if trade entry date is greater than mid date
            elif Utility.isDateGreater(midDate, tradeEntryDate):
                low = mid + 1
            else:
                high = mid - 1
        
        addTradeLine = True # Trade does not exist in openTradesJournDict
        return (tradeIdx, addTradeLine)

    # Determine how trades are added/updated in openTradesJournDict
    def addTradesPrecursor(self, openTradesjournDict: dict, tradesTransDict: dict, tradeDes: str, tradeDate: str, tradeAction: str) -> None:
        # Return index in list of value of key in openTradesJournDict and bool value to for tradeExit and skipTrade
        precursorResult = self.validateTrades(openTradesjournDict, tradeDes, tradeDate)

        # Condition that determines how journDict is updated
        # True: updates exit date, close price, comm & fees
        if precursorResult[:2] == (True, False):
            self.addTrades(openTradesjournDict, tradesTransDict, precursorResult, tradeAction)

        # True: updates entry date, exit date, trade description, open price, close price, comm & fees
        elif precursorResult[:2] == (False, False):
            precursorResult = self.validateMultlgTrades(openTradesjournDict, tradesTransDict)
            self.addTrades(openTradesjournDict, tradesTransDict, precursorResult, tradeAction)    
    # Add specific character to string object in a specific index
    def addChar(self, strObj: str, character: str, idx: int) -> str:
        newStrObj = strObj[:idx] + character + strObj[idx:]
        return newStrObj

    
    # Add new trades chronologically based on entry dates in the journal dictionary
    # Update exit date, close price, comm & fees in the journal dictionary
    # Closed trades: updates exit date, close price, progress, comm & fees
    # New trades: updates entry date, exit date, trade description, open price, close price, progress, comm & fees
    def addTrades(self, openTradesJournDict: dict, tradesTransDict: dict, precusorResult: tuple, tradeAction: str) -> None:
        tradeExist = precusorResult[0] # Flag to determine if trade exist in openTradesJournDict. True: trade exist and False trade does not exit
        
        if tradeExist and type(precusorResult[0]) == bool:
            tradeIdx = precusorResult[2] # Index in list of value of key in openTradesJournDict

            # Exit date
            openTradesJournDict["Exit Date"][tradeIdx] = Utility.numDateToWordDate(tradesTransDict['Date'][self.tradeIdx])
            
            # Close price
            # Check if the close price value is empty before performing string to float operation
            if openTradesJournDict["Close Price"][tradeIdx] == '':
                openTradesJournDict["Close Price"][tradeIdx] = f"{float(tradesTransDict['Value'][self.tradeIdx])}"

                # Add $ since trans dict doesn't add $
                openTradesJournDict["Close Price"][tradeIdx] = self.addChar(openTradesJournDict["Close Price"][tradeIdx], '$', 0) 

            else:
                openTradesJournDict["Close Price"][tradeIdx] = f"{float(Utility.removeChar(openTradesJournDict["Close Price"][tradeIdx], '$'))
                                                                       + float(tradesTransDict['Value'][self.tradeIdx])}"

                # Check if close price is negative or positive
                if openTradesJournDict["Close Price"][tradeIdx][0] == '-':
                    openTradesJournDict["Close Price"][tradeIdx] = self.addChar(openTradesJournDict["Close Price"][tradeIdx], '$', 1)

                else:
                    openTradesJournDict["Close Price"][tradeIdx] = self.addChar(openTradesJournDict["Close Price"][tradeIdx], '$', 0)

            # Comm & fees
            # Check if the comm & fees value is empty before performing string to float operation
            if openTradesJournDict["Comm & Fees"][tradeIdx] == '':
                openTradesJournDict["Comm & Fees"][tradeIdx] = f"{float(tradesTransDict['Commissions'][self.tradeIdx]) + 
                                                                    float(tradesTransDict['Fees'][self.tradeIdx])}"
                
                # Add $ since trans dict doesn't add $
                openTradesJournDict["Comm & Fees"][tradeIdx] = self.addChar(openTradesJournDict["Comm & Fees"][tradeIdx], '$', 0) 

            else:
                openTradesJournDict["Comm & Fees"][tradeIdx] = f"{float(Utility.removeChar(openTradesJournDict["Comm & Fees"][tradeIdx], '$'))
                                                                    + float(tradesTransDict['Commissions'][self.tradeIdx])
                                                                    + float(tradesTransDict['Fees'][self.tradeIdx])}"
                
                # Comm & Fees is always negative, so idx at 1
                openTradesJournDict["Comm & Fees"][tradeIdx] = self.addChar(openTradesJournDict["Comm & Fees"][tradeIdx], '$', 1) 

        else:
            rootSymbol = Utility.getTicker(tradesTransDict, None, None, 'tradesTransDict', self.tradeIdx)
            expDate = self.getExpDate(tradesTransDict, None, None, 'tradesTransDict')
            #validateResult = self.validateMultlgTrades(openTradesJournDict, tradesTransDict)
            tradeIdx = precusorResult[0] # Index in list of value of key in openTradesJournDict
            addTradeLine = precusorResult[1] # Flag to determine if trade line needs to be added
            
            # tradeIdx exist and addTradeLine is False, trade is part of multilegged trade
            if tradeIdx != None and not addTradeLine:
                if tradeAction == "BUY_TO_OPEN" or tradeAction == "SELL_TO_OPEN":
                    # Entry Date and maintain earliest date
                    # True if additional trade date is less than previous entry date in journal dict
                    if not Utility.isDateGreaterEqual(Utility.wordDateToNumDate(openTradesJournDict["Entry Date"][tradeIdx]), tradesTransDict['Date'][self.tradeIdx]):
                        openTradesJournDict["Entry Date"][tradeIdx] = Utility.numDateToWordDate(tradesTransDict['Date'][self.tradeIdx])

                    elif openTradesJournDict["Entry Date"][tradeIdx] == '':
                        openTradesJournDict["Entry Date"][tradeIdx] = Utility.numDateToWordDate(tradesTransDict['Date'][self.tradeIdx])
                
                # Exit Date
                elif tradeAction == "BUY_TO_CLOSE" or tradeAction == "SELL_TO_CLOSE":
                    # True if additional trade date is greater than previous exit date in journal dict
                    if Utility.isDateGreaterEqual(openTradesJournDict["Exit Date"][tradeIdx], tradesTransDict['Date'][self.tradeIdx]):
                        openTradesJournDict["Exit Date"][tradeIdx] = Utility.numDateToWordDate(tradesTransDict['Date'][self.tradeIdx])

                    elif openTradesJournDict["Exit Date"][tradeIdx] == '':
                        openTradesJournDict["Exit Date"][tradeIdx] = Utility.numDateToWordDate(tradesTransDict['Date'][self.tradeIdx])
                
                # Trade Description
                openTradesJournDict["Trade Description"][tradeIdx] += '\r\n' + tradesTransDict['Description'][self.tradeIdx]

                # Open Price
                # Check if the open price value is empty before performing string to float operation
                if openTradesJournDict["Open Price"][tradeIdx] == '':
                    print('if ', openTradesJournDict["Open Price"][tradeIdx])
                    openTradesJournDict["Open Price"][tradeIdx] = f"{float(tradesTransDict['Value'][self.tradeIdx])}"

                    # Add $ since trans dict doesn't add $
                    openTradesJournDict["Open Price"][tradeIdx] = self.addChar(openTradesJournDict["Open Price"][tradeIdx], '$', 0) 
                    
                else:
                    print("Trade Description openTradesJournDict: ", openTradesJournDict["Trade Description"][tradeIdx])
                    print("Trade Description tradesTransDict: ", tradesTransDict['Description'][self.tradeIdx])
                    print("Open Price in else: ", openTradesJournDict["Open Price"][tradeIdx])
                    print("Value in else: ", tradesTransDict['Value'][self.tradeIdx])

                    # Check if value in tradesTransdict is negative or positive
                    if tradesTransDict['Value'][self.tradeIdx][0] == '-':
                        print("Check if value in tradesTransdict is negative or positive: ", tradesTransDict['Value'][self.tradeIdx],
                              type(tradesTransDict['Value'][self.tradeIdx]))
                        tradesTransDict['Value'][self.tradeIdx] = float(Utility.removeChar(tradesTransDict["Value"][tradeIdx], '-')) * -1

                    else:
                        tradesTransDict['Value'][self.tradeIdx] = float(tradesTransDict["Value"][tradeIdx])

                    # Check if value in openTradesJournDict is negative or positive
                    if openTradesJournDict["Open Price"][tradeIdx][0:2] == '-$':
                        openTradesJournDict["Open Price"][tradeIdx] = Utility.removeChar(tradesTransDict["Value"][tradeIdx], '-')
                        openTradesJournDict["Open Price"][tradeIdx] = float(Utility.removeChar(tradesTransDict["Value"][tradeIdx], '$'))

                    elif openTradesJournDict["Open Price"][tradeIdx][0] == '$':
                        openTradesJournDict["Open Price"][tradeIdx] = float(Utility.removeChar(tradesTransDict["Value"][tradeIdx], '$'))

                    openTradesJournDict["Open Price"][tradeIdx] = f"{openTradesJournDict["Open Price"][tradeIdx]
                                                                        + tradesTransDict['Value'][self.tradeIdx]}"
                    
                    #print("Open Price in else after calc: ", openTradesJournDict["Open Price"][tradeIdx])

                    # Check if close price is negative or positive
                    if openTradesJournDict["Open Price"][tradeIdx][0] == '-':
                        openTradesJournDict["Open Price"][tradeIdx] = self.addChar(openTradesJournDict["Open Price"][tradeIdx], '$', 1)

                    else:
                        openTradesJournDict["Open Price"][tradeIdx] = self.addChar(openTradesJournDict["Open Price"][tradeIdx], '$', 0)
                        
                
                # Close Price
                # Check if the close price value is empty before performing string to float operation
                if openTradesJournDict["Close Price"][tradeIdx] == '':
                    openTradesJournDict["Close Price"][tradeIdx] = f"{float(tradesTransDict['Value'][self.tradeIdx])}"

                    # Add $ since trans dict doesn't add $
                    openTradesJournDict["Close Price"][tradeIdx] = self.addChar(openTradesJournDict["Close Price"][tradeIdx], '$', 0) 
                else:
                    openTradesJournDict["Close Price"][tradeIdx] = f"{float(Utility.removeChar(openTradesJournDict["Close Price"][tradeIdx], '$'))
                                                                        + float(tradesTransDict['Value'][self.tradeIdx])}"

                    # Check if close price is negative or positive
                    if openTradesJournDict["Close Price"][tradeIdx][0] == '-':
                        openTradesJournDict["Close Price"][tradeIdx] = self.addChar(openTradesJournDict["Close Price"][tradeIdx], '$', 1)

                    else:
                        openTradesJournDict["Close Price"][tradeIdx] = self.addChar(openTradesJournDict["Close Price"][tradeIdx], '$', 0)

                # Comm & fees
                # Check if the comm & fees value is empty before performing string to float operation
                if openTradesJournDict["Comm & Fees"][tradeIdx] == '':
                    openTradesJournDict["Comm & Fees"][tradeIdx] = f"{float(tradesTransDict['Commissions'][self.tradeIdx]) + 
                                                                        float(tradesTransDict['Fees'][self.tradeIdx])}"
                    
                    # Add $ since trans dict doesn't add $
                    openTradesJournDict["Comm & Fees"][tradeIdx] = self.addChar(openTradesJournDict["Comm & Fees"][tradeIdx], '$', 0) 

                else:
                    openTradesJournDict["Comm & Fees"][tradeIdx] = f"{float(Utility.removeChar(openTradesJournDict["Comm & Fees"][tradeIdx], '$'))
                                                                        + float(tradesTransDict['Commissions'][self.tradeIdx])
                                                                        + float(tradesTransDict['Fees'][self.tradeIdx])}"
                    
                    # Comm & Fees is always negative, so idx at 1
                    openTradesJournDict["Comm & Fees"][tradeIdx] = self.addChar(openTradesJournDict["Comm & Fees"][tradeIdx], '$', 1)
                
                # Progress
                # ProgressDict will have key as (root symbol, expiration date) and value list of tradeIdx, number of trades open, number of trades closed
                #self.progressDict[(rootSymbol, tradesTransDict['Expiration'][self.tradeIdx])]
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
                tradeDes = Utility.spliceTradeDes(transDictCopy['Description'][idx], 'SELL_TO_CLOSE')
                
                self.addTradesPrecursor(openTradesjournDict, transDictCopy, tradeDes, tradeDate, tradeAction)

            elif tradeAction == 'BUY_TO_CLOSE':
                tradeDes = Utility.spliceTradeDes(transDictCopy['Description'][idx], 'BUY_TO_CLOSE')

                self.addTradesPrecursor(openTradesjournDict, transDictCopy, tradeDes, tradeDate, tradeAction)

            elif tradeAction == 'SELL_TO_OPEN':
                tradeDes = Utility.spliceTradeDes(transDictCopy['Description'][idx], 'SELL_TO_OPEN')
                
                self.addTradesPrecursor(openTradesjournDict, transDictCopy, tradeDes, tradeDate, tradeAction)

            elif tradeAction == 'BUY_TO_OPEN':
                tradeDes = Utility.spliceTradeDes(transDictCopy['Description'][idx], 'BUY_TO_OPEN')
    
                self.addTradesPrecursor(openTradesjournDict, transDictCopy, tradeDes, tradeDate, tradeAction)
        
        self.mergeOpenTradeJournDictToJournalDict(openTradesjournDict)
        return self.journalDict_
