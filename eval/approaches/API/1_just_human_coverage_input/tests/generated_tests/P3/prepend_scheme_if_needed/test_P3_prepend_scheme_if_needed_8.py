from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_url_with_query_and_fragment():
    # Scenario: URL contains query parameters and a fragment/anchor.
    # Critique addressed: URL Fragments.
    # The function must preserve both the query and the fragment in the correct order.
    url = "example.org/search?q=python#ref"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://example.org/search?q=python#ref"