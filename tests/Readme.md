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

## ToDo

Use the `routes`, `pageParts` as computed by `computePagePartUsers` from
`schools.setup.router` to obtain both the entry points as well as those
pageParts which call them. Then make sure all such entry points actually exist.

Then slowly work through the "most important" pageParts ensuring they return
what is expected.

Then slowly work through each python file correcting any pycodestyle problems.


