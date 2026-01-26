from requests.utils import select_proxy

def test_select_proxy_no_hostname_scheme():
    # file:// URLs typically have None as hostname or empty string
    url = "file:///etc/passwd"
    proxies = {
        "file": "http://proxy.file_server.com",
        "all": "http://proxy.global.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://proxy.file_server.com", \
        f"Expected match by scheme 'file' when hostname is missing. Got: {result}"