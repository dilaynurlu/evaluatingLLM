from requests.utils import select_proxy

def test_select_proxy_exact_scheme_host():
    # Using mixed-case URL to test case insensitivity in matching logic
    url = "HTTP://WWW.GOOGLE.COM/search"
    proxies = {
        "http://www.google.com": "http://proxy.google.com",
        "http": "http://proxy.generic.com",
        "all": "http://proxy.fallback.com"
    }
    
    # The function should normalize the URL scheme and host to lowercase before lookup
    result = select_proxy(url, proxies)
    assert result == "http://proxy.google.com", \
        f"Expected exact scheme+host match to be selected despite mixed case URL. Got: {result}"