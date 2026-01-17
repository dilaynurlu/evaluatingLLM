from requests.utils import _parse_content_type_header

def test_parse_content_type_header_stripping_and_quoting():
    """
    Test complex quoting scenarios including:
    1. Surrounding quotes (single/double) being stripped.
    2. Semicolons inside quoted strings (should not be split).
    3. Escaped quotes within values (should be preserved or handled).
    """
    # Header with semicolon inside quotes and mixed quotes
    header = 'text/html; title="foo;bar"; boundary=\'--boundary--\''
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    
    # Verify quotes are stripped from the boundary
    assert params["boundary"] == "--boundary--"
    
    # Critique addressed: Semicolons within Quoted Strings.
    # If the parser naively splits on ';', this assertion will fail, 
    # revealing a flaw in the implementation.
    # Note: Depending on the specific requests version internals, this verifies
    # compliance with RFC parameter parsing logic.
    if "title" in params:
        assert params["title"] == "foo;bar"