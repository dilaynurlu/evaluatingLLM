from requests.utils import unquote_header_value

def test_unquote_header_filename_normal():
    val = '"file.txt"'
    assert unquote_header_value(val, is_filename=True) == "file.txt"
