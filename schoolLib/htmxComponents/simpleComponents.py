import yaml

from schoolLib.htmxComponents.utils import *

buttonClasses = {
  'default'  : [
    'p-1', 'm-1',
    'border-2', 'border-solid', 'rounded-lg'
  ],
  'selected' : [
    'p-1','m-1',
    'border-2', 'border-solid', 'border-blue-500', 'rounded-lg',
    'outline', 'outline-offset-1', 'outline-2', 'outline-blue-500'
  ],
}
buttonStyles  = {}
buttonAttrs   = {}

def button(**kwargs) :
  addDictsToKWArgs(buttonClasses, buttonStyles, buttonAttrs, kwargs)
  text = getFromKWArgs('text', 'unknown', kwargs)
  htmxAttrs = computeHtmxAttrs(kwargs)

  return f"<button {htmxAttrs}>{text}</button>"


divClasses = {
  'default' : ['m-1']
}
divStyles  = {}
divAttrs   = {}

def htmxDiv(children, **kwargs) :
  addDictsToKWArgs(divClasses, divStyles, divAttrs, kwargs)
  htmxAttrs = computeHtmxAttrs(kwargs)

  if not isinstance(children, list) : children = [ children ]
  someHtml = []
  for aChild in children :
    someHtml.append(computeComponent(aChild))
  someHtml = '\n'.join(someHtml)
  return f"""
  <div {htmxAttrs}>
  {someHtml}
  </div>
  """

# we defined a set of level divs which each act as replacement points.

# The intent is that each larger number should be nested inside the lower
# numbers, so that only the dom which needs to be replaced can be
# replaced.

def level0div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level0div'
  return htmxDiv(children, **kwargs)

def level1div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level1div'
  return htmxDiv(children, **kwargs)

def level2div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level2div'
  return htmxDiv(children, **kwargs)

def level3div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level3div'
  return htmxDiv(children, **kwargs)

def level4div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level4div'
  return htmxDiv(children, **kwargs)

menuClasses = {
  'default' : ['m-1']
}
menuStyles  = {}
menuAttrs   = {}

def menu(menuList, selected="", **kwargs):
  addDictsToKWArgs(menuClasses, menuStyles, menuAttrs, kwargs)
  htmxAttrs = computeHtmxAttrs(kwargs)

  menuList = selectComponentInList(selected, menuList)
  menuListHtml = [ f'<div {htmxAttrs}>' ]
  for anItem in menuList :
    menuListHtml.append(computeComponent(anItem))
  menuListHtml.append('</div>')
  return '\n'.join(menuListHtml)
