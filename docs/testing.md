# Testing.....

We need to test the simple school library system at a number of levels:

1. Raw HTML to ensure the forms returned contain:
   - basic htmx referents
   - required fields/content

2. "Visual layout" contains the correct div's

3. Interaction

## Access to the starlette app.

Our `setup/router.py` module keeps a complete and programatically
accessible list of all of the starlette entry points and the corresponding
python methods. We can use this information to "Unit" test each of the
entry points, individually or in "sane" sequences.

## Test descriptions

Can we keep the test descriptions as a collection of YAML files which then
drive a fairly generic test harness?

A test description would be a setup, a collection of probes
(csselect->value (with equal, contains,...)), followed by a teardown?

Some of our tests will also be setting up the database for subsequent
tests. How to we show the dependency of these tests? AND then randomise
all tests which are independent (at a given "level").

How do we make test creation as easy as possible? To do this we need to be
able to interact with the test harness and see the results. That is we
need some sort of "break-point" mechanism so we can inspect a test and its
results. We might also want to be able to skip one or more tests.

Alternatively, we might best simply use PyTest for what it is good at...
which is using Python to describe setup and tear-down.

So we might use test-harness "parts" to do the probe testing. Doing this
we might have a list of probes (which could be probed in a random order)
with each probe being a ProbeClass specific to the "thing"/"value" being
probed/checked.

## Database

Our database of borrowers and items is an integral part of the system.

Do we use an in memory or on disk database for testing.

If it is on disk we need to ensure we do not test with the live database.

Either way, we need to ensure we have a database with a sane structure.

## Resources

- [pytest documentation](https://docs.pytest.org/en/stable/)

- [unittest — Unit testing framework — Python 3.13.0
documentation](https://docs.python.org/3/library/unittest.html)

- [How do you generate dynamic (parameterized) unit tests in Python? -
Stack
Overflow](https://stackoverflow.com/questions/32899/how-do-you-generate-dynamic-parameterized-unit-tests-in-python)

- [tdd - Python library 'unittest': Generate multiple tests
programmatically - Stack
Overflow](https://stackoverflow.com/questions/2798956/python-library-unittest-generate-multiple-tests-programmatically)

- [Dynamically generating Python test cases - Eli Bendersky's
website](https://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases)

- [wolever/parameterized: Parameterized testing with any Python test
framework](https://github.com/wolever/parameterized)
