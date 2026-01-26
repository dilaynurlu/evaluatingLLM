import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_quoted_values():
    """
    Test parsing content type parameters where values are enclosed in quotes.
    Refined to test unbalanced quotes and basic escaping scenarios.
    """
    # Standard quoted
    header = "application/atom+xml; type=\"entry\"; charset='utf-8'"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "application/atom+xml"
    assert params == {'type': 'entry', 'charset': 'utf-8'}

    # Refinement: Unbalanced quotes (Security: robustness check)
    # The parser uses .strip('"'), so a single quote at start might be removed, 
    # leaving the rest.
    header_unbalanced = 'text/plain; title="Incomplete'
    _, params_u = _parse_content_type_header(header_unbalanced)
    # "Incomplete -> Incomplete (if strip removes only valid pairs or just characters)
    # requests .strip() removes all leading/trailing chars. 
    # '"Incomplete'.strip('"') -> 'Incomplete'
    assert params_u.get('title') == 'Incomplete'

    # Refinement: Quotes inside value (Not truly escaped in requests simple logic, 
    # but ensuring it doesn't crash)
    header_escaped = 'text/plain; key="val\\"ue"'
    _, params_e = _parse_content_type_header(header_escaped)
    # "val\"ue" stripped of quotes -> val\"ue
    assert params_e.get('key') == 'val\\"ue'