import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_filename():
    # \\server\share
    val = r"\\server\share"
    # if is_filename and starts with \\, it doesn't unescape backslashes (except quotes?)
    # code: if not is_filename or value[:2] != "\\\\": unescape
    # else: return value (quotes stripped)
    
    assert unquote_header_value(val, is_filename=True) == r"\\server\share"

