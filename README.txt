croc.doc is the backend service that saves the docs fed to the croc in croc.farm.

## Run it

After all of the `pip install -r requirements.txt` ordeal (you might need
some dev packages as well to compile some pips), do this:

    python main.py

This will run the production version of the service so you don't accidentally
run development code on a production machine. To debug, define a `DEBUG=1`
environment variable. Or:

    DEBUG=1 python main.py


### Database (Postgres)

Use environment variable DATABASE_URL, like: 'postgresql+psycopg2://postgres:@localhost:5432/crocfarm' (the default when not provided).


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

