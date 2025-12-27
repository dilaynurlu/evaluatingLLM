from requests.utils import _parse_content_type_header

def test_parse_content_type_header_multiple_params():
    # Refined: Covers high volume of parameters and CRLF handling (Critique: DoS/Security)
    
    # 1. DoS check: Many parameters
    params_part = "; ".join([f"key{i}=val{i}" for i in range(50)])
    header = f"application/test; {params_part}"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/test"
    assert len(params) == 50
    assert params["key0"] == "val0"
    assert params["key49"] == "val49"

    # 2. CRLF check: Ensure newline chars in value are stripped/handled
    header_crlf = "text/plain; key=value\r\n"
    ct, p = _parse_content_type_header(header_crlf)
    assert ct == "text/plain"
    # The standard strip() should remove the trailing CRLF from the value
    assert p["key"] == "value"