import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES, config as _config

CH='mm'
RUN='EFearly'
JEC='{0}APV_Run{1}_{2}'.format(JEC_BASE, 'EF', JEC_VERSION)

def config():
    return _config(CH, RUN, JEC)
