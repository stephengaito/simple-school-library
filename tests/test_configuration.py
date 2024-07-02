
import yaml

import pytest

from schoolLib.setup.configuration import *

from utils import *

def test_config() :
  assert loadedConfig('testConfig.yaml')

  print(yaml.dump(config))

  assert 'database'     in config
  assert 'templatesDir' in config
  assert 'markdownDir'  in config

  assert config['database'] == 'tmp/sslDb.sqlite'
  assert config['templatesDir'].endswith('schoolLib/templates')
  assert config['markdownDir'].endswith('schoolLib/markdown')
