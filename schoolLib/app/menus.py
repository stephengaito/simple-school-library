
# There should not be ANY imports

topLevelMenu = [
  { 'component' : 'button',
    'c-name' : 'home',
    'text' : 'Home',
    'get' : '/menu/home',
  },
  { 'component' : 'button',
    'c-name' : 'books',
    'text' : 'Books',
    'get' : "/menu/books",
  },
  { 'component' : 'button',
    'c-name' : 'people',
    'text' : 'People',
    'get' : '/menu/people',
  },
  { 'component' : 'button',
    'c-name' : 'tasks',
    'text' : 'Tasks',
    'get' : '/menu/tasks',
  }
]

secondLevelBooksMenu = [
  { 'component' : 'button',
    'c-name' : 'takeOut',
    'text' : 'Take out a book',
    'get'  : '/menu/books/takeOut'
  },
  { 'component' : 'button',
    'c-name' : 'return',
    'text' : 'Return a book',
    'get'  : '/menu/books/return'
  },
  { 'component' : 'button',
    'c-name' : 'renew',
    'text' : 'Renew a book',
    'get'  : '/menu/books/renew'
  },
  { 'component' : 'button',
    'c-name' : 'find',
    'text' : 'Find a book',
    'get'  : '/menu/books/find'
  },
]

secondLevelPeopleMenu = [
  { 'component' : 'button',
    'c-name' : 'addClass',
    'text' : 'Add a class',
    'get'  : '/menu/people/addClass'
  },
  { 'component' : 'button',
    'c-name' : 'listClasses',
    'text' : 'List classes',
    'get'  : '/menu/people/listClasses'
  },
  { 'component' : 'button',
    'c-name' : 'addBorrower',
    'text' : 'Add a person',
    'get'  : '/menu/people/addBorrower'
  },
  { 'component' : 'button',
    'c-name' : 'findBorrower',
    'text' : 'Find a person',
    'get'  : '/menu/people/addBorrower'
  },
]

secondLevelTasksMenu = [
  { 'component' : 'button',
    'c-name' : 'booksCheckedOut',
    'text' : 'Books checked out',
    'get'  : '/menu/tasks/booksCheckedOut'
  },
]
