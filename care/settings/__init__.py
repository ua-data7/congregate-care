import os
from pathlib import Path
import sys
import imp

SETTINGS_DIR = Path(__file__).parent
LOCAL_SETTINGS_FILE = SETTINGS_DIR / 'local.py'
BASE_SETTINGS_FILE = SETTINGS_DIR / 'base.py'

#####################
# LOAD DOTENV STUFF #
#####################
from .dotenv import *

######################
# LOAD BASE SETTINGS #
######################
# from .base import *
module_name = 'base'
module = imp.new_module(module_name)
module.__file__ = SETTINGS_DIR / 'base.py'
sys.modules[module_name] = module
exec(open(BASE_SETTINGS_FILE, "rb").read())

#######################
# LOAD LOCAL SETTINGS #
#######################
if(os.path.exists(LOCAL_SETTINGS_FILE)):
    module_name = 'local'
    module = imp.new_module(module_name)
    module.__file__ = LOCAL_SETTINGS_FILE
    sys.modules[module_name] = module
    exec(open(LOCAL_SETTINGS_FILE, "rb").read())
else:
    print("Generating empty settings/local.py")
    Path(SETTINGS_DIR, 'local.py').touch()

