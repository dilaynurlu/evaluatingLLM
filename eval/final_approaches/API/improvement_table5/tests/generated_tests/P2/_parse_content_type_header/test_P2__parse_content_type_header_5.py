from requests.utils import _parse_content_type_header

def test_parse_content_type_quote_stripping():
    """
    Test that single and double quotes, as well as spaces, are stripped 
    from both keys and values of the parameters.
    """
    # Note: The function strips " ' and space characters from the ends of the split strings.
    header = "attachment; \"filename\" = 'data.txt'; ' key ' = \" value \""
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "attachment"
    assert params == {
        "filename": "data.txt",
        "key": "value"
    }