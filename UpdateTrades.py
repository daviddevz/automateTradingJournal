import copy

class UpdateTrades:
    def __init__(self, journalDict: dict, transDict: dict) -> None:
        self.journalDict_ = journalDict
        self.transDict_ = transDict
    
    # Determine opened trades from the journal dict and return an opened trades dict
    def getOpenTrades(self) -> dict:
        dictCopy = copy.deepcopy(self.journalDict_) # Deep copy

        # Delete values with closed trade progress in reverse order
        for idx in range(len(dictCopy['Progress']) -1, -1, -1):
            if dictCopy['Progress'][idx] == 'Close':
                for key in dictCopy.keys():
                    dictCopy[key].pop(idx)
        return dictCopy
    
    # Search for new trades and closed trades from the transaction dictionary
    # Return either new trade or closed trades dictionary.
    def searchTrades(self, tradeType: str, openTradesjournDict: dict) -> dict:
        if tradeType == 'Closed':
            pass
        elif tradeType == 'New':
            pass
    
    # Verify closed trade
    def validateTrades(self, openTradesjournDict: dict) -> bool:
        pass
    
    # Add new trades chronologically based on entry dates in the journal dictionary
    # Update exit date, close price, progress, comm & fees in the journal dictionary
    def addTrades(self, openTradesJournDict: dict, tradesTransDict: dict, tradeType: str) -> None:
        self.journalDict_ = openTradesJournDict

    # Return the journal dictionary.
    def returnJournalDict(self) -> dict:
        return self.journalDict_
