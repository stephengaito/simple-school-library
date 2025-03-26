
# from schoolLib.htmxComponents.htmx import HtmxBase
from schoolLib.htmxComponents.simpleComponents import \
  Label  # , Text, Menu

def test_Label() :
  aLabel = Label("aLabel")
  assert aLabel.isA(Label)
  assert False
