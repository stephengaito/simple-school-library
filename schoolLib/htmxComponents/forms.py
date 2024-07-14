
from schoolLib.htmxComponents.utils import *

def htmxForm(inputs, submitMsg, **kwargs) :
  fAttrs   = computeHtmxAttrs(
    theme['formClasses'], theme['formStyles'], theme['formAttrs'], kwargs
  )
  bAttrs = computeHtmxAttrs(
    theme['buttonClasses'], theme['buttonStyles'], theme['buttonAttrs'],
    {}
  )
  tAttrs = computeHtmxAttrs(
    theme['tableClasses'], theme['tableStyles'], theme['tableAttrs'],
    {}
  )

  formHtml = [ f'<form {fAttrs}><table {tAttrs}>' ]
  for anInput in inputs :
    formHtml.append(computeComponent(anInput))
  formHtml.append(f"""
  </table>
  <button {bAttrs}>{submitMsg}</button>
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
  inputHtml = ['<tr>']
  if label : inputHtml.append(f"<td><label>{label}</label></td>")
  inputHtml.append(f'<td><input type="{inputType}" {inputAttrs} /></td>')
  inputHtml.append('</tr>')
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
