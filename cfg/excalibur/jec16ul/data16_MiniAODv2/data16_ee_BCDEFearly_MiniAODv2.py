import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES, config as _config

CH='ee'
RUN='BCDEFearly'
JEC='{0}APV_Run{1}_{2}'.format(JEC_BASE, 'BCDEF', JEC_VERSION)

def config():
    return _config(CH, RUN, JEC)
