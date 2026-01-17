import pytest
from requests.utils import unquote_header_value

@pytest.mark.parametrize("input_val, expected", [
    ('"my-value"', 'my-value'),
    ('"foo bar"', 'foo bar'),              # Whitespace handling
    ('"foo\\"bar"', 'foo"bar'),            # Escaped quote handling
    ('"Tést"', 'Tést'),                    # Unicode handling
    ('" value "', ' value '),              # Leading/trailing whitespace preservation
])
def test_unquote_header_value_compliant(input_val, expected):
    """
    Refined test for standard Quoted-String unquoting.
    
    Addresses critique:
    - Missing Escaped Quotes
    - Whitespace Handling
    - Unicode and Encoding
    """
    assert unquote_header_value(input_val) == expected