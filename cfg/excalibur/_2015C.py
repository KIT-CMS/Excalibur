

def modify_config(cfg):
	"""
	Use 2015D data only
	"""
	cfg['JsonFiles'].add_run_range(253888, 256629)
	if cfg['InputIsData']:
		cfg["InputFiles"].set_input(
			ekppath="/storage/a/mfischer/skims/zjet/2015-10-30/Zmm_DoubleMu_Run2015C_*_13TeV/*.root",
			nafpath="/pnfs/desy.de/cms/tier2/store/user/mafische/skims/MF_Zll_run2/2015-10-30/Zmm_DoubleMu_Run2015C_*_13TeV/*.root"
		)
	return cfg
