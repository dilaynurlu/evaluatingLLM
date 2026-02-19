from requests.utils import select_proxy

def test_select_proxy_empty_proxies():
    # Scenario: Verify that passing an empty dictionary as proxies returns None.
    url = "http://example.com"
    result = select_proxy(url, {})
    assert result is None