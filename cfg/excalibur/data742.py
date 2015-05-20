import ZJetConfigBase as base
import data

def config():
	cfg = data.config()
	cfg["InputFiles"] = base.setInputFiles(
		ekppath="/storage/a/dhaitz/skims/2015-05-21_DoubleMu_Run2012_742_8TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/dhaitz/2015-05-21_DoubleMu_Run2012_742_8TeV*.root",
	)
	cfg['Processors'].remove("filter:HltFilter")
	for pipeline in cfg['Pipelines']:
		for tag in ['jet1btag', 'jet1qgtag']:
			cfg['Pipelines'][pipeline]['Quantities'].remove(tag)
	return cfg
