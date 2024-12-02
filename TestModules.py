from Test.TestCSVFileHandling import TestCSVFileHandling
from Test.TestUpdateTrades import TestUpdateTrades
from Test.TestUtility import TestUtility
from Test.TestMain import TestMain
import unittest

class TestModules(unittest.TestCase):
    def __init__(self) -> None:
        self.runClasses = [TestCSVFileHandling, TestUpdateTrades, TestUtility]

    # Calls the runTest method of each class in runClasses
    def runTests(self) -> None:
        testSuite = unittest.TestSuite() #unittest.TestLoader().loadTestsFromTestCase(self.runClasses)
        
        for testClass in self.runClasses:
            testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(testClass))
        
        unittest.TextTestRunner().run(testSuite)

            
        