from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api
from marshmallow import Schema, fields
from summarizer import *

app = Flask(__name__)
api = Api(app)

class SummarizeQuerySchema(Schema):
    text = fields.Str(required=True)
    required_summary_length = fields.Int(required=True)

schema = SummarizeQuerySchema()

class Summarize(Resource):
    def get(self):
        errors = schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        text = request.args["text"]
        required_summary_length = int(request.args["required_summary_length"])
        summary, original_text_length = generate_summary(text, required_summary_length)
        return jsonify({"summary" : summary, "original_text_length" : original_text_length})

api.add_resource(Summarize, "/summarize")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)