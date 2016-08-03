import settings
from flask import Flask, request, jsonify
from docs import saveDoc, getDoc, NoDocFound

app = Flask(__name__)

@app.route("/")
def home():
    resonse = {
        "status": "hi",
        "message": "hello, how are you?",
    }
    return jsonify(resonse)

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

    new_name = saveDoc(doc)
    response = {
        "status": "ok",
        "name": new_name,
    }
    return jsonify(response)


@app.route("/doc/<which_doc>", methods=["GET"])
def get_doc(which_doc):
    response = {}
    try:
        doc = getDoc(which_doc)
        response = {
            "status": "ok",
            "name": which_doc,
            "doc": doc["doc"],
        }

    except NoDocFound:
        response = {
            "status": "error",
            "message": "couldn't find that"
        }

    finally:
        return jsonify(response)



if __name__ == "__main__":
    app.debug = settings.DEBUG
    print("Will listen on {0}:{1}".format(settings.HOST, settings.PORT))
    app.run(host=settings.HOST, port=settings.PORT)
