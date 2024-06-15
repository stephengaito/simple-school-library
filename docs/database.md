# Simple School Library

## Database structure

- people (all text fields searchable)
  - peopleID (unique primary key)
  - First name
  - Other names
  - Family name
  - cohort
  - classID

- classes
  - classesID (unique primary key)
  - className

- itemsInfo (all text fields searchable)
  - itemsInfoID  (unique primary key)
  - isbn
  - deweyDecimal
  - Title
  - Authors
  - PublisherInfo
  - itemType
  - Keywords
  - Series
  - Summary

- itemsPhysical
  - itemsPhysicalID (unique primary key)
  - barcode
  - dateAdded
  - Status
    - Lost
    - Withdrawn
  - dateLastSeen

- itemsBorrowed
  - itemsBorrowedID (unique primary key)
  - personID
  - itemsInfoID
  - itemsPhysicalID
  - dateBorrowed
  - dateDue
