from requests.utils import unquote_header_value

def test_unquote_header_value_7():
    # Test filename with backslash not at start
    val = '"path\\to\\file"'
    # Should be unescaped
    # "path\to\file" -> path\to\file
    # Code: return value.replace("\\\\", "\").replace('\"', '"')
    # wait, replace("\\\\", "\") means replace double backslash with single.
    # replace('\"', '"') means replace escaped quote with quote.
    # "path\to\file" in Python string is "path\\to\\file"
    # If input is '"path\\to\\file"', stripped is 'path\\to\\file'.
    # Does it have \\\\ ? No.
    # So it returns 'path\\to\\file'.
    
    # If input is escaped backslash: '"path\\\\to\\\\file"'
    # stripped: 'path\\\\to\\\\file'
    # replace matches \\\\ -> \\
    # result: 'path\\to\\file'
    
    val = r'"path\\to\\file"' # Literal "path\\to\\file" inside quotes
    expected = r"path\to\file"
    assert unquote_header_value(val) == expected

