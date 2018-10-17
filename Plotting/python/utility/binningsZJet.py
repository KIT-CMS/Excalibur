
# -*- coding: utf-8 -*-

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
            'mupluseta':    '50,-3,3',
            'muplusphi':    '30,-3.14,3.14',
            'muplusRiso':   '30,0.01,0.31',
            'muminuspt':    '11,25,300',
            'muminuseta':   '50,-3,3',
            'muminusphi':   '30,-3.14,3.14',
            'muminusRiso':  '30,0.01,0.31',
            
            #'phistareta':   '0.8 0.9 1.0 1.25 1.5 2 3 4 6 12 25 50 100 400',
            #'phistareta':   '0.001 0.005 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.2 1.5 2 3 4 6 12 25 50 100',
            'phistareta':   '0.102 0.114 0.128 0.145 0.165 0.189 0.219 0.258 0.312 0.391 0.524 0.695 0.918 1.153 1.496 1.947 2.522 3.2774 6 12 25 50 100 ',
            #'zpt':          '30 35 40 45 50 55 60 70 80 90 100 120 140 160 180 240 300 400 1000',
            'zpt':          '5 10 15 20 25 30 35 40 45 50 60 70 80 90 100 110 130 150 170 190 220 250 400 1000',
            #'zpt':          '30 35 41 48 56 65 76 90 105 123 144 169 198 232 272 319 374 439 1000',,
            'zy':           '30,-3,3',
            'abs(zy)':      '12,0,2.4',
            'zmass':        '40,71,111',
            'zphi':         '30,-3.14159,3.14159',
            'njets':        '10,0,10',
            'njets30':      '10,0,10',
            'jet1eta':      '30,-3,3',
            'abs(jet1y)':   '12,0,2.4',
            'abs(jet2y)':   '12,0,2.4',
            'abs(jet3y)':   '12,0,2.4',
            'jet1pt':       '5 10 20 30 50 75 125 175 225 300 400',
            'jet2pt':       '5 10 20 30 40 50 75 125 175 250',
            'jet3pt':       '5 10 20 30 40 50 75 125 175 250',
            'jet1y':        '30,-5.4,5.4',
            'jet2y':        '30,-5.4,5.4',
            'jet3y':        '30,-5.4,5.4',
            'jet1phi':      '31,-3.142,3.142',
            'jet2phi':      '31,-3.142,3.142',
            'jet3phi':      '31,-3.142,3.142',
            'jzb':          '20,-200,200',
            
            'ystar':    '6,0,3',#'6,0,3',#
            'yboost':   '6,0,3',#'6,0,3',#
            
            'npv':      '80,0,80',
            'npumean':  '80,0,80',
            'rho':      '80,0,50',
            'run':      '200,276200,276400',
            'jet1puidraw': '100,-1,1',
            'met':      '70,0,350',
            
        })
    
def rebinning(args,d,obs,yboostbin,ystarbin):
    if obs == 'mupluspt' or obs == 'muminuspt':
        d.update({
            'x_bins': [' '.join(['{}'.format(x) for x in range(25,300,(300-25)/11)])+' 350'],
            'y_bins': [' '.join(['{}'.format(x) for x in range(25,300,(300-25)/11)])+' 350'],
            })
    if obs == 'zy' or obs =='jet1y':
        d.update({'x_bins': ['-2.4 -2.2 -2.0 -1.8 -1.6 -1.4 -1.2 -1.00 -0.8 -0.6 -0.4 -0.2 0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8 2.0 2.2 2.4']})
    if obs == 'jet1pt':
        d.update({'x_bins': ['5 10 12 15 20 30 50 75 125 175 225 300 400'] })
    if obs == 'yboost' or obs=='ystar':
        d.update({'x_bins': ['0.0 0.5 1.0 1.5 2.0 2.5']})
    
    if obs=='zpt':
        if (yboostbin==(0.0,0.5) and ystarbin==(2.0,2.5)):
            print obs+" binning changed"
            d.update({  'x_ticks': [40,60,100,200],
                        'x_bins': ['25 30 40 50 70 90 110 150 250'],
                        'y_bins': ['25 30 40 50 70 90 110 150 250'],
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
                        'x_bins': ['0.4 0.6 0.8 1.0 5'],
                        'y_bins': ['0.4 0.6 0.8 1.0 5'],
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

            
