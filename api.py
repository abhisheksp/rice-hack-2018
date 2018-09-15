import flask
from offers import update_offers

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    update_offers()
    return "<h1>Offers Updated!</p>"

app.run()