import settings
from flask import Flask, request, jsonify, make_response
import docs

app = Flask(__name__)


@app.context_processor
def add_to_context():
    return {
        'base_url': settings.BASE_URL,
        'meta': {},
    }


@app.route("/")
def home():
    return jsonify(hi="hello!")


@app.route("/feedcroc", methods=["POST"])
def save_doc():
    json = request.get_json()

    if json is None:
        response = jsonify(status="error", message="do you even json?")
        response.status_code = 400  # bad request
        return response

    doc = json["doc"]
    if len(doc) > settings.MAX_DOC_SIZE:
        response = {
            "status": "error",
            "message": "nope, that's too large",
        }
        return jsonify(response)

    new_name = docs.save_doc(doc)
    response = {
        "status": "ok",
        "name": new_name,
    }
    return jsonify(response)


@app.route("/<which_doc>", methods=["GET"])
def get_doc(which_doc):
    try:
        doc = docs.get_doc(which_doc)
        doc_body = doc['body']
        return jsonify(content_data)

    except docs.NoDocFound:
        error = {
            "error": True,
            "error_message": "doc not found: {}".format(which_doc),
        }
        return make_response(jsonify(error), 404)


if __name__ == "__main__":
    app.debug = settings.DEBUG
    print("Will listen on {0}:{1}".format(settings.HOST, settings.PORT))
    app.run(host=settings.HOST, port=settings.PORT)
