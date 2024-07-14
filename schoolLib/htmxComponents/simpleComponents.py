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

def htmxForm(inputs, submitMsg, **kwargs) :
  fAttrs   = computeHtmxAttrs(
    theme['formClasses'], theme['formStyles'], theme['formAttrs'], kwargs
  )
  bAttrs = computeHtmxAttrs(
    theme['buttonClasses'], theme['buttonStyles'], theme['buttonAttrs'],
    {}
  )

  formHtml = [ f'<form {fAttrs}>' ]
  for anInput in inputs :
    formHtml.append(computeComponent(anInput))
  formHtml.append(f"""  <button {bAttrs}>{submitMsg}</button>
  </form>
  """)
  return '\n'.join(formHtml)

def addInputAttrs(kwargs) :
  inputAttrs = f' name="{kwargs['name']}"'
  if 'value' in kwargs and kwargs['value'] :
    inputAttrs += f' value="{kwargs['value']}"'
  elif 'placeholder' in kwargs and kwargs['placeholder'] :
    inputAttrs += f' placeholder="{kwargs['placeholder']}"'
  elif 'defaultValue' in kwargs :
    inputAttrs += f' value="{kwargs['defaultValue']}"'
  return inputAttrs

def getInputHtml(inputType, inputAttrs, label=None) :
  inputHtml = ['<div>']
  if label : inputHtml.append(f"<label>{label}</label>")
  inputHtml.append(f'<input type="{inputType}" {inputAttrs} />')
  inputHtml.append('</div>')
  return '\n'.join(inputHtml)

def textInput(label=None, **kwargs) :
  if 'name' not in kwargs : return "<!-- textInput with NO name -->"

  tiAttrs = computeHtmxAttrs(
    theme['textInputClasses'],
    theme['textInputStyles'],
    theme['textInputAttrs'],
    kwargs
  )
  tiAttrs += addInputAttrs(kwargs)

  return getInputHtml('text', tiAttrs, label=label)

def numberInput(label=None, **kwargs) :
  if 'name' not in kwargs : return "<!-- numberInput with NO name -->"

  niAttrs = computeHtmxAttrs(
    theme['numberInputClasses'],
    theme['numberInputStyles'],
    theme['numberInputAttrs'],
    kwargs
  )
  niAttrs += addInputAttrs(kwargs)

  return getInputHtml('number', niAttrs, label=label)

def colourInput(label=None, **kwargs) :
  if 'name' not in kwargs : return "<!-- colourInput with NO name -->"

  ciAttrs = computeHtmxAttrs(
    theme['colourInputClasses'],
    theme['colourInputStyles'],
    theme['colourInputAttrs'],
    kwargs
  )
  ciAttrs += addInputAttrs(kwargs)

  return getInputHtml('color', ciAttrs, label=label)
