import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES, config as _config

CH='ee'
RUN='BCD'
JEC='{0}APV_Run{1}_{2}'.format(JEC_BASE, RUN, JEC_VERSION)

def config():
    return _config(CH, RUN, JEC)
