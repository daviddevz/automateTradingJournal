from datetime import datetime
import sys

class Utility:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    # Add specific character to string object in a specific index
    def add_char(literal: str, character: str, idx: int) -> str:
        try:
            new_literal = literal[:idx] + character + literal[idx:]
            return new_literal

        except IndexError:
            if literal == '':
                print(f"ERROR: literal is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)

            elif character == '':
                print(f"ERROR: character is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)

            else:
                print(f"ERROR: index out of range at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
    
    # Remove specific character in string object
    @staticmethod
    def remove_char(literal: str, character: str) -> str:
        try:
            str_idx = literal.index(character)

            if str_idx == 0:
                return literal[str_idx +1:]
            
            elif str_idx == len(literal) -1:
                return literal[:str_idx]
            else:
                return literal[:str_idx] + literal[str_idx +1:]

        except ValueError:
            if literal == '':
                print(f"ERROR: literal is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)

            elif character == '':
                print(f"ERROR: character is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)

            else:
                print(f"ERROR: {character} not found in {literal} at line, "
                      f"{sys.exc_info()[2].tb_lineno}", file = sys.stderr)
                sys.exit(1)
    
    # Convert ISO 8601 date format to Date and return a dict with update date
    # YYYY-MM-DDTHH:MM:SSZ to YYYY-MM-DD example 2024-11-07T11:40:48-0600 to 2024-11-07
    @staticmethod
    def ISO8601_datetime_to_date(trade_dict: dict, key: str) -> dict:
        try:
            for idx in range(len(trade_dict[key])):
                oldValue = trade_dict[key][idx]
                trade_dict[key][idx] = oldValue[:oldValue.index('T')]
            return trade_dict
        
        except Exception as e:
            print(f"ERROR: {e} at line {sys.exc_info()[2].tb_lineno}",
                  file = sys.stderr)
            sys.exit(1)
        
    # Convert "MMM DD YYYY" to "YYYY-MM-DD"
    @staticmethod
    def word_date_to_num_date(date_literal: str) -> str:
        try:
            dateTimeObj = datetime.strptime(date_literal, "%b %d %Y")
            return dateTimeObj.strftime("%Y-%m-%d")
        
        except ValueError:
            if date_literal == '':
                print(f"ERROR: date_literal is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
            
            else:
                print(f"ERROR: Invalid date format at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
    
    # Convert "YYYY-MM-DD" to "MMM DD YYY"
    @staticmethod
    def num_date_to_word_date(date_literal: str) -> str:
        try:
            dateTimeObj = datetime.strptime(date_literal, "%Y-%m-%d")
            return dateTimeObj.strftime("%b %d %Y")
        
        except ValueError:
            if date_literal == '':
                print(f"ERROR: date_literal is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
            
            else:
                print(f"ERROR: Invalid date format at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
    
    @staticmethod
    def is_date_greater_equal(initial_date: str, compare_date: str) -> bool:
        try:
            initial_date_obj = datetime.strptime(initial_date, "%Y-%m-%d")
            compare_date_obj = datetime.strptime(compare_date, "%Y-%m-%d")
            return compare_date_obj >= initial_date_obj
        
        except ValueError:
            if initial_date == '':
                print(f"ERROR: initial_date is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
                
            elif compare_date == '':
                print(f"ERROR: compare_date is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
                
            else:
                print(f"ERROR: Invalid date format {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
    
    @staticmethod
    def is_date_greater(initial_date: str, compare_date: str) -> bool:
        try:
            initial_date_obj = datetime.strptime(initial_date, "%Y-%m-%d")
            compare_date_obj = datetime.strptime(compare_date, "%Y-%m-%d")
            return compare_date_obj > initial_date_obj
        
        except ValueError:
            if initial_date == '':
                print(f"ERROR: initial_date is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)

            elif compare_date == '':
                print(f"ERROR: compare_date is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
                
            else:
                print(f"ERROR: Invalid date format {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
    
    @staticmethod
    def is_date_equal(initial_date: str, compare_date: str) -> bool:
        try:
            initial_date_obj = datetime.strptime(initial_date, "%Y-%m-%d")
            compare_date_obj = datetime.strptime(compare_date, "%Y-%m-%d")
            return compare_date_obj == initial_date_obj
        
        except ValueError:
            if initial_date == '':
                print(f"ERROR: initial_date is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
            
            elif compare_date == '':
                print(f"ERROR: compare_date is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)

            else:
                print(f"ERROR: Invalid date format {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
    
    """ The ISO 8601 dateformat is a standard for representing dates and times 
    that uses specific characters to separate date and time components.
    Format: YYYY-MM-DDTHH:MM:SSZ"""
    @staticmethod
    def is_ISO8601(date_literal: list) -> bool:
        try:
            for date in date_literal:
                if date == '':
                    continue
                else:
                    datetime.fromisoformat(date)
                    return True
        except ValueError:
            if date_literal == '':
                print(f"ERROR: date_literal is empty at line {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)
            
            else:
                print(f"ERROR: Invalid date format {sys.exc_info()[2].tb_lineno}",
                      file = sys.stderr)
                sys.exit(1)