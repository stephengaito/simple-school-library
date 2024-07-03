
import os
import sys
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape

jinja2env = Environment(
  loader=PackageLoader("schoolLib.htmxComponents"),
  autoescape=select_autoescape(),
  block_start_string="<%",
  block_end_string="%>",
  variable_start_string="<=",
  variable_end_string="=>",
  comment_start_string="<#",
  comment_end_string="#>",
  trim_blocks=True,
  lstrip_blocks=True
)

def loadTemplateYaml() :
  templates = {}
  yamlPath = os.path.join(
    os.path.dirname(__file__),
    'templates.yaml'
  )
  with open(yamlPath) as yamlFile :
    templates = yaml.safe_load(yamlFile.read())
  return templates

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

def cli() :
  templates = loadTemplateYaml()

  for aTemplateName, aTemplateDesc in templates.items() :
    print(f"\nworking on: {aTemplateName}")
    if 'path' not in aTemplateDesc : aTemplateDesc['path'] = ''
    templatePath = os.path.join(
      os.path.dirname(os.path.dirname(__file__)),
      'templates',
      aTemplateDesc['path'],
      aTemplateName+'.html'
    )
    print(f"writing to: {templatePath}")
    with open(templatePath, 'w') as tFile :
      if aTemplateDesc['type'] == 'form' :
        buildForm(aTemplateName, aTemplateDesc, tFile)
