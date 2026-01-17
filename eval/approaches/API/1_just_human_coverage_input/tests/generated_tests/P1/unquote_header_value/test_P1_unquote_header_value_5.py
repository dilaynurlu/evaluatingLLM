from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal_unescaping():
    # Scenario: When is_filename=True but the content is NOT a UNC path (e.g. C:\\),
    # backslashes should be unescaped normally.
    # Input corresponds to: "C:\\path\\file.txt"
    # Inner content: C:\\path\\file.txt (does not start with \\)
    input_val = r'"C:\\path\\file.txt"'
    # Expected: C:\path\file.txt
    expected = r'C:\path\file.txt'
    assert unquote_header_value(input_val, is_filename=True) == expected