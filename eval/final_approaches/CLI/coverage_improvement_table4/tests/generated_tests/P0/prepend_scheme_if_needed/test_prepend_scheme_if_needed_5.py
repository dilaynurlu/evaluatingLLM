from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_5():
    # Test valid scheme chars (+, ., -)
    url = "git+ssh://github.com/repo"
    new = prepend_scheme_if_needed(url, "http")
    assert new == "git+ssh://github.com/repo"
