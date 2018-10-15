import requests
import sys
from bs4 import BeautifulSoup

from .errors import PricePageRetrievalError, AutomationPreventionError, UserInputError

PRODUCT_URL = "https://www.amazon.com/gp/product/{asin}"
PRICE_TAG_ID = 'priceblock_ourprice'
AUTOMATION_DETECTED_STRING = "To discuss automated access to" \
                                " Amazon data please contact api" \
                                "-services-support@amazon.com."

headers = {
    # 'User-Agent': "I'm totally not a robot. Beep.... beeeep...",
    # triggers automation detection
    'User-Agent': "Netscape 1.0",
    'From': 'ebay.com'
}


def main():

    try:
        price = get_price()
    except AutomationPreventionError:
        print("Automation detected by Amazon")
        sys.exit(1)
    except PricePageRetrievalError:
        print("Unable to get the price")
        sys.exit(1)
    except UserInputError:
        print("Usage: python check_price.py ASIN")
        sys.exit(1)

    print(price)
    sys.exit(0)


def get_price():
    asin = _get_and_validate_user_input()
    url = get_url_for_asin(asin)
    page = get_page(url)
    soup = get_bs4_object(page)

    price = soup.find(id=PRICE_TAG_ID)
    if price:
        return price.text

    raise PricePageRetrievalError


def _get_and_validate_user_input():
    if len(sys.argv) != 2:
        raise UserInputError

    return sys.argv[1]


def get_url_for_asin(asin):
    return PRODUCT_URL.format(asin=asin)


def get_page(url):
    page = requests.get(url, headers=headers)
    print(page.text)
    _validate_page(page.text)

    return page.text


def get_bs4_object(page):
    soup = BeautifulSoup(page, features="html.parser")
    return soup


def _validate_page(page):
    if AUTOMATION_DETECTED_STRING in page:
        raise AutomationPreventionError


if __name__ == "__main__":
    main()
