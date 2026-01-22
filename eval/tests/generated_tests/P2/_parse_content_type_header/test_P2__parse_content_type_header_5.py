from requests.utils import _parse_content_type_header

def test_parse_content_type_case_normalization():
    """
    Test that parameter keys are case-insensitive and normalized to lowercase,
    while values preserve their case.
    """
    header = "application/json; CharSet=Utf-8; Version=1.0"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {
        "charset": "Utf-8",
        "version": "1.0"
    }