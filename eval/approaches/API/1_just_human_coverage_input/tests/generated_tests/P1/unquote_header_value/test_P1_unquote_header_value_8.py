from requests.utils import unquote_header_value

def test_unquote_header_value_none_input():
    # Scenario: Passing None should return None without error
    assert unquote_header_value(None) is None