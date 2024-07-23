
# We need to be VERY careful with ANY imports
from schoolLib.htmxComponents import *

TopLevelMenu = Menu([
  Button(
    'Home',
    theId = 'home',
    get='/menu/home',
    target='#level0div'
  ),
  Button(
    'Books',
    theId = 'books',
    get = "/menu/books",
    target='#level0div'
  ),
  Button(
    'People',
    theId = 'people',
    get = '/menu/people',
    target='#level0div'
  ),
  Button(
    'Tasks',
    theId = 'tasks',
    get = '/menu/tasks',
    target='#level0div'
  )
])

SecondLevelBooksMenu = Menu([
  Button(
    'Take out a book',
    theId  = 'takeOut',
    get    = '/menu/books/takeOut',
    target = '#level1div'
  ),
  Button(
    'Return a book',
    theId  = 'return',
    get    = '/menu/books/return',
    target = '#level1div'
  ),
  Button(
    'Renew a book',
    theId  = 'renew',
    get    = '/menu/books/renew',
    target = '#level1div'
  ),
  Button(
    'Find a book',
    theId  = 'findBook',
    get    = '/search/items',
    target = '#level1div'
  ),
  Button(
    'Add a book',
    theId  = 'addBook',
    get    = '/itemsInfo/new',
    target = '#level1div'
  )
])

SecondLevelPeopleMenu = Menu([
  Button(
    'Add a class',
    theId  = 'addClass',
    get    = '/menu/people/addClass',
    target = '#level1div'
  ),
  Button(
    'List classes',
    theId  = 'listClasses',
    get    = '/menu/people/listClasses',
    target = '#level1div'
  ),
  Button(
    'Add a person',
    theId  = 'addBorrower',
    get    = '/menu/people/addBorrower',
    target = '#level1div'
  ),
  Button(
    'Find a person',
    theId  = 'findBorrower',
    get    = '/search/borrowers',
    target = '#level1div'
  )
])

SecondLevelTasksMenu = Menu([
  Button(
    'Books checked out',
    theId  = 'booksCheckedOut',
    get    = '/menu/tasks/booksCheckedOut',
    target = '#level1div'
  )
])
