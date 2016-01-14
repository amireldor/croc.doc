This is docservice "croc.doc", manages named docs for croc.farm on a mongo

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

