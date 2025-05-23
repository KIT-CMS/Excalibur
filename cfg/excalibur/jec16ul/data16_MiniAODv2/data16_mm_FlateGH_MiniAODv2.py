import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES, config as _config

CH='mm'
JEC='{0}_Run{1}_{2}'.format(JEC_BASE, 'FGH', JEC_VERSION)
RUN='FlateGH'

def config():
    return _config(CH, RUN, JEC)
