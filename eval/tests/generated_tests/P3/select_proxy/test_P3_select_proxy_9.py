from requests.utils import select_proxy

def test_select_proxy_ipv6_handling():
    # Test with Standard IPv6 literal
    url = "http://[2001:db8::1]/index.html"
    proxies = {
        "http://2001:db8::1": "http://proxy.ipv6.com",
        "http": "http://proxy.generic.com"
    }
    # Note: requests/urllib usually strips brackets for the key
    assert select_proxy(url, proxies) == "http://proxy.ipv6.com", \
        "Failed to match IPv6 host literal (brackets stripped)"

    # Test with IPv6 Zone Index (critique point: IPv6 Zone Indices)
    # The function should handle the presence of the zone index (e.g., %eth0)
    url_zone = "http://[fe80::1%eth0]/index.html"
    proxies_zone = {
        "http://fe80::1%eth0": "http://proxy.zone.com",
        "all": "http://proxy.fallback.com"
    }
    
    result_zone = select_proxy(url_zone, proxies_zone)
    assert result_zone == "http://proxy.zone.com", \
        f"Failed to match IPv6 host with zone index. Got: {result_zone}"