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
        self.entry_date: str = ''
        self.exit_date: str = ''
        self.trade_des: str = ''
        self.open_price: str = '0.00'
        self.close_price: str = '0.00'
        self.comm_fees: str = '0.00'
        self.pL: str = '0.00'

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
            self.journal_dict_["Exit Date"].append('')
            self.journal_dict_["Close Price"].append('0.00')
            self.journal_dict_["Progress"].append('Open')
            self.journal_dict_["P/L"].append('0.00')
            self.journal_dict_["Strategies"].append('')
            self.journal_dict_["Initial Margin\r\nRequirement"].append('')

            self.journal_trade_idx = len(self.journal_dict_["Trade Description"]) - 1
            self.trade_progress.update_progress(self.journal_trade_idx, self.journal_dict_)
            self.trade_progress.add_single_leg_trade(self.journal_dict_, self.journal_trade_idx)
            
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
        #self.pL = self.update_pL()

        self.journal_dict_["Exit Date"][self.journal_trade_idx] = self.exit_date
        self.journal_dict_["Close Price"][self.journal_trade_idx] = self.close_price
        self.journal_dict_["Progress"][self.journal_trade_idx] = progress
        self.journal_dict_["Comm & Fees"][self.journal_trade_idx] = self.comm_fees
        #self.journal_dict_["P/L"][self.journal_trade_idx] = self.pL

        self.trade_progress.close_trade(self.journal_dict_, self.journal_trade_idx)
    
    def update_entry_date(self) -> str:
        date: str = Utility.num_date_to_word_date(self.transaction_dict_['Date']
                                         [self.transaction_trade_idx])
        return date

    def update_exit_date(self) -> str:
        """ date: str = Utility.word_date_to_num_date(self.journal_dict_["Exit Date"]
                                                    [self.journal_trade_idx])
        date_compare = Utility.is_date_greater(date, self.transaction_dict_['Date']
                                            [self.transaction_trade_idx]) """
        
        if self.journal_dict_["Exit Date"][self.journal_trade_idx] == '':
            date: str = Utility.num_date_to_word_date(self.transaction_dict_['Date']
                                             [self.transaction_trade_idx])
            return date
        
        elif Utility.is_date_greater(Utility.word_date_to_num_date(self.journal_dict_["Exit Date"]
                                    [self.journal_trade_idx]), 
                                    self.transaction_dict_['Date'][self.transaction_trade_idx]):
            date: str = Utility.num_date_to_word_date(self.transaction_dict_['Date']
                                             [self.transaction_trade_idx])
            return date
        
        else:
            return self.journal_dict_["Exit Date"][self.journal_trade_idx]
        


    def update_trade_des(self) -> str:
        return self.transaction_dict_['Description'][self.transaction_trade_idx]

    def update_open_price(self) -> str:
        transaction_price: str = self.transaction_dict_['Value'][self.transaction_trade_idx]
        transaction_price = Utility.remove_char(transaction_price, ['$', ','])

        if self.multi_leg_flag == True:
            old_price: str = self.journal_dict_["Open Price"][self.journal_trade_idx]
            old_price = Utility.remove_char(old_price, ['$', ','])

            new_price: float = float(old_price) + float(transaction_price)
            return str(new_price)
        
        else:
            return transaction_price
        
    def update_close_price(self) -> str:
        old_price: str = self.journal_dict_["Close Price"][self.journal_trade_idx]
        old_price = Utility.remove_char(old_price, ['$', ','])

        transaction_price: str = self.transaction_dict_['Value'][self.transaction_trade_idx]
        transaction_price = Utility.remove_char(transaction_price, ['$', ','])

        if old_price == '':
            new_price: float = float(transaction_price)
            print(f"trade des: {self.journal_dict_['Trade Description'][self.journal_trade_idx]}")
            print(f"{self.journal_trade_idx} idx: old_price if: {old_price}, transaction_price: {transaction_price}\n")
            return str(new_price)
        
        else:
            new_price: float = float(old_price) + float(transaction_price)
            print(f"trade des: {self.journal_dict_['Trade Description'][self.journal_trade_idx]}")
            print(f"{self.journal_trade_idx} idx: old_price else: {old_price}, transaction_price: {transaction_price}\n")
            return str(new_price)

    def update_progress(self) -> str:
        return self.trade_progress.get_progress(self.journal_trade_idx)

    def update_comm_fees(self) -> str:
        if self.new_trade_flag == True and self.multi_leg_flag == False:
            # Update comm & fees for opening trades
            comm_fees: str = self.transaction_dict_['Fees'][self.transaction_trade_idx]
            return comm_fees
        
        else:
            # Update comm & fees for closing trades and multi leg trades
            old_comm_fees: str = self.journal_dict_["Comm & Fees"][self.journal_trade_idx]
            old_comm_fees = Utility.remove_char(old_comm_fees, ['$', ','])

            new_comm_fees: str = self.transaction_dict_['Fees'][self.transaction_trade_idx]
            new_comm_fees = Utility.remove_char(new_comm_fees, ['$', ','])

            final_comm_fees: float = float(old_comm_fees) + float(new_comm_fees)
            return str(final_comm_fees)

    def update_pL(self) -> None:
        for idx in range(len(self.journal_dict_['P/L']) -1, -1, -1):
            open_price: str = self.journal_dict_["Open Price"][idx]
            close_price: str = self.journal_dict_["Close Price"][idx]

            open_price = Utility.remove_char(open_price, ['$', ','])
            close_price = Utility.remove_char(close_price, ['$', ','])

            comm_fees: str = self.journal_dict_["Comm & Fees"][idx]
            comm_fees = Utility.remove_char(comm_fees, ['$', ','])

            if open_price == '' and close_price != '':
                pL_value: float = float(close_price) + float(comm_fees)
                self.journal_dict_['P/L'][idx] = str(pL_value)
            
            elif open_price != '' and close_price == '':
                pL_value: float = float(open_price) + float(comm_fees)
                self.journal_dict_['P/L'][idx] = str(pL_value)
            
            elif open_price == '' and close_price == '':
                self.journal_dict_['P/L'][idx] = str('0.00') + float(comm_fees)
            
            else:
                pL_value: float = float(open_price) + float(close_price) + float(comm_fees)
                self.journal_dict_['P/L'][idx] = str(pL_value)

    def update_trades(self) -> dict:   
        for idx in range(len(self.transaction_dict_['Description']) -1, -1, -1):
            trade_description: str = self.transaction_dict_['Description'][idx]
            self.multi_leg_flag = self.trade_validator.is_trade_multi_leg(trade_description, idx)
            self.transaction_trade_idx = idx

            if self.trade_validator.trade_exists(self.multi_leg_flag) == True:
                self.journal_trade_idx = self.trade_validator.get_journal_trade_idx()
                self.trade_progress.update_progress(self.journal_trade_idx, self.journal_dict_)

                if self.journal_dict_["Progress"][self.journal_trade_idx] == 'Close':
                    continue

                else:
                    self.new_trade_flag = True
                    self.update_trade_in_journal()
            
            elif self.multi_leg_flag == True:
                self.journal_trade_idx = self.trade_validator.get_journal_trade_idx()
                self.trade_progress.update_progress(self.journal_trade_idx, self.journal_dict_)
                self.new_trade_flag = True
                self.update_trade_in_journal()
            
            else:
                self.new_trade_flag = True
                self.add_trade_to_journal()
        
        self.update_pL()

        return self.journal_dict_   
    


    
