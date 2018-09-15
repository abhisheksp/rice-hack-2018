from flask import Flask, request, jsonify
from offers import update_user_offers

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '<h1>Works!</h1>'


@app.route('/update/offers', methods=['POST'])
def update_offers_handler():
    request_body = request.get_json()
    user_id = request_body['user_id']
    emails = request_body['emails']
    update_user_offers(user_id, emails)
    return jsonify({'offers_updated': True})


if __name__ == '__main__':
    app.run()
