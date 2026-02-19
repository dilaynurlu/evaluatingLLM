from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal():
    value = r'"C:\file.txt"'
    # is_filename=True -> normal unquote
    assert unquote_header_value(value, is_filename=True) == r"C:\file.txt"

