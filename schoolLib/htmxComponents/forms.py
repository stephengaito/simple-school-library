
from schoolLib.htmxComponents.utils import *
from schoolLib.htmxComponents.tables import *

def form(aComponent, submitMsg, **kwargs) :
  fAttrs   = computeHtmxAttrs(
    'formClasses', 'formStyles', 'formAttrs', kwargs
  )

  bKWArgs = {}
  if 'buttonKWArgs' in kwargs : bKWArgs = kwargs['buttonKWArgs']
  bAttrs = computeHtmxAttrs(
    'buttonClasses', 'buttonStyles', 'buttonAttrs', bKWArgs
  )

  formHtml = [ f'<form {fAttrs}>' ]
  formHtml.append(computeComponent(aComponent))
  formHtml.append(f"""
  <button {bAttrs}>{submitMsg}</button>
  </form>
  """)
  return '\n'.join(formHtml)

def formTable(inputs, submitMsg, **kwargs) :
  tKWArgs = {}
  if 'tableKWArgs' in kwargs : tKWArgs = kwargs['tableKWArgs']

  return form(
    table(inputs, **tKWArgs),
    submitMsg, **kwargs
  )


def addInputAttrs(kwargs) :
  inputAttrs = f' name="{kwargs['name']}"'
  if 'value' in kwargs and kwargs['value'] :
    inputAttrs += f' value="{kwargs['value']}"'
  elif 'placeholder' in kwargs and kwargs['placeholder'] :
    inputAttrs += f' placeholder="{kwargs['placeholder']}"'
  elif 'defaultValue' in kwargs :
    inputAttrs += f' value="{kwargs['defaultValue']}"'
  return inputAttrs

# We cheat here...
# IF a label has been specified,
#  THEN we wrap everything in tableEntries inside a tableRow
# IF NO label has been specified,
#  THEN we do not add any tableEntries or tableRows
#
def getInputHtml(inputType, inputAttrs, label=None, inRow=True) :
  inputHtml = []
  if label :
    inputHtml.append('<tr>')
    inputHtml.append(f"<td><label>{label}</label></td>")
    inputHtml.append(f'<td><input type="{inputType}" {inputAttrs} /></td>')
    inputHtml.append('</tr>')
  else :
    inputHtml.append(f'<input type="{inputType}" {inputAttrs} />')
  return '\n'.join(inputHtml)

def textInput(label=None, **kwargs) :
  if 'name' not in kwargs : return "<!-- textInput with NO name -->"

  tiAttrs = computeHtmxAttrs(
    'textInputClasses', 'textInputStyles', 'textInputAttrs', kwargs
  )
  tiAttrs += addInputAttrs(kwargs)

  return getInputHtml('text', tiAttrs, label=label)

def numberInput(label=None, **kwargs) :
  if 'name' not in kwargs : return "<!-- numberInput with NO name -->"

  niAttrs = computeHtmxAttrs(
    'numberInputClasses', 'numberInputStyles', 'numberInputAttrs',
    kwargs
  )
  niAttrs += addInputAttrs(kwargs)

  return getInputHtml('number', niAttrs, label=label)

def colourInput(label=None, **kwargs) :
  if 'name' not in kwargs : return "<!-- colourInput with NO name -->"

  ciAttrs = computeHtmxAttrs(
    'colourInputClasses', 'colourInputStyles', 'colourInputAttrs',
    kwargs
  )
  ciAttrs += addInputAttrs(kwargs)

  return getInputHtml('color', ciAttrs, label=label)

def classesSelector(sortedClasses, label=None, inRow=False, **kwargs) :
  if 'name' not in kwargs : return "<!-- classesSelector with NO name -->"

  csAttrs = computeHtmxAttrs(
    'classesSelectorClasses', 'classesSelectorStyles', 'classesSelectorAttrs',
    kwargs
  )
  csAttrs += f' name="{kwargs['name']}"'

  csHtml = [f'<select {csAttrs}>' ]
  for aClass in sortedClasses :
    csHtml.append(
      f'<option value="{kwargs['name']}-{aClass['id']}" {aClass['selected']}>{aClass['name']}</option>'
    )
  csHtml.append('</select>')

  if label :
    # add the prefixes in reverse order
    csHtml.insert(0, '<td>')
    csHtml.insert(0, f'<td><label>{label}</label></td>')
    csHtml.insert(0, '<tr>')
    # add the suffic in normal order
    csHtml.append('</td>')
    csHtml.append('</tr>')

  return '\n'.join(csHtml)