from src.trade_sort.utility import Utility


class TradeValidator:
    def __init__(self, journal_dict: dict, transaction_dict: dict) -> None:
        self.journal_dict_ = journal_dict
        self.transaction_dict_ = transaction_dict

    # Convert Sold 1 SMH 11/15/24 Put 220.00 @ 0.06 to 1 SMH 11/15/24 Put 220.00
    # Convert Bought 1 SMH 11/15/24 Put 220.00 @ 0.06 to 1 SMH 11/15/24 Put 220.00    
    def splice_trade_description(self, trade_description: str) -> str:
        if trade_description.find('Sold') != -1:
            splice = trade_description[trade_description.index('Sold') +5
                                    :trade_description.index('@') -1]
            return splice
        
        elif trade_description.find('Bought') != -1:
            splice = trade_description[trade_description.index('Bought') +7 
                                      :trade_description.index('@') -1]
            return splice

    