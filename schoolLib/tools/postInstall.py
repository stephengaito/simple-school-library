
import os

def patches() :
  print("Installing Bootstrap Icons")
  print("-------------------------------------------------------")
  os.system("git clone --depth=1 https://github.com/twbs/icons.git /tmp/bootstrapIcons")
  os.system("mkdir -p schoolLib/statics/svg")
  os.system("rm -rf schoolLib/statics/svg/bootstrap")
  os.system("cp -r /tmp/bootstrapIcons/icons schoolLib/statics/svg")
  os.system("mv schoolLib/statics/svg/icons schoolLib/statics/svg/bootstrap")
  os.system("rm -rf /tmp/bootstrapIcons")
  print("-------------------------------------------------------")