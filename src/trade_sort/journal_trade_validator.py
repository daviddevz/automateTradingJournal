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
        (self.trade_exist_flag, self.journal_trade_idx) = self.find_trade(trade_description, transaction_trade_idx)
        print(f"trade_exist_flag: {self.trade_exist_flag} journal_trade_idx: {self.journal_trade_idx}") 
        if (self.trade_exist_flag == False):
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
        print(f"journal_trade_idx in get_journal_trade_idx: {self.journal_trade_idx}")
        return self.journal_trade_idx
    
    # Returns tuple of trade_exist_flag and trade_idx
    def find_trade(self, trade_description: str, transaction_trade_idx: int) -> tuple[bool, int]:
        self.transaction_trade_idx = transaction_trade_idx

        for idx in range(len(self.journal_dict_["Trade Description"])):
            shortened_trade_description = super().splice_trade_description(trade_description)

            #print(f"journal_dict: {self.journal_dict_['Trade Description']}")
            print(f"shortened_trade_description: {shortened_trade_description}", 
                  f"journal trade description: {self.journal_dict_['Trade Description'][idx]}")
            
            # Trade exists
            if shortened_trade_description in self.journal_dict_["Trade Description"][idx]:
                return(True, idx)
            
            # Multi leg trade exists but not recorded in journal
            elif (TradeProgress.get_ticker(self.transaction_dict_, {}, self.transaction_trade_idx)
            == TradeProgress.get_ticker({}, self.journal_dict_, idx)):
                transaction_exp_date: str = TradeProgress.get_expiration_date(self.transaction_dict_,
                                                                {}, self.transaction_trade_idx)
                transaction_exp_date = Utility.num_date_to_word_date(transaction_exp_date)
                transaction_exp_date = Utility.word_date_to_num_date(transaction_exp_date)

                journal_expiration_date: str = TradeProgress.get_expiration_date({}, self.journal_dict_,
                                                                 idx)
                journal_expiration_date = Utility.num_date_to_word_date(journal_expiration_date)
                journal_expiration_date = Utility.word_date_to_num_date(journal_expiration_date)

                transaction_date: str = self.transaction_dict_['Date'][self.transaction_trade_idx]
                journal_entry_date: str = self.journal_dict_["Entry Date"][idx]
                journal_entry_date = Utility.word_date_to_num_date(journal_entry_date)
                
                if (Utility.is_date_equal(journal_expiration_date, transaction_exp_date)
                and Utility.is_date_equal(journal_entry_date, transaction_date)):
                    return(False, idx)
            
        return(False, None)
            