from requests.utils import unquote_header_value

def test_unquote_header_value_basic_quoted():
    """
    Test unquoting strings wrapped in double quotes, including Unicode characters.
    """
    # Basic ASCII
    assert unquote_header_value('"simple_value"') == 'simple_value'
    
    # Unicode handling (UTF-8)
    # Ensure high-bit characters are preserved through the unquoting process
    unicode_val = '"Unicöde_vålue_with_emoji_🚀"'
    expected_unicode = 'Unicöde_vålue_with_emoji_🚀'
    assert unquote_header_value(unicode_val) == expected_unicode