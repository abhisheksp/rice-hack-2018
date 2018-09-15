# -*- coding: utf-8 -*-

import hashlib
import re
from firebase_admin import initialize_app
from firebase_admin import credentials
from firebase_admin import db
from email_parser import parse_emails

# Fetch the service account key JSON file contents
cred = credentials.Certificate('ricehack2018-firebase-adminsdk-ukl68-192239081c.json')
# Initialize the app with a service account, granting admin privileges
initialize_app(cred, {
    'databaseURL': 'https://ricehack2018.firebaseio.com/'
})


# TODO: possible improvements
# 1. add appropriate index
# 2. trigger asynchronously

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
            "emailBody": "Present coupon in store or enter code online to redeem 15% off any purchase of at least $75 USD before tax (subject exceptions below), within 30 days of receiving this coupon. Offer applies to in-store purchases at Aldo store locations and online at aldoshoes.com. Offer not valid towards the purchase of footwear care products, gift cards, previous purchases and cannot be combined with any other offer or promotion. After 30 days, this offer is null and void. Coupon may not be re-issued, re-validated or redeemed for cash. All applicable sales taxes excluded. Valid for one-time use only. Aldo is not responsible if coupon is lost, stolen or used without authorization.‌",
            "emailSubject": "Here is your 15% coupon from ALDO! Happy Shopping!‌"
        },
        {
            "emailTime": "1537029703000",
            "emailBody": "20% off on Clothing, Shoes and Accessories Category & **20% off on Bags and Luggage Category: 20% discount up to $30 maximum discount. Valid from 9/11/18 at 12:00AM (PST) until 9/17/18 at 11:59PM (PST) or until promotional funding is exhausted, whichever occurs first. Rakuten.com reserves the right to cancel, modify or limit the promotion at any time in its sole discretion. This promotion is open only to individuals 18 or older and must establish a Rakuten.com account or be signed into their Rakuten.com account to apply the Coupon Code APPAREL20 and BAGS20. This Coupon Code is valid for one-time use and can be used only once per account within a single transaction with one merchant, while supplies last. Limit one redemption for each coupon per household. Coupon code exclude certain products due to the merchant’s sales restriction. Gift cards cannot be redeemed in conjunction with this promotion. Bulk purchases made by re-sellers do not qualify. This promotion is not valid with any other offer. You are responsible to pay for any applicable sales tax on your purchase and this is valid in U.S. only.‌",
            "emailSubject": "2 Days of Earning 20% Back in Points Sitewide‌"
        },
        {
            "emailTime": "1537036010000",
            "emailBody": "PFA ---------- Forwarded message --------- From: noreply@inmoment.com &lt;noreply@inmomentfeedback.com&gt; Date: Wed, Aug 22, 2018 at 12:55 AM Subject: Aldo",
            "emailSubject": "PFA ---------- Forwarded message --------- From: noreply@inmoment.com &lt;noreply@inmomentfeedback.com&gt; Date: Wed, Aug 22, 2018 at 12:55 AM Subject: Here is your coupon from ALDO! Happy Shopping"
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


def reset_all():
    ref = db.reference('/')
    ref.set({})


# reset_all()
# test_runner()
