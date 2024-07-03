
import glob
import os
import sys
import yaml

from schoolLib.htmxComponents.forms import buildForm

def loadTemplateYaml() :
  templates = {}
  yamlGlob = os.path.join(
    os.path.dirname(__file__),
    'yaml',
    '*.yaml'
  )
  for aYamlPath in glob.iglob(yamlGlob) :
    with open(aYamlPath) as yamlFile :
      templates.update(yaml.safe_load(yamlFile.read()))
  return templates

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
