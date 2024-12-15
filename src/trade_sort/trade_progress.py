from src.trade_sort.utility import Utility

class TradeProgress:
    def __init__(self, journal_dict: dict, transaction_dict: dict) -> None:
        self.journal_dict_ = journal_dict
        self.trade_progress_dict: dict = {}
        self.num_trades_open: int = 0
        self.num_trades_closed: int = 0
        self.trade_progress: str = 'Open'
    
    # Get the ticker from tradesTransDict or openTradesJournDict
    # Too specific that it may not be needed under utility class
    @staticmethod
    def get_ticker(transaction_trade_dict: dict, journal_trade_dict: dict,
                   trade_idx: int) -> str:
        if len(transaction_trade_dict) > 0:
            ticker = transaction_trade_dict["Root Symbol"][trade_idx]
            return ticker
        
        elif len(journal_trade_dict) > 0:
            firstIdx = journal_trade_dict["Trade Description"][trade_idx].index(' ')
            secondIdx = journal_trade_dict["Trade Description"][trade_idx].index(' ', firstIdx + 1)
            thirdIdx = journal_trade_dict["Trade Description"][trade_idx].index(' ', secondIdx + 1)

            # Check for futures ticker (Bought 1 /MCLN4 MCON4 06/14/24 Call 81.75 @ 0.92)
            if journal_trade_dict["Trade Description"][trade_idx][secondIdx + 1] == '/':
                forthIdx = journal_trade_dict["Trade Description"][trade_idx].index(' ', thirdIdx + 1)
                ticker = journal_trade_dict["Trade Description"][trade_idx][secondIdx + 1:forthIdx]
                return ticker
            
            # Check for stock ticker (Sold 1 XLP 06/21/24 Put 69.00 @ 0.03)
            else:
                ticker = journal_trade_dict["Trade Description"][trade_idx][secondIdx + 1:thirdIdx]
                return ticker
    
    # Function to get the expiration date from transaction_trade_dict
    @staticmethod
    def get_expiration_date(transaction_trade_dict: dict, journal_trade_dict: dict,
                            trade_idx: int) -> str:
        if len(transaction_trade_dict) > 0:
            expDate = transaction_trade_dict["Expiration Date"][trade_idx]
            return expDate

        elif len(journal_trade_dict) > 0:
            # Check for futures and exclude trade descriptions with no expiration date
            if '/' in journal_trade_dict["Trade Description"][trade_idx]:
                firstIdx = journal_trade_dict["Trade Description"][trade_idx].index('/')

                # Check for futures expiration
                if journal_trade_dict["Trade Description"][trade_idx][firstIdx - 1] == ' ':
                    secondIdx = journal_trade_dict["Trade Description"][trade_idx].index('/', firstIdx + 1)
                    thirdIdx = journal_trade_dict["Trade Description"][trade_idx].index(' ', secondIdx + 1)
                    expDate = journal_trade_dict["Trade Description"][trade_idx][secondIdx - 2:thirdIdx]
                    return expDate
                
                else:
                    secondIdx = journal_trade_dict["Trade Description"][trade_idx].index(' ', firstIdx + 1)
                    expDate = journal_trade_dict["Trade Description"][trade_idx][firstIdx - 2:secondIdx]
                    return expDate

    def add_single_leg_trade(self, journal_dict_: dict, journal_trade_idx: int) -> None:
        self.journal_dict_ = journal_dict_
        self.trade_progress_dict[journal_trade_idx][2] += 1
        self.check_previous_exp_date(journal_trade_idx)

    def add_multi_leg_trade(self, journal_dict_: dict, journal_trade_idx: int) -> None:
        self.journal_dict_ = journal_dict_
        self.trade_progress_dict[journal_trade_idx][2] += 1
        self.check_previous_exp_date(journal_trade_idx)

    def close_trade(self, journal_dict_: dict, journal_trade_idx: int) -> None:
        self.journal_dict_ = journal_dict_
        self.trade_progress_dict[journal_trade_idx][3] += 1
        self.check_previous_exp_date(journal_trade_idx)

    """This function compares current trade entry date, to previous
    expiration dates. If the exp date is less than the current date,
    it checks if the trade was closed or closes it automatically.
    Esle it does nothing.
    """
    def check_previous_exp_date(self, journal_trade_idx: int) -> None:
        curren_entry_date = Utility.word_date_to_num_date(self.journal_dict_["Entry Date"]
                                                          [journal_trade_idx])
        
        for idx in range(journal_trade_idx - 1, -1, -1):
            exp_date = self.get_expiration_date({}, self.journal_dict_, idx)
            exp_date = Utility.num_date_to_word_date(exp_date)
            exp_date = Utility.word_date_to_num_date(exp_date)

            if self.trade_progress_dict[journal_trade_idx][-1] == "Close":
                continue

            elif Utility.is_date_greater(exp_date, curren_entry_date):
                if (self.trade_progress_dict[journal_trade_idx][2]
                == self.trade_progress_dict[journal_trade_idx][3]):
                    self.trade_progress_dict[journal_trade_idx][-1] = "Close"

                else:
                    # Single or some part of multi leg trade exipred worthless
                    # and was not closed or recorded as a trade in csv
                    self.trade_progress_dict[journal_trade_idx][-1] = "Close"

            else:
                self.trade_progress_dict[journal_trade_idx][-1] = "Open"
            

    def get_progress(self, journal_trade_idx: int) -> str:
        return self.trade_progress_dict[journal_trade_idx][-1]
    
    """ set_progress loop through journal and determines the following in a dictionary
    format: {"journal trade idx": ["expiration date", "ticker", "num of trades opened",
    "num of trades closed", "progress"}"""
    def update_progress(self, journal_trade_idx: int, journal_dict: dict) -> None:
        self.journal_dict_ = journal_dict
        journal_exp_date: str = self.get_expiration_date({}, self.journal_dict_, journal_trade_idx)
        journal_ticker: str = self.get_ticker({}, self.journal_dict_, journal_trade_idx)

        self.trade_progress_dict[journal_trade_idx] = [journal_exp_date, journal_ticker]
        self.trade_progress_dict[journal_trade_idx].append(self.num_trades_open)
        self.trade_progress_dict[journal_trade_idx].append(self.num_trades_closed)

        if self.journal_dict_['Progress'][journal_trade_idx] == 'Close':
            self.trade_progress = 'Close'
            self.trade_progress_dict[journal_trade_idx].append(self.trade_progress)

        else:
            self.trade_progress_dict[journal_trade_idx].append(self.trade_progress)  