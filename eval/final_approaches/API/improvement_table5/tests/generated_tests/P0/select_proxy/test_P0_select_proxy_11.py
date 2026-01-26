from requests.utils import select_proxy

def test_select_proxy_ignore_port():
    # Scenario: Verify that the port number in the URL is ignored when generating 
    # the proxy lookup key (uses hostname, not netloc).
    url = "http://example.com:8080/path"
    proxies = {
        "http://example.com": "matched-proxy"
    }
    # Even though URL has port 8080, it should match the key without port
    result = select_proxy(url, proxies)
    assert result == "matched-proxy"