from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc():
    value = '"\\server\share"'
    # is_filename=True -> preserve UNC
    assert unquote_header_value(value, is_filename=True) == "\\server\share"
