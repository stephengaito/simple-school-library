
from datetime import date

from schoolLib.htmxComponents.htmx import *
from schoolLib.htmxComponents.tables import *
from schoolLib.htmxComponents.simpleComponents import *

class Form(HtmxChildrenBase) :
  def __init__(self, aComponent, submitMsg, **kwargs) :
    super().__init__(aComponent, **kwargs)
    self.submitButton = Button(submitMsg)

  def collectHtml(self, htmlFragments) :
    htmlFragments.append(f'<form {self.computeHtmxAttrs()}>')
    self.collectChildrenHtml(htmlFragments)
    self.submitButton.collectHtml(htmlFragments)
    htmlFragments.append(f'</form>')

class FormTable(Form) :
  def __init__(self, someInputs, submitMsg, tableKWArgs={}, **kwargs) :
    theTable = Table(someInputs, **tableKWArgs)
    super().__init__(theTable, submitMsg, **kwargs)

class FormInputsBase(HtmxBase) :
  def __init__(
    self,
    name,
    inputType='text',
    label=None,
    value=None,
    defaultValue=None,
    placeholder=None,
    **kwargs
  ) :
    super().__init__(**kwargs)
    if inputType.startswith('t')   : inputType = 'text'
    elif inputType.startswith('c') : inputType = 'color'
    elif inputType.startswith('n') : inputType = 'number'
    elif inputType.startswith('d') : inputType = 'date'
    elif inputType.startswith('s') : inputType = 'search'
    else : inputType  = 'text'
    self.inputType    = inputType
    self.name         = name
    self.value        = value
    self.defaultValue = defaultValue
    self.placeholder  = placeholder
    self.label        = label

  def computeHtmxAttrs(self) :
    fiAttrs = super().computeHtmxAttrs()
    fiAttrs += f' name="{self.name}"'
    if self.value          : fiAttrs += f' value="{self.value}"'
    elif self.placeholder  : fiAttrs += f' placeholder="{self.placeholder}"'
    elif self.defaultValue : fiAttrs += f' value="{self.defaultValue}"'
    return fiAttrs

class FormInputs(FormInputsBase) :
  def collectHtml(self, htmlFragments) :
    if self.label :
      htmlFragments.append(f"""
        <tr>
        <td><label>{self.label}</label></td>
        <td><input type="{self.inputType}" {self.computeHtmxAttrs()}/></td>
        </tr>
      """)
    else :
      htmlFragments.append(f'<input type="{self.inputType}" {self.computeHtmxAttrs()}/>')

class TextInput(FormInputs) :
  def __init__(
    self,
    name,
    label=None,
    value=None,
    defaultValue=None,
    placeholder=None,
    **kwargs
  ) :
    super().__init__(
      name,
      inputType='text',
      label=label,
      value=value,
      defaultValue=defaultValue,
      placeholder=placeholder,
      **kwargs
    )

class NumberInput(FormInputs) :
  def __init__(
    self,
    name,
    label=None,
    value=None,
    defaultValue=None,
    placeholder=None,
    **kwargs
  ) :
    super().__init__(
      name,
      inputType='number',
      label=label,
      value=value,
      defaultValue=defaultValue,
      placeholder=placeholder,
      **kwargs
    )

class ColourInput(FormInputs) :
  def __init__(
    self,
    name,
    label=None,
    value=None,
    defaultValue=None,
    placeholder=None,
    **kwargs
  ) :
    super().__init__(
      name,
      inputType='color',
      label=label,
      value=value,
      defaultValue=defaultValue,
      placeholder=placeholder,
      **kwargs
    )

class DateInput(FormInputs) :
  def __init__(
    self,
    name,
    label=None,
    value=None,
    defaultValue=None,
    placeholder=None,
    **kwargs
  ) :
    if not value : value = today
    super().__init__(
      name,
      inputType='date',
      label=label,
      value=value,
      defaultValue=defaultValue,
      placeholder=placeholder,
      **kwargs
    )

class SearchBox(FormInputs) :
  def __init__(
    self,
    name,
    label=None,
    value=None,
    defaultValue=None,
    placeholder=None,
    **kwargs
  ) :
    super().__init__(
      name,
      inputType='search',
      label=label,
      value=value,
      defaultValue=defaultValue,
      placeholder=placeholder,
      **kwargs
    )

class TextAreaInput(FormInputsBase) :
  def __init__(self, value=None, **kwargs) :
    # for textareas we don't use a value attribute....
    super().__init__(value=None, defaultValue=None, **kwargs)
    self.taValue = value

  def collectHtml(self, htmlFragments) :
    taValue = ""
    if self.value : taValue = self.value

    if self.label :
      htmlFragments.append(f"""
        <tr>
        <td><label>{self.label}</label></td>
        <td><textarea {self.computeHtmxAttrs()}>{taValue}</textarea></td>
        </tr>
      """)
    else :
      htmlFragments.append(
        f'<textarea {self.computeHtmxAttrs()}>{taValue}</textarea>'
      )

class ClassesSelector(HtmxBase) :
  def __init__(
    self,
    sortedClasses,
    name,
    label=None,
    inRow=False,
    **kwargs
  ) :
    raise Exception("not yet implemented!")

#def classesSelector(sortedClasses, label=None, inRow=False, **kwargs) :
#  if 'name' not in kwargs : return "<!-- classesSelector with NO name -->"
#
#  csAttrs = computeHtmxAttrs(
#    'classesSelectorClasses', 'classesSelectorStyles', 'classesSelectorAttrs',
#    kwargs
#  )
#  csAttrs += f' name="{kwargs['name']}"'
#
#  csHtml = [f'<select {csAttrs}>' ]
#  for aClass in sortedClasses :
#    csHtml.append(
#      f'<option value="{kwargs['name']}-{aClass['id']}" {aClass['selected']} style="color: {aClass['colour']};">{aClass['name']}</option>'
#    )
#  csHtml.append('</select>')
#
#  if label :
#    # add the prefixes in reverse order
#    csHtml.insert(0, '<td>')
#    csHtml.insert(0, f'<td><label>{label}</label></td>')
#    csHtml.insert(0, '<tr>')
#    # add the suffic in normal order
#    csHtml.append('</td>')
#    csHtml.append('</tr>')
#
#  return '\n'.join(csHtml)
