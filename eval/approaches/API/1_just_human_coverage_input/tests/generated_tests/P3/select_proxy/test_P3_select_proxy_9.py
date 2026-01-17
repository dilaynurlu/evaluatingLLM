from requests.utils import select_proxy

def test_select_proxy_ipv6_with_port():
    # Scenario: IPv6 address in URL with a port.
    # Critique addressed: IPv6 with Ports.
    # urlparse can sometimes mishandle brackets if port is present.
    # select_proxy must correctly extract the hostname (without brackets/port) for the key.
    url = "http://[::1]:8080/index.html"
    proxies = {"http://::1": "http://proxy.ipv6.com"}
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.ipv6.com"