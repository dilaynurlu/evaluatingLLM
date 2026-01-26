from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslashes():
    """
    Test that escaped backslashes (double backslashes) within the quoted string
    are converted to single backslashes when unquoting.
    Input represents: "domain\\user"
    """
    # The string literal '"domain\\\\user"' evaluates to the string: "domain\\user"
    # The content inside quotes is: domain\\user
    value = '"domain\\\\user"'
    result = unquote_header_value(value)
    
    # Expectation: domain\user
    assert result == 'domain\\user'