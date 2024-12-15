from datetime import datetime
import sys

class Utility:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    # Add specific character to string object in a specific index
    def add_char(literal: str, character: str) -> str:
        char_idx = literal.find('-')

        if char_idx == -1:
            new_literal = literal[:char_idx] + character + literal[char_idx:]
            return new_literal
        
        else:
            new_literal = literal[:char_idx] + character + literal[char_idx +1:]
            new_literal = new_literal[:char_idx] + '-' + new_literal[char_idx:]
            return new_literal
    
    # Remove specific character in string object
    @staticmethod
    def remove_char(literal: str, character: list[str]) -> str:
        for char in character:
            literal = literal.replace(char, '')
        return literal
    
    # Convert ISO 8601 date format to Date and return a dict with update date
    # YYYY-MM-DDTHH:MM:SSZ to YYYY-MM-DD example 2024-11-07T11:40:48-0600 to 2024-11-07
    @staticmethod
    def ISO8601_datetime_to_date(trade_dict: dict, key: str) -> dict:
        for idx in range(len(trade_dict[key])):
            oldValue = trade_dict[key][idx]
            trade_dict[key][idx] = oldValue[:oldValue.index('T')]
        return trade_dict
        
    # Convert "MMM DD YYYY" to "YYYY-MM-DD"
    @staticmethod
    def word_date_to_num_date(date_literal: str) -> str:
        dateTimeObj = datetime.strptime(date_literal, "%b %d %Y")
        return dateTimeObj.strftime("%Y-%m-%d")
    
    # Convert "YYYY-MM-DD" to "MMM DD YYY"
    @staticmethod
    def num_date_to_word_date(date_literal: str) -> str:
        if '-' in date_literal:
            dateTimeObj = datetime.strptime(date_literal, "%Y-%m-%d")
            return dateTimeObj.strftime("%b %d %Y")
        
        elif '/' in date_literal:
            dateTimeObj = datetime.strptime(date_literal, "%m/%d/%y")
            return dateTimeObj.strftime("%b %d %Y")
    
    @staticmethod
    def is_date_greater_equal(initial_date: str, compare_date: str) -> bool:
        initial_date_obj = datetime.strptime(initial_date, "%Y-%m-%d")
        compare_date_obj = datetime.strptime(compare_date, "%Y-%m-%d")
        return compare_date_obj >= initial_date_obj
    
    @staticmethod
    def is_date_greater(initial_date: str, compare_date: str) -> bool:
        initial_date_obj = datetime.strptime(initial_date, "%Y-%m-%d")
        compare_date_obj = datetime.strptime(compare_date, "%Y-%m-%d")
        return compare_date_obj > initial_date_obj
    
    @staticmethod
    def is_date_equal(initial_date: str, compare_date: str) -> bool:
        initial_date_obj = datetime.strptime(initial_date, "%Y-%m-%d")
        compare_date_obj = datetime.strptime(compare_date, "%Y-%m-%d")
        return compare_date_obj == initial_date_obj
    
    """ The ISO 8601 dateformat is a standard for representing dates and times 
    that uses specific characters to separate date and time components.
    Format: YYYY-MM-DDTHH:MM:SSZ"""
    @staticmethod
    def is_ISO8601(date_literal: list) -> bool:
        for date in date_literal:
            if date == '':
                continue
            else:
                datetime.fromisoformat(date)
                return True