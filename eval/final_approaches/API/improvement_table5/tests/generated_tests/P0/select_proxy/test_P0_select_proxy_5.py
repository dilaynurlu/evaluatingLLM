from requests.utils import select_proxy

def test_select_proxy_all_host_precedence():
    # Scenario: Verify that "all://hostname" takes precedence over "all".
    url = "ftp://example.com/foo"
    proxies = {
        # "ftp://example.com" and "ftp" are missing
        "all://example.com": "http://all-host-proxy",
        "all": "http://generic-proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "http://all-host-proxy"