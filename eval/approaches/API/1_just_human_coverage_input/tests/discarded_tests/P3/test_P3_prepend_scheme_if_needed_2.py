from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_mixed_case_scheme():
    # Scenario: URL already has a scheme with mixed casing.
    # Critique addressed: Functional Coverage Gaps (Scheme detection robustness).
    # The function should detect the existing scheme despite casing and NOT prepend the new one.
    url = "Https://example.com"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "Https://example.com"