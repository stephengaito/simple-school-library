# Testing

## Testing the HTML

We can use [xml.etree.ElementTree — The ElementTree XML API — Python
3.12.4
documentation](https://docs.python.org/3/library/xml.etree.elementtree.html)
and most especially the [xml.etree.ElementTree — The ElementTree XML API
— Python 3.12.4
documentation](https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support)
to test for the presence of individual elements inthe HTML.

We can use the [Test Client -
Starlette](https://www.starlette.io/testclient/) to mock the full ASGI
stack for our app.

We could either use a ":memory:" SQLite3 database, or load a simple
database from YAML, or dumped SQL to test our app against.
