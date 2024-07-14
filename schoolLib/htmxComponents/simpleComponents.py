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
  text = getFromKWArgs('text', 'unknown', kwargs)
  htmxAttrs = computeHtmxAttrs(
    buttonClasses, buttonStyles, buttonAttrs, kwargs
  )

  return f"<button {htmxAttrs}>{text}</button>"


divClasses = {
  'default' : ['m-1']
}
divStyles  = {}
divAttrs   = {}

def htmxDiv(children, **kwargs) :
  htmxAttrs = computeHtmxAttrs(divClasses, divStyles, divAttrs, kwargs)

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

def htmxMenu(
  menuList,
  selected="",
  hxAttrs={'hx-target': '#level0div' },
  **kwargs
):
  htmxAttrs = computeHtmxAttrs(menuClasses, menuStyles, menuAttrs, kwargs)

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

formClasses = {
  'default' : ['pl-8', 'pt-4',
  'border-2', 'border-solid', 'border-blue-500', 'rounded-lg']
}
formStyles  = {}
formAttrs   = {}

def htmxForm(inputs, submitMsg, **kwargs) :
  fAttrs   = computeHtmxAttrs(
    formClasses, formStyles, formAttrs, kwargs
  )
  bAttrs = computeHtmxAttrs(
    buttonClasses, buttonStyles, buttonAttrs, {}
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

textInputClasses = {}
textInputStyles  = {}
textInputAttrs   = {}

def textInput(label=None, **kwargs) :
  if 'name' not in kwargs : return "<!-- textInput with NO name -->"

  tiAttrs = computeHtmxAttrs(
    textInputClasses, textInputStyles, textInputAttrs, kwargs
  )
  tiAttrs += addInputAttrs(kwargs)

  return getInputHtml('text', tiAttrs, label=label)

numberInputClasses = {}
numberInputStyles  = {}
numberInputAttrs   = {}

def numberInput(label=None, **kwargs) :
  if 'name' not in kwargs : return "<!-- numberInput with NO name -->"

  niAttrs = computeHtmxAttrs(
    numberInputClasses, numberInputStyles, numberInputAttrs, kwargs
  )
  niAttrs += addInputAttrs(kwargs)

  return getInputHtml('number', niAttrs, label=label)

colourInputClasses = {}
colourInputStyles  = {}
colourInputAttrs   = {}

def colourInput(label=None, **kwargs) :
  if 'name' not in kwargs : return "<!-- colourInput with NO name -->"

  ciAttrs = computeHtmxAttrs(
    colourInputClasses, colourInputStyles, colourInputAttrs, kwargs
  )
  ciAttrs += addInputAttrs(kwargs)

  return getInputHtml('color', ciAttrs, label=label)
