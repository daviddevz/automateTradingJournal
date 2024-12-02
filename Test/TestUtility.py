import unittest
from Classes.Utility import Utility


class TestUtility(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        pass
        
    # Test for the Utility class
    # Test for the dateTimeToDate method
    def _testDateTimeToDate(self) -> None:
        # Test for Utility.dateTimeToDate implementation
        dictVar = {'Date': ['2022-01-01T00:00:00', '2022-01-02T00:00:00', '2022-01-03T00:00:00']}
        result = Utility.dateTimeToDate(dictVar, 'Date')
        expectedResult = {'Date': ['2022-01-01', '2022-01-02', '2022-01-03']}
        self.assertEqual(result, expectedResult)

        # Test for ValueError where T is missing. T is used in Utility.dateTimeToDate to split the date and time
        dictVar2 = {'Date': ['2022-01-0100:00:00', '2022-01-0200:00:00', '2022-01-0300:00:00']}
        with self.assertRaises(ValueError):
            Utility.dateTimeToDate(dictVar2, 'Date')