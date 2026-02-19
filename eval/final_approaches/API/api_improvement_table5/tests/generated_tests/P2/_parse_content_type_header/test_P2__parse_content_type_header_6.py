from requests.utils import _parse_content_type_header

def test_parse_content_type_case_insensitivity_and_overwrite():
    """
    Test that parameter keys are normalized to lowercase and that 
    subsequent parameters with the same key overwrite previous ones.
    """
    header = "application/x-www-form-urlencoded; CharSet=UTF-8; charset=ISO-8859-1"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/x-www-form-urlencoded"
    # 'CharSet' becomes 'charset', and the second 'charset' overwrites the first.
    assert params == {"charset": "ISO-8859-1"}