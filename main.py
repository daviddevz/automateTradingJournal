import MyModules

def main() -> None:
    journalFile = "CSVFiles/Journal.csv"
    transactionFile = "CSVFiles/Transactions.csv"
    colToRemove = ["Sub Type", "Symbol", "Instrument Type", "Quantity", 
                    "Average Price", "Multiplier", "Underling", "Order",
                    "Currency", "Type", "Strike Price", "Call or Put", "Order #"]
    
    
    csvFilesJorn = MyModules.CSVFileHandling(journalFile)
    csvFilesJorn.createCopy()
    csvDictJourn = csvFilesJorn.createCSVDict(False)
    #print(csvDictJourn)
    csvFilesJorn.rewriteCopy(csvDictJourn)

    csvFilesTrans = MyModules.CSVFileHandling(transactionFile, colToRemove)
    csvFilesTrans.createCopy()
    csvDictTrans = csvFilesTrans.createCSVDict(True)
    #print(csvDictTrans)
    csvFilesTrans.rewriteCopy(csvDictTrans)

    updateJourn = MyModules.UpdateTrades(csvDictJourn, csvDictTrans)
    openTradesJournDict = updateJourn.getOpenTrades()
    print(openTradesJournDict)
    #print(updateJourn.initialProgressDict(openTradesJournDict))

    #print(updateJourn.numDateToWordDate("2020-9-23"))

    updatedJournDict = updateJourn.updateJournDict(openTradesJournDict)

