import configtools


def modify_config(cfg):
	"""
	Use 2015D data only
	"""
	cfg["InputFiles"] = configtools.setInputFiles(
		ekppath="/storage/a/mfischer/skims/zjet/2015-10-09/DoubleMu_Run2015C_Jul2015_13TeV/*.root",
		nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_AnyMu_2015_746/2015-10-09/DoubleMu_Run2015C_Jul2015_13TeV/*.root",
	)
	configtools.get_lumi(json_source=cfg['JsonFiles'][0], min_run=253888., max_run=256629.)
	return cfg
