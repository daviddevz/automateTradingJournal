from main import main
import unittest

class TestMain(unittest.TestCase):
    def __init__(self,  *args, **kwargs) -> None:
        self.main = main()
        pass

    # Test main function
    def _testMain(self): pass