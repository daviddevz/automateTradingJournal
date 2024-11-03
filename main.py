from myModules import myModules

def main() -> None:
    journalFile = "csvfiles/TT Margin V.1.2 2024.csv"
    transactionFile = "csvfiles/TastytradeTransactions.csv"
    
    try:
        csvFiles = myModules.CSVFileHandling(journalFile, transactionFile)
        
        copyJournalFile = csvFiles.createCopy()
        print(copyJournalFile)

        refTransFile = csvFiles.createRef()
        #print(refTransFile)
    except Exception as ex:
        print(f"Error creating CSVFileHandling instance: {ex}")
        #return

if __name__ == "__main__":
    main()