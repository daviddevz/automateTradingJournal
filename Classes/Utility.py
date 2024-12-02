
from datetime import datetime
class Utility:
    def __init__(self) -> None:
        pass

    # Convert Date/Time Format to Date and return a dict with update date
    # YYYY-MM-DDTHH:MM:SSZ to YYYY-MM-DD example 2024-11-07T11:40:48-0600 to 2024-11-07
    @staticmethod
    def dateTimeToDate(dictVar: dict, key: str) -> dict:
        # Loop that goes through each date and splice out the neccessary files
        for idx in range(len(dictVar[key])):
            oldValue = dictVar[key][idx]
            dictVar[key][idx] = oldValue[:oldValue.index('T')]
        return dictVar
    
    # Splice trade description based on trade action
    # For 'SELL_TO_CLOSE' or 'SELL_TO_OPEN', convert Sold 1 SMH 11/15/24 Put 220.00 @ 0.06 to SMH 11/15/24 Put 220.00
    # For 'BUY_TO_CLOSE' or 'BUY_TO_OPEN', convert Bought 1 SMH 11/15/24 Put 220.00 @ 0.06 to SMH 11/15/24 Put 220.00
    @staticmethod
    def spliceTradeDes(tradeDescription, tradeAction) -> str:
        # +5 skips  "SOLD # SPY..." to # SPY
        if tradeAction == 'SELL_TO_CLOSE' or tradeAction == 'SELL_TO_OPEN':
            return tradeDescription[tradeDescription.index('Sold') +5 : tradeDescription.index('@') -1]
        
        # +7 skips  "BOUGHT # SPY..." to # SPY
        elif tradeAction == 'BUY_TO_CLOSE' or tradeAction == 'BUY_TO_OPEN':
            return tradeDescription[tradeDescription.index('Bought') +7 : tradeDescription.index('@') -1]
        
    # Convert "MMM DD YYYY" to "YYYY-MM-DD"
    @staticmethod
    def wordDateToNumDate(dateStr: str) -> str:
        dateTimeObj = datetime.strptime(dateStr, "%b %d %Y")
        return dateTimeObj.strftime("%Y-%m-%d")
    
    # Convert "YYYY-MM-DD" to "MMM DD YYY"
    @staticmethod
    def numDateToWordDate(dateStr: str) -> str:
        dateTimeObj = datetime.strptime(dateStr, "%Y-%m-%d")
        return dateTimeObj.strftime("%b %d %Y")
    
    # Determines if compare date is greater than or equal to  initial date
    @staticmethod
    def isDateGreaterEqual(initialDate: str, compareDate: str) -> bool:
        initialDateObj = datetime.strptime(initialDate, "%Y-%m-%d")
        compareDateObj = datetime.strptime(compareDate, "%Y-%m-%d")
        return compareDateObj >= initialDateObj
    
    # Determines if compare date is greater than initial date
    @staticmethod
    def isDateGreater(initialDate: str, compareDate: str) -> bool:
        initialDateObj = datetime.strptime(initialDate, "%Y-%m-%d")
        compareDateObj = datetime.strptime(compareDate, "%Y-%m-%d")
        return compareDateObj > initialDateObj
    
    # Determines if compare date is equal to initial date
    @staticmethod
    def isEqual(initialDate: str, compareDate: str) -> bool:
        initialDateObj = datetime.strptime(initialDate, "%Y-%m-%d")
        compareDateObj = datetime.strptime(compareDate, "%Y-%m-%d")
        return compareDateObj == initialDateObj
    
    # Function to get the ticker from tradesTransDict and openTradesJournDict
    def getTicker(tradesTransDict: dict, openTradesJournDict: dict, tradeIdx: int, dictVar: str, transTradeIdx: int) -> str:
        if dictVar == 'tradesTransDict':
            ticker = tradesTransDict["Root Symbol"][transTradeIdx]
            return ticker
        
        elif dictVar == 'openTradesJournDict':
            firstIdx = openTradesJournDict["Trade Description"][tradeIdx].index(' ')
            secondIdx = openTradesJournDict["Trade Description"][tradeIdx].index(' ', firstIdx + 1)
            thirdIdx = openTradesJournDict["Trade Description"][tradeIdx].index(' ', secondIdx + 1)

            # Check for futures ticker
            if openTradesJournDict["Trade Description"][tradeIdx][secondIdx + 1] == '/':
                forthIdx = openTradesJournDict["Trade Description"][tradeIdx].index(' ', thirdIdx + 1)
                ticker = openTradesJournDict["Trade Description"][tradeIdx][secondIdx + 1:forthIdx]
                return ticker
            
            else:
                ticker = openTradesJournDict["Trade Description"][tradeIdx][secondIdx + 1:thirdIdx]
                return ticker
    
    # Remove specific character in string object
    @staticmethod
    def removeChar(strObj: str, character: str) -> str:
        print("strObj: ", strObj)
        strIdx = strObj.index(character)

        # Check if character is the first element in str obj
        if strIdx == 0:
            return strObj[strIdx +1:]
        
        # Check if character is the last element in str obj
        elif strIdx == len(strObj) -1:
            return strObj[:strIdx]
        else:
            return strObj[:strIdx] + strObj[strIdx +1:]