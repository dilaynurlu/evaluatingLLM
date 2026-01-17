import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ignores_existing_scheme():
    """
    Test that existing schemes are preserved.
    Refined to include:
    1. Standard hierarchy (https).
    2. Opaque schemes (mailto).
    3. Dangerous/Script schemes (javascript).
    """
    new_scheme = "http"

    # Standard
    assert prepend_scheme_if_needed("https://example.org", new_scheme) == "https://example.org"

    # Opaque
    assert prepend_scheme_if_needed("mailto:user@example.com", new_scheme) == "mailto:user@example.com"

    # Dangerous / Other
    # Ensure it doesn't become http://javascript:alert(1)
    assert prepend_scheme_if_needed("javascript:alert(1)", new_scheme) == "javascript:alert(1)"