from requests.utils import select_proxy

def test_select_proxy_ipv6():
    # Scenario: Verify correct key generation for IPv6 literals.
    # The key should be constructed using the unbracketed IPv6 address.
    url = "http://[2001:db8::1]/index.html"
    proxies = {
        "http://2001:db8::1": "ipv6-proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "ipv6-proxy"