from cross_section import *
deltaRgen = 'sqrt((genmupluseta-genmuminuseta)^2+min(abs(genmuplusphi-genmuminusphi),6.283-abs(genmuplusphi-genmuminusphi))^2)'
deltaRreco = 'sqrt((mupluseta-muminuseta)^2+min(abs(muplusphi-muminusphi),6.283-abs(muplusphi-muminusphi))^2)'
def comp_sim_IDs(args=None):
	plots = []
	for year in ['16',]:
		d = ({
			'files' : ['work/mc16_genCuts.root', 'work/mc16_tightIso.root', 'work/mc16_highpt.root','work/mc16_noRochcorr.root'],
			'folders' : ['genzcuts/ntuple','zcuts/ntuple','zcuts/ntuple','zcuts/ntuple'],
			'nicks' : ['gen', 'tight', 'highpt', 'medloose'],
			'x_expressions': ['genzpt', 'zpt','zpt','zpt'],
			#'x_label' : r'$\\phi^*_\\eta$',
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			'y_lims' : [0.0001,6], 
			'weights': [ '1', '(leptonSFWeight)','(leptonSFWeight)','(leptonSFWeight)'],
			#'histograms_to_normalize_by_binwidth' : ['data','mc'],
			#'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
			'labels' : ['Gen','TightIDTightIso', 'HighPtIDLooseIso', 'MediumIDLooseIso'],
			'x_bins' :  ['30 40 50 60 80 100 120 140 170 200 1000'],
			'analysis_modules' : ['NormalizeByBinWidth', 'Ratio', 'PrintBinContent'],
			'ratio_numerator_nicks' : ['tight', 'highpt', 'medloose'],
			'ratio_denominator_nicks' : ['gen','gen','gen'],
			'colors' : ['black', 'blue', 'red', 'green', 'blue', 'red', 'green'], 
			"filename" : 'mc_comp_pt',
			'y_subplot_lims' : [0.90,1.05],
			'y_subplot_label' : 'Ratio to Genlevel',
			'y_log' : True,
			'x_log' : True,
			#'legend' : 'lower left',
			#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
			'scale_factors' : scalefactors[year],
			#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
			#'www' : 'cross_sections_2016',
		})
		plots.append(d)
		return [PlottingJob(plots=plots, args=args)]
def comp_sim_cuts(args=None):
	plots = []
	for year in ['16',]:
		d = ({
			'files' : ['work/mc16_genCuts.root', 'work/mc16_tightIso.root','work/mc16_genCuts.root', 'work/mc16_tightIso.root', 'work/mc16_genCuts.root', 'work/mc16_tightIso.root', 'work/mc16_genCuts.root',  'work/mc16_tightIso.root'],
			'folders' : ['genzcuts/ntuple', 'zcuts/ntuple','genzcuts/ntuple', 'zcuts/ntuple','genzcuts/ntuple', 'zcuts/ntuple','genzcuts/ntuple', 'zcuts/ntuple' ],
			'nicks' : ['gen22', 'reco22', 'gen30', 'reco30', 'gendeltaR', 'recodeltaR','gen200', 'reco200'],
			'x_expressions': ['genzpt','zpt', 'genzpt','zpt','genzpt', 'zpt','genzpt', 'zpt'],
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			'y_lims' : [0.9,1.02], 
			'weights': ['1','(leptonSFWeight)','genmupluspt>30&genmuminuspt>30','(leptonSFWeight)*(mupluspt>30&muminuspt>30)', '('+deltaRgen+'>0.5)','(leptonSFWeight)*('+deltaRreco+'>0.5)','(genmupluspt<200&genmuminuspt<200)*('+deltaRgen+'>0.5)','(mupluspt<200&muminuspt<200)*(leptonSFWeight)*('+deltaRreco+'>0.5)'],
			'markers': ['_','_','_','_','_','_','_','_','_','_','_'],
			'lines': [1.0],
			'labels' : ['StandardCuts','MuPt>30', 'DeltaRCut'],
			'x_bins' :  ['30 40 50 60 80 100 120 140 170 200 1000'],
			'analysis_modules' : ['NormalizeByBinWidth','Divide', 'PrintBinContent'],
			'divide_numerator_nicks' : ['reco22', 'reco30', 'recodeltaR','reco200'],
			'divide_denominator_nicks' : ['gen22','gen30','gendeltaR','gen200'],
			'divide_result_nicks' : ['res22', 'res30', 'resdeltaR', 'res200'],
			'nicks_whitelist' : ['res'],
			'nicks_blacklist' : ['res200'],
			#'ratio_numerator_nicks' : ['tight', 'highpt', 'medloose', 'medno'],
			#'ratio_denominator_nicks' : ['gen','gen','gen','gen'],
			#'colors' : ['black', 'blue', 'red', 'green', 'cyan', 'blue', 'red', 'green', 'cyan'], 
			"filename" : 'mc_comp_Cuts',
			'y_label' : 'Ratio Reco/Gen',
			'x_log' : True,
			#'legend' : 'lower left',
			#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
			'scale_factors' : scalefactors[year],
			#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			#'www' : 'cross_sections_2016',
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def comp_sim_stat_errors(args=None):
	plots = []
	for year in ['16',]:
		d = ({
			'files' : ['work/mc16_tightIso.root', 'work/mc16_tightIso.root', 'work/mc16_tightIso.root'],
			'folders' : ['zcuts/ntuple','zcuts/ntuple','zcuts/ntuple'],
			'nicks' : ['22', '30', '40'],
			'x_expressions': ['zpt', 'zpt'],
			#'x_label' : r'$\\phi^*_\\eta$',
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			#'y_lims' : [1,7], 
			'weights': ['(leptonSFWeight)','(leptonSFWeight)*(mupluspt>30&muminuspt>30)', '(leptonSFWeight)*('+deltaRreco+'>0.5)'],
			#'histograms_to_normalize_by_binwidth' : ['data','mc'],
			#'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
			'labels' : ['StandardCuts','MuonPt>30', 'DeltaRCut', ],
			'x_bins' :  ['30 40 50 60 80 100 120 140 170 200 1000'],
			'analysis_modules' : ['StatisticalErrors', 'PrintBinContent'],
			'stat_error_relative' : True,
			'stat_error_relative_percent' : True,
			#'ratio_numerator_nicks' : ['tight', 'highpt', 'medloose', 'medno'],
			#'ratio_denominator_nicks' : ['gen','gen','gen','gen'],
			#'colors' : ['black', 'blue', 'red', 'green', 'cyan', 'blue', 'red', 'green', 'cyan'], 
			"filename" : 'mc_comp_errors',
			#'y_subplot_lims' : [0.90,1.05],
			#'y_subplot_label' : 'Ratio to Genlevel',
			#'y_log' : True,
			'x_log' : True,
			#'legend' : 'lower left',
			#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
			#'scale_factors' : scalefactors[year],
			'y_label' : "Relative Unc. / %",
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			#'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
			#'www' : 'cross_sections_2016',
		})
		plots.append(d)
		return [PlottingJob(plots=plots, args=args)]
def comp_sim_flag(args=None):
	plots = []
	d = ({
		'files' : ['work/mc16_genzproducer.root','work/mc16_allmukincuts.root'],
		'folders' : ['genleptoncuts/ntuple','genleptoncuts/ntuple'],
		'nicks' : ['reco','gen'],
		'x_expressions' : ['nmuons', 'nmuons'],
		#'x_label' : r'$\\phi^*_\\eta$',
		#'x_errors': [1],
		'lumis':  lumi['16'],
		'x_bins' : ['6,-0.5,5.5'],
		'analysis_modules' : ['PrintBinContent'],
		'energies' : [13],
		'weights': 'genzmass>81&&genzmass<101&validz<1',
		#'histograms_to_normalize_by_binwidth' : ['data','mc'],
		#'zorder' : ['nnpdf','ct14','hera','abm','data'],
		'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
		'labels' : ['RecoMuons', 'GenMuons'],
		#'y_bins' :  ['20,-10,10'],
		"filename" : 'mc_comp_nmuons',

	})
	plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def comp_sim_mu_IDs(args=None):
	plots = []
	for obs in ['pt','eta','phi']:
		for n in ['1','2']:
			d = ({
				'files' : ['work/mc16_noIDIso.root','work/mc16_zleptons.root','work/mc16_zleptons.root','work/mc16_zleptons.root'],
				'folders' : ['allleptoncuts/ntuple','allleptoncuts/ntuple','allleptoncuts/ntuple','genleptoncuts/ntuple'],
				'nicks' : ['noidiso', 'weightson', 'weightsoff', 'gen'],
				'x_expressions' : ['mu'+n+obs, 'mu'+n+obs,'mu'+n+obs, 'genzlepton'+n+obs],
				#'x_label' : r'$\\phi^*_\\eta$',
				'x_errors': [1],
				'lumis':  lumi['16'],
				'energies' : [13],
				'weights': ['1', 'leptonSFWeight','1', '1'],
				#'histograms_to_normalize_by_binwidth' : ['data','mc'],
				#'zorder' : ['nnpdf','ct14','hera','abm','data'],
				'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
				'labels' : ['NOIDIso', 'IDIsoWeighted', 'IDIsoUnweighted', 'Gen'],
				#'y_bins' :  ['20,-10,10'],
				'analysis_modules' : ['NormalizeByBinWidth', 'Ratio', 'PrintBinContent'],
				'ratio_numerator_nicks' : ['noidiso', 'weightson', 'weightsoff'],
				'ratio_denominator_nicks' : ['gen','gen','gen'],
				'colors' : ['black','red','blue', 'green'], 
				"filename" : 'mc_comp_mu'+n+obs,
				'y_subplot_lims' : [0.70,1.30],
				'y_subplot_label' : 'Ratio to Gen',
				#'y_log' : True,
				#'legend' : 'lower left',
				#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
				#'scale_factors' : scalefactors[year],
				#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
				#'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
				#'www' : 'cross_sections_2016',
			})
			if(obs == 'pt'):
				d['x_bins'] = ['22 24 26 28 30 35 40 45 50 60 70 80 90 100']
				d['x_ticks'] = [22, 40, 60, 80, 100]
				d['x_label'] = r'$\\mathit{p}_{T}^{\\mu_'+n+'}$ / GeV'
			elif obs == 'eta':
				d['x_bins'] = ['46,-2.3,2.3']
				d['x_label'] = r'$\\mathit{\\eta}^{\\mu_'+n+'}$ / GeV'
			elif obs == 'phi':
				d['x_bins'] = ['64,-3.2,3.2']
				d['x_label'] = r'$\\mathit{\\phi}^{\\mu_'+n+'}$ / GeV'
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def comp_sim_muplus(args=None):
	plots = []
	for obs in ['pt']:
		for n in ['1']:
			d = ({
				'files' : ['work/mc16_muplus.root','work/mc16_muplus.root'],
				'folders' : ['allleptoncuts/ntuple','genleptoncuts/ntuple'],
				'nicks' : ['reco', 'gen'],
				'x_expressions' : ['genmupluspt', 'genmupluspt'],
				#'x_label' : r'$\\phi^*_\\eta$',
				'x_errors': [1],
				'lumis':  lumi['16'],
				'energies' : [13],
				#'weights': ['leptonSFWeight','1'],
				#'histograms_to_normalize_by_binwidth' : ['data','mc'],
				#'zorder' : ['nnpdf','ct14','hera','abm','data'],
				'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
				'labels' : ['Reco+Gen', 'Gen'],
				#'y_bins' :  ['20,-10,10'],
				'analysis_modules' : ['Ratio', 'PrintBinContent'],
				#'ratio_numerator_nicks' : ['reco', 'gen'],
				#'ratio_denominator_nicks' : ['genall','genall'],
				#'colors' : ['black','red','blue', 'green'], 
				"filename" : 'comp_muplus_genreco',
				'y_subplot_lims' : [0.95,1.05],
				'y_subplot_label' : 'Ratio to Gen',
				#'y_log' : True,
				#'legend' : 'lower left',
				#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
				#'scale_factors' : scalefactors[year],
				#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
				#'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
				#'www' : 'cross_sections_2016',
			})
			if(obs == 'pt'):
				d['x_bins'] = ['25 30 35 40 45 50 60 70 80 90 100']
				d['x_ticks'] = [25, 40, 60, 80, 100]
				#d['x_bins'] =  ['0 1000']
				d['x_label'] = r'$\\mathit{p}_{T}^{gen/reco\\mu^+}$ / GeV'
			elif obs == 'eta':
				d['x_bins'] = ['46,-2.3,2.3']
				d['x_label'] = r'$\\mathit{\\eta}^{\\mu_'+n+'}$ / GeV'
			elif obs == 'phi':
				d['x_bins'] = ['64,-3.2,3.2']
				d['x_label'] = r'$\\mathit{\\phi}^{\\mu_'+n+'}$ / GeV'
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def comp_sim_mu(args=None):
	plots = []
	for obs in ['pt']:
		for n in ['1','2']:
			d = ({
				'files' : ['mc16_status1_new.root','mc16_status1.root'],
				'folders' : ['genzcuts/ntuple','genzcuts/ntuple'],
				'nicks' : ['new', 'old'],
				'x_expressions' : ['genzlepton'+n+obs, 'genzlepton'+n+obs],
				#'x_label' : r'$\\phi^*_\\eta$',
				'x_errors': [1],
				'lumis':  lumi['16'],
				'energies' : [13],
				#'weights': ['genzmass>81&genzmass<101'],
				#'weights': ['leptonSFWeight','1'],
				#'histograms_to_normalize_by_binwidth' : ['data','mc'],
				#'zorder' : ['nnpdf','ct14','hera','abm','data'],
				'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
				'labels' : ['Cuts Before', 'Cuts After'],
				#'y_bins' :  ['20,-10,10'],
				'analysis_modules' : ['Ratio', 'PrintBinContent'],
				#'ratio_numerator_nicks' : ['reco', 'gen'],
				#'ratio_denominator_nicks' : ['genall','genall'],
				#'colors' : ['black','red','blue', 'green'], 
				"filename" : 'mc_comp_mu_genreco'+n+obs,
				'y_subplot_lims' : [0.90,1.10],
				'y_subplot_label' : 'Ratio to Gen',
				#'y_log' : True,
				#'legend' : 'lower left',
				#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
				#'scale_factors' : scalefactors[year],
				#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
				#'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
				#'www' : 'cross_sections_2016',
			})
			if(obs == 'pt'):
				d['x_bins'] = ['25 30 35 40 45 50 60 70 80 90 100']
				d['x_ticks'] = [25, 40, 60, 80, 100]
				#d['x_bins'] =  ['0 1000']
				d['x_label'] = r'$\\mathit{p}_{T}^{gen\\mu_'+n+'}$ / GeV'
			elif obs == 'eta':
				d['x_bins'] = ['46,-2.3,2.3']
				d['x_label'] = r'$\\mathit{\\eta}^{\\mu_'+n+'}$ / GeV'
			elif obs == 'phi':
				d['x_bins'] = ['64,-3.2,3.2']
				d['x_label'] = r'$\\mathit{\\phi}^{\\mu_'+n+'}$ / GeV'
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def comp_sim_Trigger(args=None):
	plots = []
	for year in ['16',]:
		d = ({
			'files' : ['work/mc16_genrecocomp.root','work/mc16_newTrigger.root', ],
			'folders' : ['zcuts/ntuple','zcuts/ntuple'],
			'nicks' : ['data', 'mc'],
			'x_expressions': ['zpt','zpt'],
			#'x_label' : r'$\\phi^*_\\eta$',
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			'y_lims' : [0.001,6], 
			'weights': ['(leptonSFWeight)', '(leptonSFWeight*leptonTriggerSFWeight)'],
			#'histograms_to_normalize_by_binwidth' : ['data','mc'],
			#'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
			'labels' : ['NoHLT', 'HLT'],
			'x_bins' :  ['30 40 50 60 80 100 120 140 170 200 1000'],
			#'x_bins' : ['30 35 40 45 50 60 70 80 90 100 125 150 175 200 250 300 350 400 500 600'],
			#'x_ticks' : [22, 30, 50, 100, 250, 600],
			'analysis_modules' : ['NormalizeByBinWidth', 'Ratio', 'PrintBinContent'],
			#'ratio_numerator_nicks' : ['data','nnpdf'],
			#'ratio_denominator_nicks' : ['mc', 'mc'],
			'colors' : ['black','red','black'], 
			"filename" : 'mc_comp_Trigger',
			'y_subplot_lims' : [0.90,1.10],
			#'y_subplot_label' : 'Ratio to Gen',
			'y_log' : True,
			'x_log' : True,
			#'legend' : 'lower left',
			#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
			'scale_factors' : scalefactors[year],
			#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			#'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
			#'www' : 'cross_sections_2016',
		})
		plots.append(d)
		return [PlottingJob(plots=plots, args=args)]
def comp_sim_pt(args=None):
	plots = []
	for year in ['16',]:
		d = ({
			'files' : ['work/mc16_status1test.root','work/mc16_allmukincuts.root'],
			'folders' : ['genleptoncuts/ntuple','genleptoncuts/ntuple'],
			'nicks' : ['data', 'mc'],
			'x_expressions': ['genzpt','genzpt'],
			#'x_label' : r'$\\phi^*_\\eta$',
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			#'y_lims' : [0.001,30], 
			#'weights': ['leptonSFWeight', '1'],
			'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
			'labels' : ['Reco', 'Gen'],
			'x_bins' :  ['-1000 2000'],
			#'x_bins' :  ['30 40 50 60 80 100 120 140 170 200 1000'],
			#'x_ticks' : [5, 15, 30, 70, 200, 700, 1000],
			'analysis_modules' : [ 'Ratio', 'PrintBinContent'],
			#'ratio_numerator_nicks' : ['data','nnpdf'],
			#'ratio_denominator_nicks' : ['mc', 'mc'],
			'colors' : ['black','red','black'], 
			"filename" : 'mc_comp_pt',
			'y_subplot_lims' : [0.90,1.10],
			#'y_subplot_label' : 'Ratio to Gen',
			'y_log' : True,
			'x_log' : True,
			#'legend' : 'lower left',
			#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
			#'scale_factors' : scalefactors[year],
			#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			#'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
			#'www' : 'cross_sections_2016',
		})
		plots.append(d)
		return [PlottingJob(plots=plots, args=args)]

def comp_sim_y(args=None):
	plots = []
	for year in ['16',]:
		d = ({
			'files' : ['work/mc16_zleptons.root','work/mc16_zleptons.root'],
			'folders' : ['allleptoncuts/ntuple','genleptoncuts/ntuple'],
			'nicks' : ['data', 'mc'],
			'x_expressions': ['zy','genzy'],
			#'x_label' : r'$\\phi^*_\\eta$',
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			#'y_lims' : [0.001,30], 
			'weights': ['(leptonSFWeight)', '1'],
			'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
			'labels' : ['Reco', 'Gen'],
			'x_bins' : ['46,-2.3,2.3'],
			'analysis_modules' : ['NormalizeByBinWidth', 'Ratio', 'PrintBinContent'],
			#'ratio_numerator_nicks' : ['data','nnpdf'],
			#'ratio_denominator_nicks' : ['mc', 'mc'],
			'colors' : ['black','red','black'], 
			"filename" : 'mc_comp_y',
			'y_subplot_lims' : [0.90,1.10],
			#'y_subplot_label' : 'Ratio to Gen',
			#'legend' : 'lower left',
			#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
			'scale_factors' : scalefactors[year],
			#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
			'x_label' : r'$\\mathit{y}^{Z}$ / GeV',
			#'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
			#'www' : 'cross_sections_2016',
		})
		plots.append(d)
		return [PlottingJob(plots=plots, args=args)]
def deltaR(args=None):
	plots = []
	year = '16'
	d = ({
		'files' : ['work/mc16_zleptons.root','work/mc16_zleptons.root'],
		'folders' : ['allzcuts/ntuple','genzcuts/ntuple'],
		'nicks' : ['reco', 'gen'],
		'x_expressions': ['zpt','genzpt'],
		'y_expressions': ['sqrt((mu1eta-mu2eta)^2+min(abs(mu1phi-mu2phi),6.283-abs(mu1phi-mu2phi))^2)','sqrt((genzlepton1eta-genzlepton2eta)^2+min(abs(genzlepton1phi-genzlepton2phi),6.283-abs(genzlepton1phi-genzlepton2phi))^2)'],
		'lumis':  lumi[year],
		'energies' : [13],
		'y_errors' : [True,True,False],
		'weights': ['(leptonSFWeight)', '1'],	
		'labels' : ['Reco', 'Gen'],
		#'y_lims': [0, 4],
		'markers': ['o', 'o'],
		'marker_fill_styles': ['full', 'none'],
		'x_errors': [True],
		'analysis_modules': ['Ratio'],
		'x_bins' : ['30 40 50 60 80 100 120 140 170 200 400 600 800 1000'],
		'ratio_denominator_no_errors' : True,
		'ratio_numerator_no_errors' : True,
		#'y_bins' : ['2 3 4'],
		'colors' : ['black', 'red'], 
		"filename" : 'deltaR_comp',
		'y_subplot_lims' : [0.8,1.20],
		'y_subplot_label' : 'Reco/Gen',
		#'y_log' : True,
		'x_log' : True,
		#'z_log' : True,
		#'z_lims' : [0.0001,10],
		#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
		'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
		'y_label' : r"$\\Delta R(\\mu^{+},\\mu^{-})$",
		'tree_draw_options' : 'profs',
		#'www' : 'cross_sections_2016',
	})
	plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def deltaR_2D(args=None):
	plots = []
	year = '16'
	for sets in ['gen', 'reco']:
		d = ({
			'files' : ['work/mc16_zleptons.root','work/mc16_zleptons.root'],
			'folders' : ['zcuts/ntuple','genzcuts/ntuple'],
			'nicks' : ['reco', 'gen'],
			'x_expressions': ['zpt','genzpt'],
			'y_expressions': ['sqrt((mu1eta-mu2eta)^2+min(abs(mu1phi-mu2phi),6.283-abs(mu1phi-mu2phi))^2)','sqrt((genzlepton1eta-genzlepton2eta)^2+min(abs(genzlepton1phi-genzlepton2phi),6.283-abs(genzlepton1phi-genzlepton2phi))^2)'],
			'lumis':  lumi[year],
			'nicks_whitelist': [sets],
			'energies' : [13],
			'y_errors' : False,
			'weights': ['(leptonSFWeight)', '1'],	
			'labels' : ['Reco', 'Gen'],
			'y_bins': ['50,0,5'],
			'markers': ['o', 'o'],
			'marker_fill_styles': ['full', 'none'],
			'x_errors': [True],
			'analysis_modules': ['ConvertToHistogram','Ratio'],
			'x_bins' : ['30 40 50 60 80 100 120 140 170 200 1000'],
			#'y_bins' : ['2 3 4'],
			'colors' : ['black', 'red'], 
			"filename" : 'deltaR_comp_'+sets,
			'y_subplot_lims' : [0.5,1.50],
			'y_subplot_label' : 'Reco/Gen',
			#'y_log' : True,
			'x_log' : True,
			'z_log' : True,
			'z_lims' : [1,1e5],
			#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			'y_label' : r"$\\Delta R(\\mu^{+},\\mu^{-})$",
			#'tree_draw_options' : 'profs',
			#'www' : 'cross_sections_2016',
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def deltaEta(args=None):
	plots = []
	year = '16'
	for sets in ['gen', 'reco']:
		d = ({
			'files' : ['work/mc16_Iso04_loose.root','work/mc16_genCuts.root'],
			'folders' : ['zcuts_L1L2L3/ntuple','genzcuts_L1L2L3/ntuple'],
			'nicks' : ['reco', 'gen'],
			'x_expressions': ['zpt','genzpt'],
			'y_expressions': ['abs(mupluseta-muminuseta)','abs(genmupluseta-genmuminuseta)'],
			'lumis':  lumi[year],
			'energies' : [13],
			'y_bins': ['30,0,3'],
			#'y_errors' : False,
			'nicks_whitelist': [sets],
			'weights': ['(leptonSFWeight)', '1'],	
			'labels' : ['Reco', 'Gen'],
			'markers': ['o', 'o'],
			'marker_fill_styles': ['full', 'none'],
			'x_errors': [True],
			'analysis_modules': ['ConvertToHistogram','Ratio'],
			'x_bins' : ['30 40 50 60 80 100 120 140 170 200 1000'],
			#'y_bins' : ['2 3 4'],
			'colors' : ['black', 'red'], 
			"filename" : 'deltaeta_comp_'+sets,
			'y_subplot_lims' : [0.5,1.50],
			'y_subplot_label' : 'Reco/Gen',
			#'y_log' : True,
			'x_log' : True,
			'z_log' : True,
			'z_lims' : [1,1e6],
			#'z_log' : True,
			#'z_lims' : [0.0001,10],
			#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			'y_label' : r"$\\Delta \\eta(\\mu^{+},\\mu^{-})$",
			#'tree_draw_options' : 'prof',
			#'www' : 'cross_sections_2016',
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def deltaPhi(args=None):
	plots = []
	year = '16'
	for sets in ['gen', 'reco']:
		d = ({
			'files' : ['work/mc16_Iso04_loose.root','work/mc16_genCuts.root'],
			'folders' : ['zcuts_L1L2L3/ntuple','genzcuts_L1L2L3/ntuple'],
			'nicks' : ['reco', 'gen'],
			'x_expressions': ['zpt','genzpt'],
			'y_expressions': ['min(abs(muplusphi-muminusphi),6.2831-abs(muplusphi-muminusphi))','min(abs(genmuplusphi-genmuminusphi),6.2831-abs(genmuplusphi-genmuminusphi))'],
			'lumis':  lumi[year],
			'energies' : [13],
			'nicks_whitelist': [sets],
			#'y_errors' : False,
			'weights': ['(leptonSFWeight)', '1'],	
			#'labels' : ['Reco', 'Gen'],
			'y_bins': ['30,0,3'],
			'markers': ['o', 'o'],
			'marker_fill_styles': ['full', 'none'],
			'x_errors': [True],
			'analysis_modules': ['ConvertToHistogram','Ratio'],
			'x_bins' : ['30 40 50 60 80 100 120 140 170 200 1000'],
			#'y_bins' : ['2 3 4'],
			'colors' : ['black', 'red'], 
			"filename" : 'deltaphi_comp_'+sets,
			'y_subplot_lims' : [0.5,1.50],
			'y_subplot_label' : 'Reco/Gen',
			#'y_log' : True,
			'x_log' : True,
			'z_log' : True,
			'z_lims' : [1,1e6],
			#'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			'y_label' : r"$\\Delta \\phi(\\mu^{+},\\mu^{-})$",
			#'tree_draw_options' : 'profs',
			#'www' : 'cross_sections_2016',
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def comp_cross_section_gen(args=None):
	plots = []
	for year in years:
		d = ({
			'files' : ['work/mc16_momID.root','work/zpt.root','work/zpt_CT14.root','work/zpt_hera.root','work/zpt_abm.root'],
			'folders' : ['genzcuts/ntuple','','','',''],
			'nicks' : ['data', 'nnpdf','ct14','hera','abm'],
			'x_expressions': ['genzpt','0','0','0','0'],
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			#'nicks_whitelist' : ['uncertainties','simunc', 'nnpdf','ct10','ratio'],
			'y_errors' : False,
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			'weights' : ['genzmass>81.2&genzmass<101.2','1','1','1','1'],
			'histograms_to_normalize_by_binwidth' : 'data',
			'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['.','_','_','_','_','_','_','_','_','_'],	
			'labels' : ['GenlevelMC', 'NNPDF30','CT14','HERAPDF20','ABM11'],
			'x_bins' : ['30 40 50 60 80 100 120 140 170 200 1000'],
			'analysis_modules' : ['NormalizeByBinWidth', 'Ratio','PrintBinContent'],
			'ratio_numerator_nicks' : ['data','data','data','data'],
			'ratio_denominator_nicks' : ['nnpdf','ct14','hera','abm'],
			'y_subplot_label' : 'Data/MC',
			'colors' : ['black', 'red', 'blue', 'green', 'purple','red','blue','green','purple'], 
			"filename" : 'sim_comp_pt',
			'scale_factors' : [scalefactors[year], '1','1','1','1'],
			#'subplot_legend' : 'upper right',
			'x_log' : True,
			'y_subplot_lims' : [0.90,1.10],
			'y_log' : True,
			'x_ticks' : [30, 40, 60, 100, 200, 400, 1000],
			'x_lims' : [30,1000],
			'y_lims' : [0.001, 6],
			'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
			#'www' : 'cross_sections_20'+year,
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
   
