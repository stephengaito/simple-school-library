
# import yaml

# from schoolLib.htmxComponents.htmx import HtmxBase
from schoolLib.htmxComponents.simpleComponents import \
  Label  # , Text, Menu

def test_Label() :
  aLabel = Label("aLabel")
  assert aLabel.isA(Label)
  assert len(aLabel.children) == 1
  assert aLabel.children[0] == "aLabel"
  assert aLabel.collectHtmlStr() == '<label > aLabel </label>'

