from requests.utils import select_proxy

def test_select_proxy_ignore_port():
    # Using a URL with a port
    url = "http://example.com:8080/foo"
    proxies = {
        "http://example.com": "http://proxy.example.com",
        # This key includes a port, which logic should ideally ignore if it strictly matches host-only
        "http://example.com:8080": "http://proxy.bad.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://proxy.example.com", \
        f"Expected proxy selection to ignore port in URL and match 'scheme://host'. Got: {result}"