import csv
from src.trade_sort.utility import Utility

class CSVHandling:
    def __init__(self, file_path: str, col_to_remove: list = []) -> None:
        self.file_path_ = file_path
        self.col_to_remove_ = col_to_remove
        self.copy_filename = self.get_copy_filename()
    
    def get_copy_filename(self) -> str:
        return self.file_path_.replace('.csv', '_copy.csv', 1)
    
    def create_copy(self) -> None:
        with open(self.file_path_,'r', newline='') as csvfile:
            read = csv.reader(csvfile, delimiter=',')

            with open(self.copy_filename, 'w', newline='') as csvfile:
                writeFile = csv.writer(csvfile, delimiter=',')

                for row in read:
                    writeFile.writerow(row)
    
    def create_dict(self) -> dict:
        with open(self.copy_filename, newline='') as csvfile:
            header = next(csv.reader(csvfile))
            reader = csv.DictReader(csvfile, fieldnames= header)
            csv_dict = {}

            for row in reader:
                for key in row:
                    if key == '' or key in self.col_to_remove_:
                        continue

                    elif key not in csv_dict:
                        csv_dict[key] = []
                        csv_dict[key].append(row[key])

                    else:
                        csv_dict[key].append(row[key])
            
            # Converts ISO 8601 format YYYY-MM-DDTHH:MM:SSZ to YYYY-MM-DD
            # Checks csv dict is not journal dict
            if "Entry Date" not in csv_dict.keys() and Utility.is_ISO8601(csv_dict['Date']):
                return Utility.ISO8601_datetime_to_date(csv_dict, 'Date') 
            
            else:
                return csv_dict
    
    def dict_to_csv(self, dict_copy: dict) -> None:
        with open(self.copy_filename,'w', newline='') as csvfile:
            fieldnames = list(dict_copy.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            
            writer.writeheader()

            for idx in range(len(dict_copy[fieldnames[0]])):
                row = {}

                for key in fieldnames:
                    row[key] = dict_copy[key][idx]

                writer.writerow(row)
        
