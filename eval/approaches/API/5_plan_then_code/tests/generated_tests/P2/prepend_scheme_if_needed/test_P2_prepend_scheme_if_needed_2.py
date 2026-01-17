from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_existing():
    """
    Test that an existing scheme is preserved and not replaced by the new scheme.
    Note: prepend_scheme_if_needed parses and reconstructs the URL, so we use
    normalized inputs to ensure string equality matches the reconstruction.
    """
    url = "https://example.org/resource"
    new_scheme = "http"
    # The existing scheme 'https' should be kept.
    assert prepend_scheme_if_needed(url, new_scheme) == "https://example.org/resource"