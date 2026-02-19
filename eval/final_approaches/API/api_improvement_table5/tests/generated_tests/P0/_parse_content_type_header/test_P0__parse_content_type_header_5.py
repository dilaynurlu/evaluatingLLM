from requests.utils import _parse_content_type_header

def test_content_type_irregular_whitespace_and_empty_segments():
    # Scenario: Header with extra spaces and empty segments (consecutive semicolons)
    header = "  image/png  ;  ;  q = 0.8  "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "image/png"
    assert params == {"q": "0.8"}