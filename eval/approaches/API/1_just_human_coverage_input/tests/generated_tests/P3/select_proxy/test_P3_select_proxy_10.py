from requests.utils import select_proxy

def test_select_proxy_key_with_port_ignored():
    # Scenario: URL has a port, and proxies dict has keys with and without ports.
    # Critique addressed: Keys with Ports.
    # select_proxy logic relies on hostname-only keys.
    # This test verifies that a key explicitly containing a port ("http://example.com:8080")
    # is NOT matched, and the logic correctly finds the host-only key ("http://example.com").
    url = "http://example.com:8080/api"
    proxies = {
        "http://example.com:8080": "http://proxy.specific-port.com",
        "http://example.com": "http://proxy.general.com"
    }
    
    result = select_proxy(url, proxies)
    
    # Expectation: logic strips port from URL, looking up "http://example.com"
    assert result == "http://proxy.general.com"