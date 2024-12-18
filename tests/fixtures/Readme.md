# Using PyTest Fixtures to populate a database

We will use `pytest`'s `fixtures` to reliably populate our in-memory
testing SQLite3 database.

Since there is inherent interdependency between the data stored in our
database, we need to ensure that this data gets entered in the correct
order. For example, in order to add a borrower, we must already have
classes into which a new borrower can be assigned. Equally, to be able to
take a book out, we must have both the book to be taken out as well as the
borrower who is taking the book out.

These interdependencies can be expressed by `pytest`'s fixture dependency
system. This allows us to have small focused fixture "parts" which get
chained into the correct order to populate the in-memory database. 

Since we are ultimately manipulating a database by using an HTTP POST api,
each fixture part will require that we specify a POST FORM. We store this
structured FORM data in various YAML structures (either on disk or in a
string in the pytest fixture definition.

Since we are using `pageParts` as our testing api, to provide the required
HTTP Request as well as any POST FORMS, we fabricate a
`schoolLib.setup.router:PageData` object with the required data. We do
this by subclassing the `schoolLib.setup.router:PageData` class, an
providing appropriate constructors.

