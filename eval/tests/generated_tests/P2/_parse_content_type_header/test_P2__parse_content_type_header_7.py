from requests.utils import _parse_content_type_header

def test_parse_content_type_equals_in_quoted_value():
    """
    Test that an equals sign inside a quoted value is treated as part of the value,
    not as a delimiter for that specific parameter logic.
    """
    header = 'text/x-custom; config="key=value"'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/x-custom"
    # The split logic finds the first '=' for separation, but quotes are stripped afterwards.
    # Logic: key='config', value='"key=value"' -> stripped to 'key=value'
    assert params == {"config": "key=value"}