
import yaml

# import pytest

from schoolLib.setup.configuration import loadedConfig, config

# from utils import getResponseBody

def test_config() :
  assert loadedConfig('tests/testConfig.yaml')

  print(yaml.dump(config))

  assert 'database'     in config
  assert 'markdownDir'  in config

  assert config['database'] == 'tmp/sslDb.sqlite'
  assert config['markdownDir'].endswith('schoolLib/markdown')
