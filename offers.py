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


# TODO: remove after integrating with other APIs
def seed_emails():
    user_id = 'abhisheksp1993'

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

    ref = db.reference('/')
    ref.set({
        'emails': {
            'users': {
                user_id: [
                    aldo_email,
                    bestbuy_email,
                ]
            }
        },
        'offers': {
            'users': {
                user_id: [],
            },
        }
    })


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


def parse_emails():
    ref = db.reference('/emails/users')
    users_emails = ref.get()
    user_offers = {}
    for user_id, emails in users_emails.items():
        user_offers[user_id] = list(map(parse_email, emails))
    return user_offers


def save_user_offers(user_offers):
    for user_id, new_offers in user_offers.items():
        ref = db.reference('/offers/users/')
        existing_offers = ref.child(user_id).get() or []
        existing_offers += new_offers  # TODO: find a better way to add to existing list
        ref.update({user_id: existing_offers})


def update_offers():
    seed_emails()
    user_offers = parse_emails()
    save_user_offers(user_offers)
