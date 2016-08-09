This is what runs croc.farm. It is called croc.doc after the docs it manages.

# frontend:

You build stuff with `npm` and `gulp`.  
`npm i` and `gulp dev` (will add more commands later, this is a watch thing).
This will create `backend/static` with the appropriate entries and also copy the
ninja template from `frontend/index.html` to `backend/templates/index.html`.

# backend:

stuff. stfu.

## Run it

After all of the `pip install -r requirements.txt` ordeal (you might need
some dev packages as well to compile some pips), do this:

    python main.py

This will run the production version of the service so you don't accidentally
run development code on a production machine. To debug, define a `DEBUG=1`
environment variable. Or:

    DEBUG=1 python main.py


Will automatically connect to host 'mongo' for mongo stuff (use with Docker).
Change this with env var MONGO_URL=mongodb://yourhost.

## Web interface

endpoints:
/               just says hello
/doc            POST: post new doc, returns json*
/doc/<name>     GET: get a doc, returns json*

POST: Should be Content-Type: application/json

*json:
{
    "status": ["ok", "error", "hi"],
    "doc": <the doc itself, when GETing>,
    "name": <name of the doc>,
    "message": <some greeting, optional>
}


# frontend

npm install and gulp and such, currently there's `gulp js`
