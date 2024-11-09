from myModules import myModules

def main() -> None:
    journalFile = "csvfiles/Journal.csv"
    transactionFile = "csvfiles/Transactions.csv"
    colToRemove = ["Sub Type", "Symbol", "Instrument Type", "Quantity", 
                    "Average Price", "Multiplier", "Underling", "Order",
                    "Currency"]
    
    try:
        csvFilesJorn = myModules.CSVFileHandling(journalFile)
        
        csvFilesJorn.createCopy()
        #csvDictJourn = csvFiles.createCSVDict()

        #print(csvDict)

        csvFilesTrans = myModules.CSVFileHandling(transactionFile, colToRemove)
        
        csvFilesTrans.createCopy()
        csvDictTrans = csvFilesTrans.createCSVDict()
        print(csvDictTrans)
        csvFilesTrans.rewriteCopy(csvDictTrans)
        
    except Exception as ex:
        print(f"Error creating CSVFileHandling instance: {ex}")
        #return

if __name__ == "__main__":
    main()