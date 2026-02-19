from requests.utils import get_auth_from_url

def test_get_auth_from_url_none_input():
    """
    Test with None and other invalid non-string inputs.
    
    Verifies that the function is robust against improper input types (None, int, list)
    by catching the resulting AttributeErrors or TypeErrors during parsing/unquoting
    and returning safe defaults ("","").
    """
    invalid_inputs = [None, 12345, ["http://url"], object()]
    
    for invalid in invalid_inputs:
        result = get_auth_from_url(invalid)
        assert result == ("", ""), f"Failed for input type: {type(invalid)}"