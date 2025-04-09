# Testing

## What to sanity check

- Check the database schema

- Untested pageParts that interact with the database.

- Check all routes have a corresponding pagePart

## What to pytest

- Database updates (Highest priority)

  - All known database updates are applied by the database pytests
    fixture.

  - Need to compare this updated database against the schema (and other
    wise test its initial sanity).

- Database interactions (High priority)

  - The `findPagePartsUsingSql` sanity check lists all untested sql using
    pageParts. We test these pageParts by calling them using mocked
    `callWithParameters` and then check the database to confirm the
    appropriate changes have been made.

- HtmlComponents returned by each pagePart (medium priority unless
  something goes wrong)

- Each HtmxComponent (low priority unless something goes wrong)

- General usage "tests" (on going)

## Strategy

The bulk of the testing will be done by calling appropriate `pageParts`
with fabricated `pageData` objects. By doing this we will essentially be
integration testing using the application's "front-end" to manipulate the
underlying database.

Since we are using an SQLite3 database, we can ensure that, for testing,
we are using an in-memory database. To do this, however, we need to
reliably (re)populate the database with reasonably valid data.

This means that we need to make extensive use `pytest`'s `fixtures` and in
particular `pytest`'s fixture dependencies system. This will ensure we can
have a large number of small "fixtures" which add known data to the
database in an appropriate order.

By using `pageParts`, the returned values will be `HtmxComponent`
structures, which can be directly tested to ensure we are presenting to
the user a known UI.

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
pageParts which call them. Then make sure all such entry points actually
exist.

Then slowly work through the "most important" pageParts ensuring they
return what is expected.

Then slowly work through each python file correcting any pycodestyle
problems.


