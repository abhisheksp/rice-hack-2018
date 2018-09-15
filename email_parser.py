import re


def find_brand(email_content):
    supported_brands = ['ALDO']
    for brand in supported_brands:
        if brand in email_content:
            return brand
    # default to ALDO
    return 'ALDO'


def find_discount(email_content):
    discount = re.findall(r'\d{1,2}%|$', email_content)[0]
    return discount


def find_coupon_code(email_content):
    # TODO: add coupon code rules
    return ''


def find_expire_date(email_content):
    expire_date = re.findall(r'until \d{1,2}/\d{1,2}/\d{2,4}|$', email_content)[0]
    expire_date = expire_date and expire_date[6:]
    return expire_date


def find_products(brand):
    brand_products = {
        'ALDO': ['shoe', 'bag'],
        'Nike': ['shoe']
    }
    return brand_products[brand]


def parse_email(email):
    email_content = email['emailBody']
    email_time = email['emailTime']
    brand = find_brand(email_content)
    discount = find_discount(email_content)
    coupon_code = find_coupon_code(email_content)
    expire_date = find_expire_date(email_content)
    products = find_products(brand)
    offer = {
        'brandName': brand,
        'brandeImageURL': '',
        'brandeClassification': products,
        'offerArrivalDate': email_time,
        'offerPercentage': discount,
        'offerExpiry': expire_date,
        'couponCode': coupon_code
    }
    return offer


def parse_emails(emails):
    user_offers = list(map(parse_email, emails))
    return user_offers
