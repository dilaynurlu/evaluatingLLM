from requests.utils import _parse_content_type_header

def test_parse_content_type_strip_quotes_and_spaces():
    """Test that quotes and surrounding whitespace are stripped from parameter keys and values."""
    # The function strips double quotes, single quotes, and spaces from params
    header = "attachment; filename=\"fname.ext\""
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "attachment"
    assert params == {"filename": "fname.ext"}