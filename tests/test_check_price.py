import pytest


def test_validate_the_page_ok():
    from amazon_price_check.price_check.check_price import _validate_page
    # from amazon_price_check.price_check.check_price import _validate_the_page
    page = "nothing to see here"
    _validate_page(page)


def test_validate_the_page_automation_detected():
    from amazon_price_check.price_check.check_price import _validate_page,\
        AUTOMATION_DETECTED_STRING
    from amazon_price_check.price_check.errors import AutomationPreventionError

    page = "nothing to see here"+AUTOMATION_DETECTED_STRING+"some other stuff"
    with pytest.raises(AutomationPreventionError):
        _validate_page(page)




