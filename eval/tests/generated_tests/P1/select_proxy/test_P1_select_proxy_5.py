from requests.utils import select_proxy

def test_select_proxy_ignores_port():
    """
    Test that the proxy selection logic generates keys based on hostname only, ignoring the port.
    If the URL has a port, it matches a proxy key defined without the port.
    """
    url = "http://example.com:8080/resource"
    proxies = {
        "http://example.com": "http://target-proxy.com",
        "all": "http://wrong-proxy.com"
    }
    
    # Key 'http://example.com' should match despite port 8080 in URL
    result = select_proxy(url, proxies)
    assert result == "http://target-proxy.com"