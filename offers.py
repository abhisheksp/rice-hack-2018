import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('ricehack2018-firebase-adminsdk-ukl68-192239081c.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ricehack2018.firebaseio.com/'
})


# TODO: possible improvements
# 1. add appropriate index
# 2. trigger asynchronously

def parse_email(email_content):
    aldo_offer = {
        'email_date': '09/15/2018',
        'vendor': 'ALDO',
        'coupon_code': 'HJASBDKJ',
        'expire_date': '09/15/2018',
        'product_types': ['shoe', 'bag'],
        'discount': 50,
    }

    bestbuy_offer = {
        'email_date': '09/16/2018',
        'vendor': 'BestBuy',
        'coupon_code': 'HJASBDKJ',
        'expire_date': '10/01/2018',
        'product_types': ['mobile', 'laptop', 'camera', 'television'],
        'discount': 40,
    }

    # TODO: update parsing logic once hardcoded email API is completed
    if 'ALDO' in email_content:
        return aldo_offer
    else:
        return bestbuy_offer


def parse_emails(emails):
    user_offers = list(map(parse_email, emails))
    return user_offers


def save_new_user_offers(user_id, new_offers):
    ref = db.reference('/offers/users/')
    existing_offers = ref.child(user_id).get() or []
    existing_offers += new_offers  # TODO: find a better way to add to existing list
    ref.update({user_id: existing_offers})


def update_user_offers(user_id, emails):
    new_offers = parse_emails(emails)
    save_new_user_offers(user_id, new_offers)


# TEST
def test_runner():
    aldo_email = '''
    ALDO Offer

    Free Shipping!

    {ALDO_PRODUCTS}

    Valid until October 19th, 2018.
    '''
    bestbuy_email = '''
    BestBuy Offer

    Best deals in the world!

    {BestBuy_PRODUCTS}

    Valid until September 29th, 2018.
    '''
    user_id = 'abhisheksp1993'
    emails = [aldo_email, bestbuy_email]
    update_user_offers(user_id, emails)


def reset_offers(user_id):
    ref = db.reference('/offers/users/{}'.format(user_id))
    ref.set({})


# reset_offers('abhisheksp1993')
# test_runner()
