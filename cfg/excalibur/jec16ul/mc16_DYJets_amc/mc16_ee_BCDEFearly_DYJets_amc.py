import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES, config as _config

CH='ee'
JEC='{0}APV_{1}'.format(JEC_BASE, JEC_VERSION)
RUN='BCDEFearly'

def config():
    return _config(CH, RUN, JEC)
