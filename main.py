from myModules import myModules

def main() -> None:
    journalFile = "csvfiles/Journal.csv"
    transactionFile = "csvfiles/Transactions.csv"
    colToRemove = ["Sub Type", "Symbol", "Instrument Type", "Quantity", 
                    "Average Price", "Multiplier", "Underling", "Order",
                    "Currency", "Type", "Strike Price", "Call or Put", "Order #"]
    
    
    csvFilesJorn = myModules.CSVFileHandling(journalFile)
    csvFilesJorn.createCopy()
    csvDictJourn = csvFilesJorn.createCSVDict(False)
    #print(csvDictJourn)
    csvFilesJorn.rewriteCopy(csvDictJourn)

    csvFilesTrans = myModules.CSVFileHandling(transactionFile, colToRemove)
    csvFilesTrans.createCopy()
    csvDictTrans = csvFilesTrans.createCSVDict(True)
    #print(csvDictTrans)
    csvFilesTrans.rewriteCopy(csvDictTrans)

    updateJourn = myModules.UpdateTrades(csvDictJourn, csvDictTrans)
    openTradesJournDict = updateJourn.getOpenTrades()
    #print(openTradesJournDict)

    #print(updateJourn.numDateToWordDate("2020-9-23"))
   
    updatedJournDict = updateJourn.updateJournDict(openTradesJournDict)
    #print(openTradesJournDict)

if __name__ == "__main__":
    main()