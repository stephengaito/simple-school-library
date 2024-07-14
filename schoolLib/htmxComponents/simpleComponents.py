import yaml

from schoolLib.htmxComponents.utils import *

def button(**kwargs) :
  text = getFromKWArgs('text', 'unknown', kwargs)
  htmxAttrs = computeHtmxAttrs(
    theme['buttonClasses'], theme['buttonStyles'], theme['buttonAttrs'],
    kwargs
  )

  return f"<button {htmxAttrs}>{text}</button>"

def htmxDiv(children, **kwargs) :
  htmxAttrs = computeHtmxAttrs(
    theme['divClasses'], theme['divStyles'], theme['divAttrs'], kwargs
  )

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

def htmxMenu(
  menuList,
  selected="",
  hxAttrs={'hx-target': '#level0div' },
  **kwargs
):
  htmxAttrs = computeHtmxAttrs(
    theme['menuClasses'], theme['menuStyles'], theme['menuAttrs'], kwargs
  )

  if 'hx-swap' not in hxAttrs : hxAttrs['hx-swap'] = 'outerHTML'

  menuList = selectComponentInList(selected, menuList)
  menuListHtml = [ f'<div {htmxAttrs}>' ]
  for anItem in menuList :
    if isinstance(anItem, dict) :
      if 'attrs' not in anItem : anItem['attrs'] = {}
      anItem['attrs'].update(hxAttrs)
    menuListHtml.append(computeComponent(anItem))
  menuListHtml.append('</div>')
  return '\n'.join(menuListHtml)
