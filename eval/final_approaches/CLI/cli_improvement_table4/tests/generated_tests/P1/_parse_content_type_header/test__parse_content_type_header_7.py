import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_case_insensitive():
    """Test that parameter keys are lowercased and whitespace is stripped."""
    header = "Text/Html ; Charset=UTF-8"
    content_type, params = _parse_content_type_header(header)
    # The first part is stripped but not lowercased in the return value?
    # Code: content_type = tokens[0].strip()
    assert content_type == "Text/Html"
    # Keys are lowercased: params_dict[key.lower()] = value
    assert params == {"charset": "UTF-8"}
