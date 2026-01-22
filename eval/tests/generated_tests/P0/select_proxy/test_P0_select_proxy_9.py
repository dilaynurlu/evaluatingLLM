from requests.utils import select_proxy

def test_select_proxy_case_insensitivity():
    """
    Test that URL parsing normalizes scheme/host to lowercase, 
    successfully matching lowercase keys in the proxies dict even if URL is uppercase.
    """
    url = "HTTP://EXAMPLE.COM/resource"
    proxies = {
        "http://example.com": "http://proxy_lower",
    }
    # The function normalizes the URL to http://example.com before lookup
    assert select_proxy(url, proxies) == "http://proxy_lower"