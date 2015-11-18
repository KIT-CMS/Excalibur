import configtools


def modify_config(cfg):
	"""
	Use 2015D data only
	"""
	cfg['JsonFiles'].add_run_range(256629, float("inf"))
	if cfg['InputIsData']:
		cfg["InputFiles"].set_input(
			ekppath="/storage/a/mfischer/skims/zjet/2015-10-30/Zmm_DoubleMu_Run2015D_*_13TeV/*.root",
		)
		cfg['Lumi'] = configtools.get_lumi(json_source=cfg['JsonFiles'])
	return cfg
