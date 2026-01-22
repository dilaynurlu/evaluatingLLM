from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_various_existing_schemes():
    """
    Test that if the URL already has a scheme, it is NOT replaced.
    Includes coverage for schemes without double slashes (e.g., mailto, news).
    """
    # Standard scheme with double slashes
    url_https = "https://example.com/resource"
    new_scheme = "http"
    assert prepend_scheme_if_needed(url_https, new_scheme) == "https://example.com/resource"

    # Scheme without double slashes (Critique: Schemes without Double Slashes)
    # 'mailto' is a valid scheme; the function should detect it and not prepend http.
    url_mailto = "mailto:user@example.com"
    assert prepend_scheme_if_needed(url_mailto, new_scheme) == "mailto:user@example.com"
    
    # Another opaque scheme example
    url_news = "news:comp.lang.python"
    assert prepend_scheme_if_needed(url_news, new_scheme) == "news:comp.lang.python"