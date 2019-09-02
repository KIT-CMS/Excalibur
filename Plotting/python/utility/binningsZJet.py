
# -*- coding: utf-8 -*-
import numpy as np
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

from Artus.HarryPlotter.utility.binnings import BinningsDict

"""
    This module contains a dictionary for binnings and a function for rebinning in rapidity bins.
"""
class BinningsDictZJet(BinningsDict):

    def __init__(self):
        super(BinningsDictZJet, self).__init__()

        absetabins = "0 0.783 1.305 1.93 2.5 2.964 3.139 5.191"
        self.binnings_dict.update({
            #'zpt': "30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500",
            'pt':'38,10,200',
            'eta':" ".join([str(y) for y in [-i for i in [float(x) for x in absetabins.split(" ")][7:0:-1]]+[float(x) for x in absetabins.split(" ")]]),
            'phi': '30,-3.14159,3.14159',
            'abseta': absetabins,
            'alpha': '20,0,2',
            'deltaphijet1jet2': '25,-0,3.14159',
            'deltaetajet1jet2': '20,0,5',
            'deltarjet1jet2': '40,0,7',
            'deltayzjet1': '100,0,10',
            'deltaphizjet1': '30,0,3.14159',
            'deltaRzjet1': '30,0,6',
            'deltaphimuminusmuplus': '30,0,3.14159',
            'deltaRmuminusmuplus': '30,0,5',
            'jet1match': '100,0,6',
            'jet2match': '100,0,6',
            'deltaRjet1genjet2': '100,0,6',
            'deltaRjet1genjet3': '100,0,6',
            'deltaRjet2genjet1': '100,0,6',
            'jet1resolution': '100,-1,3',
            
            'nmuons':       '10,0,10',
            'mupluspt':     '11,25,300',
            'mupluseta':    '24,-2.4,2.4',
            'muplusphi':    '30,-3.14,3.14',
            'muplusRiso':   '30,0.01,0.31',
            'muminuspt':    '11,25,300',
            'muminuseta':   '24,-2.4,2.4',
            'muminusphi':   '30,-3.14,3.14',
            'muminusRiso':  '30,0.01,0.31',
            
            'zl1pt':        '15,25,500',
            'zl1eta':       '24,-2.4,2.4',
            'zl1phi':       '30,-3.14,3.14',
            'zl2pt':        '10,25,300',
            'zl2eta':       '24,-2.4,2.4',
            'zl2phi':       '30,-3.14,3.14',
            
            #'phistareta':   '0.001 0.003 0.01 0.03 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.2 1.5 2 3 4 5 7 10 15 20 30 50',
            'phistareta':   '0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.2 1.5 2 3 4 5 7 10 15 20 30 50',
            #'zpt':          '5 10 15 20 25 30 35 40 45 50 60 70 80 90 100 110 130 150 170 190 220 250 400 1000',
            'zpt':          '25 30 35 40 45 50 60 70 80 90 100 110 130 150 170 190 220 250 400 1000',
            'zy':           '12,-2.4,2.4',
            'abs(zy)':      '12,0,2.4',
            'zmass':        '80,71,111',
            'zphi':         '30,-3.14159,3.14159',
            'njets':        '10,0,10',
            'njets30':      '10,0,10',
            'jet1eta':      '-5.191 -3.839 -3.489 -3.139 -2.964 -2.853 -2.650 -2.500 -2.322 -2.172 -1.930 -1.653 -1.479 -1.305 -1.044 -0.783 -0.522 -0.261 0.000 0.261 0.522 0.783 1.044 1.305 1.479 1.653 1.930 2.172 2.322 2.500 2.650 2.853 2.964 3.139 3.489 3.839 5.191',
            'absjet1eta':   '0.000 0.261 0.522 0.783 1.044 1.305 1.479 1.653 1.930 2.172 2.322 2.500 2.650 2.853 2.964 3.139 3.489 3.839 5.191',
            'abs(jet1y)':   '12,0,2.4',
            'abs(jet2y)':   '12,0,2.4',
            'abs(jet3y)':   '12,0,2.4',
            'jet1pt':       '5 10 15 20 25 30 40 50 75 125 175 225 300 400',
            'jetavept':     '5 10 15 20 25 30 40 50 75 125 175 225 300 400',
            'jetyboost':    '12,0,2.4',
            'jetystar':     '12,0,2.4',
            'jet2pt':       '5 10 20 30 40 50 75 125 175 250 400',
            'jet3pt':       '5 10 20 30 40 50 75 125 175 250 400',
            'jet1y':        '24,-2.4,2.4',
            'jet2y':        '30,-2.4,2.4',
            'jet3y':        '30,-2.4,2.4',
            'jet1phi':      '31,-3.142,3.142',
            'jet2phi':      '31,-3.142,3.142',
            'jet3phi':      '31,-3.142,3.142',
            'jzb':          '20,-200,200',
            
            'ystar':    '5,0,2.5',
            'yboost':   '5,0,2.5',
            
            'npv':      '80,0,80',
            'npumean':  '80,0,80',
            'rho':      '80,0,50',
            'run':      '200,276200,276400',
            'jet1puidraw': '100,-1,1',
            'met':      '70,0,350',

            'jet1pt/genjet1pt': '40,0.,2.',  # JER gen
            'jet1pt/zpt':       '40,0.,2.',  # ptbalance gen
            'genjet1pt/genzpt': '40,0.,2.',  # PLI gen
            'genzpt/zpt':       '40,0.,2.',  # ZRes gen
            'ptbalance':        '40,0.,2.',  # ptbalance data
            'mpf':              '40,0.,2.',  # mpf data
        })
    
def rebinning(args,d,obs,yboostbin,ystarbin):
    if obs in ['mupluspt','muminuspt','zl1pt','zl2pt']:
        d.update({
            'x_bins': [' '.join(['{}'.format(x) for x in range(25,300,(300-25)/11)])+' 350'],
            'y_bins': [' '.join(['{}'.format(x) for x in range(25,300,(300-25)/11)])+' 350'],
            })
    if obs in ['zy','jet1y','mupluseta','muminuseta','zl1eta','zl2eta']:
        d.update({'x_bins': ['-2.4 -2.2 -2.0 -1.8 -1.6 -1.4 -1.2 -1.00 -0.8 -0.6 -0.4 -0.2 0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0 2.2 2.4']})
    if obs == 'jet1pt':
        d.update({'x_bins': ['5 10 12 15 20 30 50 75 125 175 225 300 400'] })
    if obs == 'yboost' or obs=='ystar':
        d.update({'x_bins': ['0.0 0.5 1.0 1.5 2.0 2.5']})
    
    if obs=='zpt':
        if (yboostbin==(0.0,0.5) and ystarbin==(2.0,2.5)):
            print obs+" binning changed"
            d.update({  'x_ticks': [40,60,100,200],
                        'x_bins': ['25 30 40 50 70 90 110 150 250 1000'],
                        'y_bins': ['25 30 40 50 70 90 110 150 250 1000'],
                        })
        elif ( (yboostbin==(0.0,0.5) and ystarbin==(1.5,2.0))
            or (yboostbin==(0.5,1.0) and ystarbin==(1.5,2.0))
            or (yboostbin==(1.0,1.5) and ystarbin==(1.0,1.5))
            or (yboostbin==(1.5,2.0) and ystarbin==(0.5,1.0))
            or (yboostbin==(2.0,2.5) and ystarbin==(0.0,0.5))
            ):
            print obs+" binning changed"
            d.update({  'x_ticks': [40,60,100,200,400,1000],
                        'x_bins': ['25 30 35 40 45 50 60 70 80 90 100 110 130 150 170 190 250 1000'],
                        'y_bins': ['25 30 35 40 45 50 60 70 80 90 100 110 130 150 170 190 250 1000'],
                        })
        else: # use standard binning
            d.update({  'x_ticks': [40,60,100,200,400,1000],
                        'x_bins': ['25 30 35 40 45 50 60 70 80 90 100 110 130 150 170 190 220 250 400 1000'],
                        'y_bins': ['25 30 35 40 45 50 60 70 80 90 100 110 130 150 170 190 220 250 400 1000'],
                        })
    if obs=='phistareta':
        if (yboostbin==(0.0,0.5) and ystarbin==(2.0,2.5)):
            print obs+" binning changed"
            d.update({  'x_ticks': [0.5, 1, 2, 4],
                        'x_bins': ['0.4 0.6 0.8 1.0 5 50'],
                        'y_bins': ['0.4 0.6 0.8 1.0 5 50'],
                        #'x_bins': ['0.4 0.5 0.6 0.7 0.8 1.0 5.0'],
                        #'y_bins': ['0.4 0.5 0.6 0.7 0.8 1.0 5.0'],
                        })
        elif ( (yboostbin==(0.0,0.5) and ystarbin==(1.5,2.0))
            or (yboostbin==(0.5,1.0) and ystarbin==(1.5,2.0))
            or (yboostbin==(1.0,1.5) and ystarbin==(1.0,1.5))
            or (yboostbin==(1.5,2.0) and ystarbin==(0.5,1.0))
            or (yboostbin==(2.0,2.5) and ystarbin==(0.0,0.5))
            ):
            print obs+" binning changed"
            d.update({  'x_ticks': [0.5, 1, 2, 4, 10, 30],
                        'x_bins': ['0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.2 1.5 2 3 5 10 50'],
                        'y_bins': ['0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.2 1.5 2 3 5 10 50'],
                        #'x_bins': ['0.4 0.5 0.6 0.7 0.8 0.9 1.0 3.0 5.0 7.0 50'],
                        #'y_bins': ['0.4 0.5 0.6 0.7 0.8 0.9 1.0 3.0 5.0 7.0 50'],
                        })
        else: # use standard binning            
            d.update({  'x_ticks': [0.5, 1, 2, 4, 10, 30],
                        'x_bins': ['0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.2 1.5 2 3 4 5 7 10 15 20 30 50'],
                        'y_bins': ['0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.2 1.5 2 3 4 5 7 10 15 20 30 50'],
                        #'x_bins':['0.4 0.5 0.6 0.7 0.8 0.9 1.0 3.0 5.0 7.0 10 20 30 50'],
                        #'y_bins':['0.4 0.5 0.6 0.7 0.8 0.9 1.0 3.0 5.0 7.0 10 20 30 50'],
                        })

            
