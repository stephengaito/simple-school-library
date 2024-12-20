
import os
import yaml

# from starlette.templating import Jinja2Templates

###############################################################
# A simple (global) configuration system

# QUESTION: Should we move the schema loading to this module?

emojiColours = {
  'red'       : '&#x1F534;',
  'orange'    : '&#x1F7E0;',
  'yellow'    : '&#x1F7E1;',
  'green'     : '&#x1F7E2;',
  'turquoise' : '&#x1F535;',
  'blue'      : '&#x1F535;',
  'purple'    : '&#x1F7E3;',
  'brown'     : '&#x1F7E4;',
  'black'     : '&#x26AB;',
  'white'     : '&#x26AA;'
}

def addEmojiColour(emojiColourName, text) :
  if emojiColourName not in emojiColours :
    emojiColourName = 'black'
  return emojiColours[emojiColourName] + ' ' + text

config = {}

def sanitizeConfig(config, verbose=False) :
  if 'database' not in config :
    config['database'] = 'db.sqlite'

  # if 'makrdownDir' not in config :
  #   config['markdownDir'] = os.path.join(
  #     os.path.dirname(os.path.dirname(__file__)),
  #     'markdown'
  #   )

  if 'themeDir' not in config :
    config['themeDir'] = os.path.join(
      os.path.dirname(os.path.dirname(__file__)),
      'htmxComponents',
      'theme'
    )

  if verbose :
    print("----------------------------------------")
    print(yaml.dump(config))
    # print(repr(templates))
    print("----------------------------------------")
  # config['templates'] = templates

def loadedConfigFromStr(aConfigStr, reportErrors=False, verbose=False) :
  if config :
    # do not try to load the configuration twice
    return True

  if verbose :
    reportErrors = True
  try :
    config.update(yaml.safe_load(aConfigStr))
    sanitizeConfig(config, verbose=verbose)
    return True
  except Exception as err :
    if reportErrors :
      print(repr(err))
  return False

def loadedConfig(aConfigPath, reportErrors=False, verbose=False) :
  if config :
    # do not try to load the configuration twice
    return True

  if verbose :
    reportErrors = True
  try :
    with open(aConfigPath) as configFile :
      return loadedConfigFromStr(
        configFile.read(), reportErrors=reportErrors, verbose=verbose
      )
  except Exception as err :
    if reportErrors :
      print(repr(err))
  return False


