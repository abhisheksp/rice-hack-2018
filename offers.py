# -*- coding: utf-8 -*-

import hashlib
from firebase_admin import initialize_app
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('ricehack2018-firebase-adminsdk-ukl68-192239081c.json')
# Initialize the app with a service account, granting admin privileges
initialize_app(cred, {
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


def update_user_metadata(user_id, user_details):
    ref = db.reference('/users')
    ref.update({user_id: user_details})


def hash(key):
    return hashlib.md5(key.encode()).hexdigest()


def update_user_offers(user_details, emails):
    user_id = hash(user_details['user'])
    new_offers = parse_emails(emails)
    update_user_metadata(user_id, user_details)
    save_new_user_offers(user_id, new_offers)


# TEST
def test_runner():
    emails = [
        {
            "emailTime": "1537015269000",
            "emailBody": "Email Date: mm/dd/yyyy Vendor: ALDO Coupon Code: XXX Expiry: mm/dd/yyyy Product Type:Bag Discount: 50% ‌",
            "emailSubject": "Email Date: mm/dd/yyyy Vendor: ALDO Coupon Code: XXX Expiry: mm/dd/yyyy Product Type:Bag Discount: 50% ‌"
        },
        {
            "emailTime": "1537029703000",
            "emailBody": "Email Date: mm/dd/yyyy Vendor: ALDO Coupon Code: XXX Expiry: mm/dd/yyyy Product Type:Bag2 Discount: 50% ‌",
            "emailSubject": "Email Date: mm/dd/yyyy Vendor: ALDO Coupon Code: XXX Expiry: mm/dd/yyyy Product Type:Bag2 Discount: 50% ‌"
        },
        {
            "emailTime": "1537036010000",
            "emailBody": "PFA ---------- Forwarded message --------- From: noreply@inmoment.com &lt;noreply@inmomentfeedback.com&gt; Date: Wed, Aug 22, 2018 at 12:55 AM Subject: Here is your 15% coupon from ALDO! Happy Shopping",
            "emailSubject": "PFA ---------- Forwarded message --------- From: noreply@inmoment.com &lt;noreply@inmomentfeedback.com&gt; Date: Wed, Aug 22, 2018 at 12:55 AM Subject: Here is your 15% coupon from ALDO! Happy Shopping"
        },
        {
            "emailTime": "1537029674000",
            "emailBody": "Email Date: mm/dd/yyyy Vendor: ALDO Coupon Code: XXX Expiry: mm/dd/yyyy Product Type:Bag1 Discount: 50% ‌",
            "emailSubject": "Email Date: mm/dd/yyyy Vendor: ALDO Coupon Code: XXX Expiry: mm/dd/yyyy Product Type:Bag1 Discount: 50% ‌"
        },
        {
            "emailTime": "1537036199000",
            "emailBody": "PFA ---------- Forwarded message --------- From: ALDO &lt;aldoshoes@e.aldoshoes.com&gt; Date: Wed, Sep 12, 2018 at 8:08 AM Subject: 🚨 60% off everything! 🚨 To: &lt;agrawroh@bu.edu&gt; Make the most of",
            "emailSubject": "PFA ---------- Forwarded message --------- From: ALDO &lt;aldoshoes@e.aldoshoes.com&gt; Date: Wed, Sep 12, 2018 at 8:08 AM Subject: 🚨 60% off everything! 🚨 To: &lt;agrawroh@bu.edu&gt; Make the most of"
        }
    ]

    user_details = {
        'user': 'abhisheksp1993',
        "updatedTime": 1537036469719,
        "token": {
            "access_token": "ya29.GlsZBmtI8NPmyPkM1DKqldpm0GMVZ9k52EYmEG0e1c2UdsB0htevDkbLCTxQdpgEw0auhIvKTq08n_w5We9rqINWuFTT1HnYyMEzf2hL3CRks3whal5ivfYhVjau",
            "refresh_token": "1/eKl8qv_0a7zdS6tbVDfdEEbdzkmystvYpwxxjPrNYm8",
            "scope": "https://www.googleapis.com/auth/gmail.readonly",
            "token_type": "Bearer",
            "expiry_date": 1536990182016
        },
    }
    update_user_offers(user_details, emails)


def reset_offers(user_id):
    ref = db.reference('/offers/users/{}'.format(user_id))
    ref.set({})


def reset_user_details(user_id):
    ref = db.reference('/users/{}'.format(user_id))
    ref.set({})


# reset_offers(hash('abhisheksp1993'))
# reset_user_details(hash('abhisheksp1993'))
# test_runner()
