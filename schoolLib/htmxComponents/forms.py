
import yaml

from schoolLib.htmxComponents.jinja import jinja2env

def buildForm(formName, formDesc, aFile) :
  formLines = []
  try :
    formLines.append(
      jinja2env.get_template('formHeader'
      ).render(formDesc)
    )
    for anItem in formDesc['items'] :
      if 'component' not in anItem : anItem['component'] = 'textInput'
      formLines.append(
        jinja2env.get_template(anItem['component']
        ).render(anItem)
      )
    formLines.append(
      jinja2env.get_template('formFooter'
      ).render(formDesc)
    )
  except Exception as err :
    print(f"Could not render a component template for {formName}")
    print(repr(err))
    print(yaml.dump(formDesc))
  aFile.write("\n".join(formLines))
