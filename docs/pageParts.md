# Page Parts Design

## Goals

1. I want to be able to expose the meta-level page structure by extracting
   the use of `hx-get`, `hx-post`, as well as `hx-swap`. This will tell me
   how the user might be enabled (or not) to interact with the system.

2. This meta-level structure should be exposed as an external YAML file
   (and possibly as a `Dot` graphics file).

## Solutions

1. We will programatically extract this information.

2. We will mock the database as well as our SQL statement classes

   - we will make the SelectSQL class' `.parseResults` method the main
     mocking code. The other *SQL classes will simply be mocked as no-ops.

   - we will keep the existing separation of the 'db' from the *SQL
     classes. To do this the `db` will return a special structure which
     the `.parseResults` method will recognise as the signal to mock its
     own data using the structure declared in the SelectSQL class.

3. We will move the database connection and the call to the existing
   `.response` method to the router wrapper.

4. We need to register all "page part factories"

## Questions

1. We could obtain this meta-level structure by either:

   - declaring this structure via data

   - running the code in a special mode in-order to capture the required
     data.

   IF we declare this structure as data then EITHER we MUST used this
   declared data to *drive* the code OR the declared data and the code
   base will drift.

   IF we run the code and collect the structure, we need to "mock" the
   database. Since we have our SQL queries (and hence all interactions
   with the database) as our own classes, this mocking (and subsequent
   interpreting of the SQL statment's intent) is fairly straight forward.

2. Should the "page part factories" BE sub-classes of the HtmxBase class?

   - as sub-classes, the could be made to automatically register
     themselves as page parts

   - as sub-classes they would implement `collectHtmlFragments`

