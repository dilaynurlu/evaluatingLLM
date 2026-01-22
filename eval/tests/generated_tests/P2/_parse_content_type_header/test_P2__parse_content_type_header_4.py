from requests.utils import _parse_content_type_header

def test_parse_content_type_flags():
    """
    Test parsing parameters that act as flags (no equals sign/value).
    """
    header = "text/plain; myflag; another_flag"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    # Parameters without values are treated as True
    assert params == {
        "myflag": True,
        "another_flag": True
    }