
from datetime import date
from jinja2 import Environment, PackageLoader, select_autoescape

jinja2env = Environment(
  loader=PackageLoader("schoolLib.oldHtmxComponents"),
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
jinja2env.globals['today'] = date.today()
