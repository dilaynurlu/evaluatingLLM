from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_preservation():
    # Scenario: When is_filename=True and the content looks like a UNC path (starts with \\),
    # the function should return the content without unescaping the backslashes.
    # Input corresponds to: "\\server\share"
    # Inner content: \\server\share (starts with \\)
    input_val = r'"\\server\share"'
    # Expected: \\server\share (quotes removed, but backslashes preserved)
    expected = r'\\server\share'
    assert unquote_header_value(input_val, is_filename=True) == expected