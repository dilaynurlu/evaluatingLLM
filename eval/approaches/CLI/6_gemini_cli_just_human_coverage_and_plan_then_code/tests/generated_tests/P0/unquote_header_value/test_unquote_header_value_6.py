
import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_path():
    # UNC path like \\server\share
    # The implementation says: if not is_filename or value[:2] != "\\\\
    # So if is_filename is True and it starts with \\, it just returns without quotes stripped?
    # Wait, code:
    # if not is_filename or value[:2] != "\\\\
    #    return value.replace("\\\\", "\\").replace('\\"', '"')
    #
    # Wait, the code removes surrounding quotes FIRST:
    # value = value[1:-1]
    #
    # So if input is '"\\server\share"'
    # value becomes '\\server\share'
    # if is_filename=True and value[:2] == '\\':
    #    skips the replace call
    
    value = r'"\\server\share"'
    result = unquote_header_value(value, is_filename=True)
    assert result == r'\\server\share'

