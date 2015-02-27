def getBaseConfig(**kwargs):
    cfg = {
        'SkipEvents': 0,
        'EventCount': -1,
        'GlobalProducer': [],
        'InputFiles': [],     # overridden by artus
        'OutputPath': "out",  # overridden by artus
        'ZMass': 91.1876,
        'ZMassRange': 20.,
        'Pipelines': {
            'default': {
                'Level': 1,
                'JetAlgorithm': "AK5PFJetsCHSL1L2L3Res",
                'Consumers': [
                    "KappaLambdaNtupleConsumer",
                    "cutflow_histogram",
                ],
                'EventWeight': 'eventWeight',
                'Filter':[],
                'Processors': [
                    'filter:ZFilter'
                ],
                'Quantities': [
                    "run", "event", "lumi"
                ],
                'Cuts': [],
            }
        },

        # Wire Kappa objects
        "EventMetadata" : "eventInfo",
        "LumiMetadata" : "lumiInfo",
        #"VertexSummary": "goodOfflinePrimaryVerticesSummary",
        "VertexSummary": "offlinePrimaryVerticesSummary",
    }
    return cfg

##
##


def data(cfg, **kwargs):
    cfg['InputType'] = 'data'
    cfg['InputIsData'] = True
    #cfg['Pipelines']['default']['QuantitiesVector'] += ['run', 'eventnr', 'lumisec']


def mc(cfg, **kwargs):
    cfg['InputType'] = 'mc'
    cfg['InputIsData'] = "false"
    # put the gen_producer first since e.g. l5_producer depend on it

##
##


def _2011(cfg, **kwargs):
    cfg['Year'] = 2011


def _2012(cfg, **kwargs):
    cfg['Year'] = '2012'


##
##


def ee(cfg, **kwargs):
    pass

def em(cfg, **kwargs):
    pass

def mm(cfg, **kwargs):
    cfg['Muons'] = 'muons'
    # The order of these producers is important!
    cfg['Processors'] = [
        'producer:ValidMuonsProducer',			#Artus
        'producer:MuonCorrectionsProducer',		#Artus
        'producer:ZProducer',					#Excalibur
        'filter:ZFilter',						#Excalibur
    ]
    cfg['MuonID'] = 'tight'
    cfg['MuonIso'] = 'tight'
    cfg['MuonIsoType'] = 'pf'
    cfg['DirectIso'] = 'true'
    
    cfg['Pipelines']['default']['Quantities'] += ['nMuons']


###
###


def data_2011(cfg, **kwargs):
    pass

def data_2012(cfg, **kwargs):
    pass

def mc_2011(cfg, **kwargs):
    pass

def mc_2012(cfg, **kwargs):
    pass


def mcee(cfg, **kwargs):
    pass


def _2011mm(cfg, **kwargs):
    pass

def _2012mm(cfg, **kwargs):
    pass


##
##

def mc_2011mm(cfg, **kwargs):
    pass


def mc_2012ee(cfg, **kwargs):
    pass


def mc_2012mm(cfg, **kwargs):
    pass


def data_2011mm(cfg, **kwargs):
    pass


def data_2012mm(cfg, **kwargs):
    pass


def data_2012ee(cfg, **kwargs):
    pass


def data_2012em(cfg, **kwargs):
    pass


