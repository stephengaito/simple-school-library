
import os
import yaml

from starlette.templating import Jinja2Templates

###############################################################
# A simple (global) configuration system

# QUESTION: Should we move the schema loading to this module?

config = {}

def sanitizeConfig(config, verbose=False) :
  if 'database' not in config :
    config['database'] = 'db.sqlite'
  if 'templatesDir' not in config :
    config['templatesDir'] = os.path.join(
      os.path.dirname(os.path.dirname(__file__)),
      'templates'
    )
  templates = Jinja2Templates(directory=config['templatesDir'])

  if 'makrdownDir' not in config :
    config['markdownDir'] = os.path.join(
      os.path.dirname(os.path.dirname(__file__)),
      'markdown'
    )

  if 'themeDir' not in config :
    config['themeDir'] = os.path.join(
      os.path.dirname(os.path.dirname(__file__)),
      'htmxComponents',
      'theme'
    )

  if verbose :
    print("----------------------------------------")
    print(yaml.dump(config))
    print(repr(templates))
    print("----------------------------------------")
  config['templates'] = templates

def loadedConfig(aConfigPath, reportErrors=False, verbose=False) :
  if verbose : reportErrors = True
  try :
    with open(aConfigPath) as configFile :
      config.update(yaml.safe_load(configFile.read()))
    sanitizeConfig(config, verbose=verbose)
    return True
  except Exception as err :
    if reportErrors :
      print(repr(err))
  return False
