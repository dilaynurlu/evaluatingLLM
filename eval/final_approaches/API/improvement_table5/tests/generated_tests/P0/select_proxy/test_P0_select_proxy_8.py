from requests.utils import select_proxy

def test_select_proxy_no_hostname_match():
    # Scenario: Verify behavior when URL has no hostname (e.g. file://).
    # It should look up by scheme first.
    url = "file:///etc/hosts"
    proxies = {
        "file": "file-proxy",
        "all": "all-proxy"
    }
    # Parsing 'file:///etc/hosts' results in a None hostname in standard usage
    result = select_proxy(url, proxies)
    assert result == "file-proxy"