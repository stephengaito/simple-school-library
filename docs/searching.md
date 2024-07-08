# Simple School Library searching database

For most purposes we simply use indices...

For full text searching see: [SQLite FTS5
Extension](https://sqlite.org/fts5.html)

- **classes** : too small to be bothered?

- **borrowers** :
  - borrower number (already indexed as primary key?)
  - combined **full text search** on:
    - firstName
    - familyName

- **itemsBorrowed** :

- **itemsInfo** :
  - isbn (indexed)
  - combined **full text search** on:
    - title
    - authors
    - keywords
    - summary
    - type
    - publisher
    - series

- **itemsPhysical** :
  - barcode (indexed)
  - combined **full text search** on:
    - status?


## Questions:

- Do we need a reindex function?
  Should this be run automaticall periodicall?
