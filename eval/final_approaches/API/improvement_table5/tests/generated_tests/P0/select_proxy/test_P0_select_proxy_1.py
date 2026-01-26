from requests.utils import select_proxy

def test_select_proxy_none_input():
    # Scenario: Verify that passing None as the proxies argument is handled gracefully (treated as empty)
    # and returns None when no proxy is found.
    url = "http://example.com"
    result = select_proxy(url, None)
    assert result is None