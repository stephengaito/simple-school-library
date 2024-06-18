# Simple School Library

## Database structure

- classes
  - classesID (unique primary key)
  - className

- borrowers (all text fields searchable)
  - borrowersID (unique primary key)
  - First name
  - Other names
  - Family name
  - cohort
  - classID

- itemsInfo (all text fields searchable)
  - itemsInfoID  (unique primary key)
  - isbn
  - deweyDecimal
      SELECT
        author, title, biblio_metadata.metadata
      FROM biblio, biblio_metadata
      WHERE biblio.biblionumber = biblio_metadata.biblionumber

      The DDC is located as the value in the datafield tag="082" code="a"
      it the metadata field which is itself an XML structure.

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
  - borrowersID
  - itemsInfoID
  - itemsPhysicalID
  - dateBorrowed
  - dateDue
