import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_single_quote_mismatch():
    """
    Test unquoting a string that has only one quote or mismatched quotes.
    Should return the string as-is because it doesn't meet the "wrapped in quotes" criteria.
    """
    input_val = '"mismatched'
    expected = '"mismatched'
    assert unquote_header_value(input_val) == expected
    
    input_val_2 = 'mismatched"'
    assert unquote_header_value(input_val_2) == 'mismatched"'