from requests.utils import unquote_header_value

def test_unquote_header_value_4():
    # is_filename=True logic
    # "C:\\foo\\bar.txt" -> check if unquoted correctly or left alone
    
    # Case 1: normal quoted string
    assert unquote_header_value('"foo"', is_filename=True) == "foo"
    
    # Case 2: UNC path \\
    # code: if not is_filename or value[:2] != "\\\\":
    # If it starts with \\, it might NOT unquote?
    
    # value = "\\\\server\\share" ?
    # logic:
    # value = value[1:-1] -> \\\\server\\share
    # if not is_filename or value[:2] != "\\\\": ...
    # if it IS filename and starts with \\\\, it skips the replace.
    
    val = '"\\\\server\\share"'
    # unquoted -> \\server\share
    # replace skipped.
    assert unquote_header_value(val, is_filename=True) == "\\\\server\\share"
    
    # Compare with is_filename=False
    # replace("\\\\", "\\\\").replace('\\"', '"')
    # \\server\share -> \server\share ?
    assert unquote_header_value(val, is_filename=False) == "\\server\\share"

