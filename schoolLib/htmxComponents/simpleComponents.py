import yaml

from schoolLib.htmxComponents.utils import *

def button(**kwargs) :
  text = getFromKWArgs('text', 'unknown', kwargs)
  bAttrs = computeHtmxAttrs(
    'buttonClasses', 'buttonStyles', 'buttonAttrs', kwargs
  )

  return f"<button {bAttrs}>{text}</button>"

def div(children, **kwargs) :
  dAttrs = computeHtmxAttrs('divClasses', 'divStyles', 'divAttrs', kwargs)

  if not isinstance(children, list) : children = [ children ]
  divHtml = [ f'<div {dAttrs}>' ]
  for aChild in children :
    divHtml.append(computeComponent(aChild))
  divHtml.append('</div>')
  return '\n'.join(divHtml)

# we defined a set of level divs which each act as replacement points.

# The intent is that each larger number should be nested inside the lower
# numbers, so that only the dom which needs to be replaced can be
# replaced.

def level0div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level0div'
  return div(children, **kwargs)

def level1div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level1div'
  return div(children, **kwargs)

def level2div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level2div'
  return div(children, **kwargs)

def level3div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level3div'
  return div(children, **kwargs)

def level4div(children, **kwargs) :
  if 'theId' not in kwargs : kwargs['theId'] = 'level4div'
  return div(children, **kwargs)

def menu(
  menuList,
  selected="",
  target='#level0div',
  swap='outerHTML',
  **kwargs
):
  #kwargs['target'] = target
  #kwargs['swap']   = swap
  mAttrs = computeHtmxAttrs(
    'menuClasses', 'menuStyles', 'menuAttrs', kwargs
  )

  menuList = selectComponentInList(selected, menuList)
  menuListHtml = [ f'<div {mAttrs}>' ]
  for anItem in menuList :
    if isinstance(anItem, dict) :
      if 'target' not in anItem : anItem['target'] = target
      if 'swap'   not in anItem : anItem['swap']   = swap
    menuListHtml.append(computeComponent(anItem))
  menuListHtml.append('</div>')
  return '\n'.join(menuListHtml)

def text(someText, type=None, **kwargs) :
  tAttrs = computeHtmxAttrs(
    'textClasses', 'textStyles', 'textAttrs', kwargs
  )

  if isinstance(someText, list) :
    someTextHtml = []
    for aPart in someText :
      someTextHtml.append(computeComponent(aPart))
    someText = ' '.join(someTextHtml)

  textHtml = [ someText ]
  if type :
    if type.startswith('p') :
      textHtml.insert(0, f'<p {tAttrs}>')
      textHtml.append('</p>')
    elif type.startswith('s') :
      textHtml.insert(0, f'<span {tAttrs}>')
      textHtml.append('</span>')
    else :
      textHtml.insert(0, f'<div {tAttrs}>')
      textHtml.append('</div>')

  return '\n'.join(textHtml)

def link(url, text, method='get', **kwargs) :
  lAttrs = ""
  if 'target' not in kwargs : lAttrs = f'href="{url}" '
  else                      : kwargs[method] = url
  lAttrs += computeHtmxAttrs(
    'linkClasses', 'linkStyles', 'linkAttrs', kwargs
  )
  return f'<a {lAttrs}>{text}</a>'
