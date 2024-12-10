from src.trade_sort.utility import Utility
from src.trade_sort.trade_validator import TradeValidator
from src.trade_sort.trade_progress import TradeProgress

class JournalTradeValidator(TradeValidator):
    def __init__(self, journal_dict: dict, transaction_dict: dict) -> None:
        super().__init__(journal_dict, transaction_dict)

        self.journal_trade_idx: int = None
        self.transaction_trade_idx: int = None
        self.trade_exist_flag: bool = False
    
    def is_trade_multi_leg(self, trade_description: str, transaction_trade_idx: int) -> bool:
        (self.trade_exist_flag, self.journal_trade_idx) = self.find_trade(trade_description)
        self.transaction_trade_idx = transaction_trade_idx

        transaction_date: str = self.transaction_dict_['Date'][self.transaction_trade_idx]
        transaction_date = Utility.num_date_to_word_date(transaction_date)
        journal_entry_date: str = self.journal_dict_["Entry Date"][self.journal_trade_idx]

        transaction_exp_date: str = TradeProgress.get_expiration_date(self.transaction_dict_,
                                                                None,self.transaction_trade_idx)
        transaction_exp_date = Utility.num_date_to_word_date(transaction_exp_date)
        journal_expiration_date: str = TradeProgress.get_expiration_date(None, self.journal_dict_,
                                                                 self.journal_trade_idx)
        
        transaction_ticker: str = TradeProgress.get_ticker(self.transaction_dict_, None,
                                                                 self.transaction_trade_idx)
        journal_ticker: str = TradeProgress.get_ticker(None, self.journal_dict_,
                                                                 self.journal_trade_idx)
        
        if (self.trade_exist_flag == False
            and Utility.is_date_equal(journal_entry_date, transaction_date)
            and Utility.is_date_equal(journal_expiration_date, transaction_exp_date)
            and journal_ticker == transaction_ticker):
            return True
        
        else:
            return False
    
    def trade_exists(self, multi_leg: bool) -> bool:
        if self.trade_exist_flag == True and multi_leg == False:
            return True
        
        else:
            # Trade exists but the remaining legs are not added to journal
            return False
    
    def get_journal_trade_idx(self) -> int:
        return self.journal_trade_idx
    
    # Returns tuple of trade_exist_flag and trade_idx
    def find_trade(self, trade_description: str) -> tuple[bool, int]:
        for idx in range(len(self.journal_dict_["Trade Description"])):
            shortened_trade_description = super().splice_trade_description(trade_description)

            if shortened_trade_description in self.journal_dict_["Trade Description"][idx]:
                return(True, idx)
            
            else:
                return(False, None)
            