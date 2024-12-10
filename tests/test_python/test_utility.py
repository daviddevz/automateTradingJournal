from src.trade_sort.utility import Utility
import pytest

# Test for the Utility class
class TestUtility():
    def test_init(self) -> None:
        assert Utility()
    
    # Test for the dateTimeToDate method
    @pytest.mark.parametrize(
        "dictVar, key, expectedResult",
        [
            ({'Date': ['2022-01-01T00:00:00', '2022-01-02T00:00:00', '2022-01-03T00:00:00']},
             'Date', {'Date': ['2022-01-01', '2022-01-02', '2022-01-03']}),

            ({'Date': ['2022-01-0100:00:00', '2022-01-0200:00:00', '2022-01-0300:00:00']},
             'Date', pytest.raises(ValueError)),
        ],
    )
    def test_datetime_to_date(self, dictVar, key, expectedResult) -> None:
        # Test for Utility.datetime_todate implementation
        if isinstance(expectedResult, type(pytest.raises(ValueError))):
            with expectedResult:
                Utility.datetime_todate(dictVar, key)
        else:
            assert Utility.datetime_todate(dictVar, key) == expectedResult
    
    # Test for Utility.splice_trade_des implementation
    @pytest.mark.parametrize(
        "tradeDescription, tradeAction, expectedResult",
        [
            ('Sold 1 SMH 11/15/24 Put 220.00 @ 0.06', 'SELL_TO_CLOSE', '1 SMH 11/15/24 Put 220.00'),
            ('Bought 1 SMH 11/15/24 Put 220.00 @ 0.06', 'BUY_TO_CLOSE', '1 SMH 11/15/24 Put 220.00'),
            ('Sold 1 SMH 11/15/24 Put 220.00 @ 0.06', 'SELL_TO_OPEN', '1 SMH 11/15/24 Put 220.00'),
            ('Bought 1 SMH 11/15/24 Put 220.00 @ 0.06', 'BUY_TO_OPEN', '1 SMH 11/15/24 Put 220.00'),            
            ('S 1 SMH 11/15/24 Put 220.00 @ 0.06', 'SELL_TO_CLOSE', pytest.raises(ValueError)), 
            ('B 1 SMH 11/15/24 Put 220.00 @ 0.06', 'BUY_TO_CLOSE', pytest.raises(ValueError)),            
            (' 1 SMH 11/15/24 Put 220.00 @ 0.06', 'SELL_TO_OPEN', pytest.raises(ValueError)),
            (' 1 SMH 11/15/24 Put 220.00 @ 0.06', 'BUY_TO_OPEN', pytest.raises(ValueError)), 
            (' 1 SMH 11/15/24 Put 220.00  0.06', 'SELL_TO_OPEN', pytest.raises(ValueError)),
            (' 1 SMH 11/15/24 Put 220.00  0.06', 'BUY_TO_OPEN', pytest.raises(ValueError)),     
        ]
    )
    def test_splice_trade_des(self, tradeDescription, tradeAction, expectedResult) -> None:
        if isinstance(expectedResult, type(pytest.raises(ValueError))):
            with expectedResult:
                Utility.splice_trade_des(tradeDescription, tradeAction)
        else:
            assert Utility.splice_trade_des(tradeDescription, tradeAction) == expectedResult
        
    # Test for Utility.worddate_to_numdate implementation
    @pytest.mark.parametrize(
        "dateStr, expectedResult",
        [
            ('Sep 12 2022', '2022-09-12'),
            ('2022 Sep 12', pytest.raises(ValueError)),
            ('October 12 2012', pytest.raises(ValueError)),
            ('2022-01-0100:00:00', pytest.raises(ValueError)),
        ],
    )
    def test_word_date_to_num_date(self, dateStr, expectedResult) -> None:
        if isinstance(expectedResult, type(pytest.raises(ValueError))):
            with expectedResult:
                Utility.worddate_to_numdate(dateStr)
        else:
            assert Utility.worddate_to_numdate(dateStr) == expectedResult