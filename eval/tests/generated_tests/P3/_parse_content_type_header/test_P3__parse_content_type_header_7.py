from requests.utils import _parse_content_type_header

def test_parse_content_type_header_case_insensitive_keys():
    # Refined: Covers case insensitivity and duplicate parameters (Critique: Duplicate Parameters)
    header = "text/html; CharSet=UTF-8; charset=iso-8859-1"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    # Ensure keys are lowercased
    assert "charset" in params
    assert "CharSet" not in params
    # Ensure defined behavior for duplicates (last wins is standard in Python dicts)
    assert params["charset"] == "iso-8859-1"