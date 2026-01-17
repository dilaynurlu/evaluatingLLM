from requests.utils import unquote_header_value

def test_unquote_header_filename_unc():
    # If is_filename=True and starts with \, it avoids some replacements
    # input: "\\server\share" (as string) -> no, it comes quoted: "\"\\server\share\""
    # value[1:-1] -> "\\server\share"
    # if is_filename and value[:2] == "\\": return value
    
    val = r'"\\server\share"'
    assert unquote_header_value(val, is_filename=True) == r'\\server\share'

