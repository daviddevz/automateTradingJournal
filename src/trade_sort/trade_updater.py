import copy
from src.trade_sort.utility import Utility
from src.trade_sort.journal_trade_validator import JournalTradeValidator
from src.trade_sort.trade_progress import TradeProgress

class TradeUpdater:
    def __init__(self, journal_dict: dict, transaction_dict: dict) -> None:
        self.journal_dict_ = journal_dict
        self.transaction_dict_ = transaction_dict

        # Updated in update_trades method
        self.journal_trade_idx: int
        self.transaction_trade_idx: int
        self.multi_leg_flag: bool = False
        self.new_trade_flag: bool = False

        # Depend on self.journal_trade_idx or self.transaction_trade_idx
        # Updated in add_trade_to_journal or update_trade_in_journal method
        self.entry_date: str
        self.exit_date: str
        self.trade_des: str
        self.open_price: str 
        self.close_price: str 
        self.comm_fees: str 
        self.pL: str

        # Initialize composite classes
        self.trade_progress = TradeProgress(self.journal_dict_, self.transaction_dict_)
        self.trade_validator = JournalTradeValidator(self.journal_dict_, self.transaction_dict_)

   
    
    """ add_trade reqire: 'Entry Date': "MMM DD YYYY", "Trade Description": 'x', 
    "Open Price": '$x.xx', "Comm & Fees": '$x.xx'"""
    def add_trade_to_journal(self) -> None:
        self.entry_date = self.update_entry_date()
        self.trade_des = self.update_trade_des()
        self.open_price = self.update_open_price()
        self.comm_fees = self.update_comm_fees()

        # For single leg trades
        if self.multi_leg_flag == False:
            self.journal_dict_["Entry Date"].append(self.entry_date)
            self.journal_dict_["Trade Description"].append(self.trade_des)
            self.journal_dict_["Open Price"].append(self.open_price)
            self.journal_dict_["Comm & Fees"].append(self.comm_fees)

            self.trade_progress.add_single_leg_trade(self.journal_dict_, self.transaction_trade_idx)
            
        # For multi leg trades
        elif self.multi_leg_flag == True:
            #self.journal_dict_["Entry Date"][self.journal_trade_idx] = self.entry_date
            self.journal_dict_["Trade Description"][self.journal_trade_idx] = self.trade_des
            self.journal_dict_["Open Price"][self.journal_trade_idx] = self.open_price
            self.journal_dict_["Comm & Fees"][self.journal_trade_idx] = self.comm_fees

            self.trade_progress.add_multi_leg_trade(self.journal_dict_, self.journal_trade_idx)

    
    """ update_trade reqire: 'Exit Date': "MMM DD YYYY", "Close Price": '$x.xx'
    "Progress": 'xxxx', "Comm & Fees": '$x.xx', "P/L": '$x.xx'"""
    def update_trade_in_journal(self) -> None:
        self.exit_date = self.update_exit_date()
        self.close_price = self.update_close_price()
        progress = self.update_progress()
        self.comm_fees = self.update_comm_fees()
        self.pL = self.update_pL()

        self.journal_dict_["Exit Date"][self.journal_trade_idx] = self.exit_date
        self.journal_dict_["Close Price"][self.journal_trade_idx] = self.close_price
        self.journal_dict_["Progress"][self.journal_trade_idx] = progress
        self.journal_dict_["Comm & Fees"][self.journal_trade_idx] = self.comm_fees
        self.journal_dict_["P/L"][self.journal_trade_idx] = self.pL

        print(f"self.journal_dict_: {self.journal_dict_} Journal trade idx: {self.journal_trade_idx}")
        self.trade_progress.close_trade(self.journal_dict_, self.journal_trade_idx)
    
    def update_entry_date(self) -> str:
        date: str = Utility.num_date_to_word_date(self.transaction_dict_['Date']
                                         [self.transaction_trade_idx])
        return date

    def update_exit_date(self) -> str:
        date: str = Utility.word_date_to_num_date(self.journal_dict_["Exit Date"]
                                                    [self.journal_trade_idx])
        date_compare = Utility.is_date_greater(date, self.transaction_dict_['Date']
                                            [self.transaction_trade_idx])
        
        if date_compare == True:
            date: str = Utility.num_date_to_word_date(self.transaction_dict_['Date']
                                             [self.transaction_trade_idx])
            return date
        
        else:
            return self.journal_dict_["Exit Date"][self.journal_trade_idx]
        


    def update_trade_des(self) -> str:
        return self.transaction_dict_['Description'][self.transaction_trade_idx]

    def update_open_price(self) -> str:
        if self.multi_leg_flag == True:
            old_price: str = self.journal_dict_["Open Price"][self.journal_trade_idx]
            new_price: float = float(Utility.remove_char(old_price, '$'))
            + float(self.transaction_dict_['Value'][self.transaction_trade_idx])
            return Utility.add_char(str(new_price), '$', 0)
        
        else:
            price: str = Utility.add_char(self.transaction_dict_['Value']
                                         [self.transaction_trade_idx], '$', 0)
            return price
        
    def update_close_price(self) -> str:
        old_price: str = self.journal_dict_["Close Price"][self.journal_trade_idx]
        new_price: float = float(Utility.remove_char(old_price, '$'))
        + float(self.transaction_dict_['Value'][self.transaction_trade_idx])
        return Utility.add_char(str(new_price), '$', 0)

    def update_progress(self) -> str:
        return self.trade_progress.get_progress(self.journal_trade_idx)

    def update_comm_fees(self) -> str:
        if self.new_trade_flag == True and self.multi_leg_flag == False:
            # Update comm & fees for opening trades
            comm_fees: str = Utility.add_char(self.transaction_dict_['Fees']
                                            [self.transaction_trade_idx], '$', 0)
            return comm_fees
        
        else:
            # Update comm & fees for closing trades and multi leg trades
            old_comm_fees: str = self.journal_dict_["Comm & Fees"][self.journal_trade_idx]
            new_comm_fees: float = float(Utility.remove_char(old_comm_fees, '$'))
            + float(self.transaction_dict_['Fees'][self.transaction_trade_idx])
            return Utility.add_char(str(new_comm_fees), '$', 0)

    def update_pL(self) -> str:
        old_open_price: str = self.journal_dict_["Open Price"][self.journal_trade_idx]
        old_close_price: str = self.journal_dict_["Close Price"][self.journal_trade_idx]
        new_pL_price: float = float(Utility.remove_char(old_open_price, '$'))
        + float(Utility.remove_char(old_close_price, '$'))
        return Utility.add_char(str(new_pL_price), '$', 0)

    def update_trades(self) -> dict:   
        for idx in range(len(self.transaction_dict_['Description']) -1, -1, -1):
            trade_description: str = self.transaction_dict_['Description'][idx]
            self.multi_leg_flag = self.trade_validator.is_trade_multi_leg(trade_description, idx)
            self.transaction_trade_idx = idx

            print(f"Multi leg flag: {self.multi_leg_flag}")

            if self.trade_validator.trade_exists(self.multi_leg_flag) == True:
                print("True in trade_validator")
                self.journal_trade_idx = self.trade_validator.get_journal_trade_idx()
                self.trade_progress.update_progress(self.journal_trade_idx)
                self.new_trade_flag = False
                self.update_trade_in_journal()
            
            elif self.multi_leg_flag == True:
                self.journal_trade_idx = self.trade_validator.get_journal_trade_idx()
                self.trade_progress.update_progress(self.journal_trade_idx)
                self.new_trade_flag = True
                self.add_trade_to_journal()
            
            else:
                self.new_trade_flag = True
                self.add_trade_to_journal()

        return self.journal_dict_   
    


    
