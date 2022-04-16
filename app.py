from flask import Flask, jsonify, request, abort, render_template
from flask_restful import Resource, Api
from marshmallow import Schema, fields
from summarizer import *
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
api = Api(app)

class SummarizeQuerySchema(Schema):
    text = fields.Str(required=True)
    required_summary_length = fields.Int(required=True)

class ScrapeQuerySchema(Schema):
    URL = fields.Str(required=True)

schema = SummarizeQuerySchema()
scrape_schema = ScrapeQuerySchema()

class Summarize(Resource):
    def get(self):
        errors = schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        text = request.args["text"]
        required_summary_length = int(request.args["required_summary_length"])
        summary = summarize(text, required_summary_length)
        return jsonify({"summary" : summary})

class ScrapeText(Resource):
    def get(self):
        errors = scrape_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        URL = request.args["URL"]
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all(['h1', 'p'])
        text = [result.text for result in results]
        scraped_text = ' '.join(text)
        return jsonify({"scraped_text" : scraped_text})

api.add_resource(Summarize, "/summarize")
api.add_resource(ScrapeText, "/scrape-text")

@app.route("/")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)