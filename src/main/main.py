import sys
sys.path.insert(0, '../TradeTransactionsSort')

from src.trade_sort.csv_handling import CSVHandling
from src.trade_sort.trade_updater import TradeUpdater
from tests.test_python.run_tests import RunTests

# index 0 = Journal csv, index 1 = Transactions csv
FILE_PATH = ["csv_files/Journal.csv", "csv_files/Transactions.csv"]

COL_TO_REMOVE = ["Sub Type", "Symbol", "Instrument Type", "Quantity",
    "Average Price", "Multiplier", "Underling", "Order",
    "Currency", "Type", "Strike Price", "Call or Put", "Order #"]

def main(file_path: list, col_to_remove: list) -> None:
    journal_path = file_path[0] 
    transaction_path = file_path[1]
    
    journal = CSVHandling(journal_path)
    journal.create_copy()
    journal_dict = journal.create_dict()    

    transaction = CSVHandling(transaction_path, col_to_remove)
    transaction.create_copy()
    transaction_dict = transaction.create_dict()
    #transaction.dict_to_csv(transaction_dict)

    update_journal = TradeUpdater(journal_dict, transaction_dict)
    update_journ_dict = update_journal.update_trades()
    journal.dict_to_csv(update_journ_dict)



if __name__ == "__main__":
    tests = RunTests()
    tests.run_tests()
    main(FILE_PATH, COL_TO_REMOVE)

