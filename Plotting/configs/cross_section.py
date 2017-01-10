# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files

import argparse
import copy
import math

# TODO to more general location
y_bins = ['0','0.6','1.2','1.8', '2.4']
observe = ['zpt', 'abs(zy)', 'phistareta']
years = ['16']
binzpt = '30 40 50 60 80 100 120 140 170 200 1000'
binsphistar = '0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.115 0.130 0.145 0.165 0.190 0.220 0.26 0.310 0.390 0.520 0.7 1.0 1.15 1.5 2.0 2.5 3.25 5 10'
modes = ['mean']
lumi = {'15': [2.169127], 
	'16': [12.05550], # Run BCD
	#'16' : [6.138487502] #Run EF
	#'16' : [4.851476655999999] #Run G
}
scalefactors = {'15': '0.0004610419548178884', 
		'16' : '8.294969101240099e-05', #Run BCD 
		#'16' : '0.00016290657913275652' #Run EF
		#'16' : '0.00020612280979714975' #Run G
}
def get_bkg_uncertainty(args=None):
	plots = []

	for obs in observe:
		for year in years:
			d = ({
				'files' : ['work/data'+year+'_leptoncuts.root', 'work/mc15_bkg_ZZ.root','work/mc15_bkg_ZW.root','work/mc15_bkg_WW.root','work/mc15_bkg_WJets.root','work/mc15_bkg_ttJets.root', 'work/mc15_bkg_Ztautau.root'],
				'zjetfolders' : 'zcuts',
				'algorithms' : [''],
				'corrections' : 'L1L2L3',
				'x_expressions' : obs,
				'nicks' : ['data', 'ZZ', 'ZW', 'WW', 'WJets', 'ttJets', 'Ztautau'],
				'legend' : None,
				'nicks_whitelist' : ['relbkg'],
				'analysis_modules' : ['SumOfHistograms','Divide','PrintBinContent'],
				'divide_denominator_nicks' : ['data'],
				"divide_numerator_nicks" : ['bkg'],
				"divide_result_nicks" : ['relbkg'],
				'x_errors': [1],
				'markers': 'd',
				'lumis': lumi[year],
				'y_subplot_label' : 'Bkg/Data', 
				'y_subplot_lims': [0, 0.1],
				"sum_nicks" : ['ZZ ZW WW WJets ttJets Ztautau'],
				"sum_scale_factors" : ["1 1 1 1 1 1"],
				"sum_result_nicks" : ['bkg'],
				'output_dir' : 'files/'+year,
				"filename" : 'bkg_uncertainty_'+obs,
				'plot_modules': ['ExportRoot'],
				'file_mode': ('RECREATE'),
				'y_log' : True,
			})
			if obs == 'zpt':
				d['x_bins'] = ['30 40 50 60 80 100 120 140 170 200 1000']
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['weights'] =  y_bins[i-1]+'<zy&zy<'+y_bins[i] if i is not 0 else '1',
					d2['filename'] = 'bkg_uncertainty_'+obs+'_'+str(i)
					plots.append(d2)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				plots.append(d)
			elif obs == 'zy':
				d['x_bins'] = ['46,-2.3,2.3']
				plots.append(d)
			elif obs == 'zmass':
				d['x_bins'] = ['20,81,101']
				plots.append(d)
			elif obs == 'phistareta':
				d['x_bins'] = [binsphistar],
				d['zjetfolders'] = 'leptoncuts'
				d['weights'] = 'zpt>5'
				plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def get_IDTrigger_uncertainties(args=None):
	plots = []
	for sf in ['ID','Trigger']:
		for obs in observe:
			for year in years:		
				d = ({
					#'files' : ['files/'+year+'/unfolded_data_'+obs+'_mean.root','files/'+year+'/unfolded_data_'+obs+'_'+sf+'up.root','files/'+year+'/unfolded_data_'+obs+'_'+sf+'down.root'],
					'files' : ['work/data'+year+'_leptoncuts.root','work/data'+year+'_leptoncuts.root'],
					'folders' : ['zcuts_L1L2L3_mean/ntuple','zcuts_L1L2L3_'+sf+'up/ntuple'],
					'x_expressions': obs,
					'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
					'y_errors' : False,
					'x_errors': [1],
					'weights' : '(leptonSFWeight*leptonTriggerSFWeight)',
					'nicks' : ['mean', 'scaleup'],
					'markers': ['d', 'd'],
					'nicks_whitelist' : ['reldiffup'],
					"sum_nicks" : ['mean scaleup'],
					"sum_scale_factors" : ['-1 1'],
					"sum_result_nicks" : ['diffup'],
					'divide_denominator_nicks' : ['mean'],
					"divide_numerator_nicks" : ['diffup'],
					"divide_result_nicks" : ['reldiffup'],
					'x_lims' : [30,1000],
					'plot_modules': ['ExportRoot'],
					'file_mode': ('RECREATE'),
					'analysis_modules' : ['NormalizeByBinWidth','SumOfHistograms','Divide','PrintBinContent'],
					'output_dir' : 'files/'+year+'/',
					"filename" : sf+'_uncertainty_'+obs,
					'x_log' : True,
					'y_label' : "Rel. Uncertainty / %",
					'scale_factors' : scalefactors[year],
				})	
				if obs == 'zpt':
					d['x_bins'] = ['30 40 50 60 80 100 120 140 170 200 1000']
					for i in range(len(y_bins)):
						d2 = copy.deepcopy(d)
						#d2['files'] = ['files/'+year+'/signal_'+obs+'_'+str(i)+'_mean.root','files/'+year+'/signal_'+obs+'_'+str(i)+'_'+sf+'up.root','files/'+year+'/signal_'+obs+'_'+str(i)+'_'+sf+'down.root'],
						d2['weights'] =  '(leptonSFWeight*leptonTriggerSFWeight)*('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')' if i is not 0 else '(leptonSFWeight*leptonTriggerSFWeight)'
						d2['filename'] = sf+'_uncertainty_'+obs+'_'+str(i)
						plots.append(d2)
				elif obs == 'abs(zy)':
					d['x_bins'] = ['23,0,2.3']
					plots.append(d)
				elif obs == 'zy':
					d['x_bins'] = ['46,-2.3,2.3']
					plots.append(d)
				elif obs == 'zmass':
					d['x_bins'] = ['20,81,101']
					plots.append(d)
				elif obs == 'phistareta':
					d['x_bins'] = [binsphistar],
					plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def get_poisson_uncertainty(args=None):
	plots = []
	for obs in observe:
		for year in years:		
			d = ({
				'files' : ['files/'+year+'/cov_mat_'+obs+'.root', 'work/data'+year+'_leptoncuts.root'],
				'folders' : ['', 'zcuts_L1L2L3_mean/ntuple'],
				'analysis_modules' : ['GetErrorFromCovMat', 'Divide', 'PrintBinContent'],
				'divide_denominator_nicks' : ['data'],
				"divide_numerator_nicks" : ['matrix'],
				"divide_result_nicks" : ['error'],
				'plot_modules': ['ExportRoot'],
				'output_dir' : 'files/'+year+'/',
				'nicks' : ['matrix', 'data'],
				'filename' : 'poisson_uncertainty_'+obs,
				'x_expressions': ['cov_matrix', obs],
				'scale_factors' : ['1', scalefactors[year]]
			})
			if obs == 'zpt':
				d['x_bins'] = ['30 40 50 60 80 100 120 140 170 200 1000']
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['weights'] = y_bins[i-1]+'<zy&zy<'+y_bins[i] if i is not 0 else '1'
					d2['filename'] = 'poisson_uncertainty_'+obs+'_'+str(i)
					d2['files'] = ['files/'+year+'/cov_mat_'+obs+'_'+str(i)+'.root','work/data'+year+'_leptoncuts.root'],
					plots.append(d2)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				plots.append(d)
			elif obs == 'zy':
				d['x_bins'] = ['46,-2.3,2.3']
				plots.append(d)
			elif obs == 'zmass':
				d['x_bins'] = ['20,81,101']
				plots.append(d)
			elif obs == 'phistareta':
				d['x_bins'] = [binsphistar],
				d['folders'] = ['', 'leptoncuts_L1L2L3/ntuple']
				d['weights'] = ['1', 'zpt>5']
				plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def print_results(args=None):
	plots = []
	for obs in observe:
		for year in years:		
			d = ({
				'files' : ['files/'+year+'/signal_'+obs+'_mean.root', 'files/'+year+'/poisson_uncertainty_'+obs+'.root', 'files/'+year+'/bkg_uncertainty_'+obs+'.root','files/'+year+'/ID_uncertainty_'+obs+'.root','files/'+year+'/Trigger_uncertainty_'+obs+'.root'],
				'folders' : [''],
				'analysis_modules' : ['NormalizeByBinWidth','PrintResults'],
				'histograms_to_normalize_by_binwidth' : ['a'],
				'filename' : 'results_'+obs+'_'+year,
				'nicks' : ['a', 'b', 'c','d', 'e'],
				'x_expressions': ['signal','error','relbkg','reldiffup','reldiffup'],
				'scale_factors' :[scalefactors[year],'100','50','100','100'],
				})
			if obs == 'zpt':
				d['x_bins'] = ['30 40 50 60 80 100 120 140 170 200 1000']
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['files'] = ['files/'+year+'/signal_'+obs+'_'+str(i)+'_mean.root', 'files/'+year+'/poisson_uncertainty_'+obs+'_'+str(i)+'.root', 'files/'+year+'/bkg_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/ID_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/Trigger_uncertainty_'+obs+'_'+str(i)+'.root']
					d2['filename'] = 'results_'+obs+'_'+str(i)+'_'+year
					plots.append(d2)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				plots.append(d)
			elif obs == 'zy':
				d['x_bins'] = ['46,-2.3,2.3']
				plots.append(d)
			elif obs == 'zmass':
				d['x_bins'] = ['20,81,101']
				plots.append(d)
			elif obs == 'phistareta':
				d['x_bins'] = [binsphistar],
				plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def get_signal(args=None):
	plots = []
	for obs in observe:
		for year in years:
			for mode in modes:
				d = ({
					'files' : ['work/data'+year+'_leptoncuts.root', 'work/mc15_bkg_ZZ.root','work/mc15_bkg_ZW.root','work/mc15_bkg_WW.root','work/mc15_bkg_WJets.root','work/mc15_bkg_ttJets.root', 'work/mc15_bkg_Ztautau.root',],
					'folders' : 'zcuts_L1L2L3_'+mode+'/ntuple',
					'x_expressions': obs,
					'weights' : '(leptonSFWeight*leptonTriggerSFWeight)',
					'y_errors' : False,
					'nicks' : ['data', 'ZZ', 'ZW', 'WW', 'WJets', 'ttJets', 'Ztautau'],
					#'labels' : ['Signal', 'ZZ', 'ZW', 'WW', 'WJets', 'ttJets', 'Ztautau'],
					'legend' : None,
					'nicks_blacklist' : ['bkg'],
					'analysis_modules' : ['SumOfHistograms','Ratio','PrintBinContent'],
					#'plot_modules' : ['PlotMplZJet', 'PlotMplLegendTable'],
					'ratio_numerator_nicks' : ['bkg'],
					'ratio_denominator_nicks' : ['signal'],
					'ratio_result_nicks' : ['ratio'],
					'x_errors': [1],
					'markers': 'd',
					'colors' : ['black','black', 'red', 'blue', 'green', 'purple', 'yellow', 'cyan', 'black'],
					'lumis': lumi[year],
					#"legend_table_row_headers" : [r'$Z(\\rightarrow\\mu\\mu)$+Jets', 'ZZ', 'ZW', 'WW', 'WJets', 'ttJets', 'Ztautau'],
					#"legend_table_column_headers" : ['     '],
					#"legend_table_invert" : False,
					#'x_bins' : ['23,0,2.3'],
					#"legend_table_filename" : "bkg_legend",
					'y_subplot_label' : 'Bkg/Data', 
					'y_subplot_lims': [0, 0.1],
					"sum_nicks" : ['data ZZ ZW WW WJets ttJets Ztautau','ZZ ZW WW WJets ttJets Ztautau'],
					"sum_scale_factors" : ["1 -1 -1 -1 -1 -1 -1","1 1 1 1 1 1"],
					"sum_result_nicks" : ['signal','bkg'],
					#'labels' : 'zy',
					#"y_label": 'Events/BinWidth',
					'plot_modules': ['ExportRoot'],
					'file_mode': ('RECREATE'),
					#'x_log' : True,
					'y_log' : True,
					'output_dir' : 'files/'+year+'/',
					'filename' : 'signal_'+obs+'_'+mode,
					#'y_lims' : [1,5e5],
					#'x_ticks' : [40, 60, 100, 140, 200, 1000],
					#'y_label' : r"$\\frac{d\\sigma}{dp_\\mathrm{T,Z}}$ / pb$^{-1}$",
					#'scale_factors' :scalefactors[year],
					###'www' : 'cross_sections_2015',
				})
				if obs == 'zpt':
					d['x_bins'] = ['30 40 50 60 80 100 120 140 170 200 1000']
					for i in range(len(y_bins)):
						d2 = copy.deepcopy(d)
						d2['weights'] =  '(leptonSFWeight*leptonTriggerSFWeight)*('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')' if i is not 0 else '(leptonSFWeight*leptonTriggerSFWeight)'
						d2['filename'] = 'signal_'+obs+'_'+str(i)+'_'+mode
						plots.append(d2)
				elif obs == 'abs(zy)':
					d['x_bins'] = ['23,0,2.3']
					plots.append(d)
				elif obs == 'zy':
					d['x_bins'] = ['46,-2.3,2.3']
					plots.append(d)
				elif obs == 'zmass':
					d['x_bins'] = ['20,81,101']
					plots.append(d)
				elif obs == 'phistareta':
					d['x_bins'] = [binsphistar],
					d['folders'] = 'leptoncuts_L1L2L3_'+mode+'/ntuple'
					d['weights'] = '(zpt>5)*(leptonSFWeight*leptonTriggerSFWeight)'
					plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def unfold(args=None):
	plots = []
	for obs in observe:
		for year in years:
			for mode in ['mean']:
				d = ({
					'files' : ['files/'+year+'/signal_'+obs+'_'+mode+'.root','work/mc'+year+'_leptoncuts.root','work/mc'+year+'_genCuts.root','work/mc'+year+'_leptoncuts.root'],
					'folders' : ['' ,'zcuts_L1L2L3/ntuple','genzcuts_L1L2L3/ntuple','zcuts_L1L2L3/ntuple'],
					'analysis_modules': ['Unfolding','NormalizeByBinWidth','PrintBinContent'],
					'plot_modules' : ['ExportRoot'],
			    		# configure input and output nicks:
					'weights' : ['1','leptonSFWeight','1','(genzpt>30&genmupluspt>22&genmuminuspt>22&abs(genmupluseta)<2.3&abs(genmuminuseta)<2.3)'],
			    		'unfolding': 'data',
			    		'unfolding_mc_gen': 'mc_gen',
			    		'unfolding_mc_reco': 'mc_reco',
			    		'unfolding_new_nicks': 'unfolded',
					'write_matrix' : True if mode == 'mean' else False, 
					'unfold_file' : ['files/'+year+'/cov_mat_'+obs+'.root'],
					'lumis': lumi[year],
					'nicks_blacklist': ['data','mc_reco', 'mc_gen','responsematrix'],
			    		'unfolding_responsematrix': 'responsematrix',  
					'libRooUnfold': '/home/afriedel/Excalibur_481/RooUnfold/libRooUnfold.so',
					'labels' : 'None',
					'x_log' : True,
					'y_log' : True,
					'z_lims' : [1,1e5],
					'nicks' : ['data','mc_reco', 'mc_gen','responsematrix'],
					#'x_bins' : ['23,0,2.3'],
					'output_dir' : 'files/'+year+'/',
					'filename' : 'unfolded_data_'+obs+'_'+mode,
					'scale_factors' : scalefactors[year],
				})
				if obs == 'zpt':
					d['x_bins'] = ['30 40 50 60 80 100 120 140 170 200 1000']
					d['y_expressions'] = [None,None,None,'genzpt'],
			    		d['x_expressions'] = ['signal', 'zpt','genzpt', 'zpt'],
			    		d['y_bins'] = [None, None,None, '30 40 50 60 80 100 120 140 170 200 1000'],
					for i in range(len(y_bins)):
						d2 = copy.deepcopy(d)
						if i != 0:
							d2['weights'] = ['1', '('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')*(leptonSFWeight)','('+y_bins[i-1]+'<abs(genzy)&abs(genzy)<'+y_bins[i]+')','('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+'&'+y_bins[i-1]+'<abs(genzy)&abs(genzy)<'+y_bins[i]+')']
						d2['files'] = ['files/'+year+'/signal_'+obs+'_'+str(i)+'_'+mode+'.root','work/mc'+year+'_leptoncuts.root','work/mc'+year+'_genCuts.root','work/mc'+year+'_leptoncuts.root']
						d2['filename'] = 'unfolded_data_'+obs+'_'+str(i)+'_'+mode
						d2['unfold_file'] = ['files/'+year+'/cov_mat_'+obs+'_'+str(i)+'.root'],
						plots.append(d2)
				elif obs == 'abs(zy)':
					d['x_bins'] = ['23,0,2.3']
					d['y_expressions'] = [None,None,None,'abs(genzy)'],
			    		d['x_expressions'] = ['signal', 'abs(zy)','abs(genzy)', 'abs(zy)'],
			    		d['y_bins'] = [None, None,None, '23,0,2.3'],
					plots.append(d)
				elif obs == 'zy':
					d['x_bins'] = ['46,-2.3,2.3']
					d['y_expressions'] = [None,None,None,'genzy'],
			    		d['x_expressions'] = ['signal', 'zy','genzy', 'zy'],
			    		d['y_bins'] = [None, None,None, '46,-2.3,2.3'],
					plots.append(d)
				elif obs == 'zmass':
					d['x_bins'] = ['20,81,101']
					d['y_expressions'] = [None,None,None,'genzmass'],
			    		d['x_expressions'] = ['signal', 'zmass','genzmass', 'zmass'],
			    		d['y_bins'] = [None, None,None, '20,81,101'],
					plots.append(d)
				elif obs == 'phistareta':
					d['x_bins'] =  [binsphistar],
					d['y_expressions'] = [None,None,None,'genphistareta'],
			    		d['x_expressions'] = ['signal', 'phistareta','genphistareta', 'phistareta'],
			    		d['y_bins'] = [None, None,None, binsphistar],
					d['folders'] = ['' ,'leptoncuts_L1L2L3/ntuple','genleptoncuts_L1L2L3/ntuple','leptoncuts_L1L2L3/ntuple'],
					d['weights'] = ['1', '(leptonSFWeight)*(zpt>5)', 'genzpt>5', '(zpt>5&genzpt>5)*(genmupluspt>22&genmuminuspt>22&abs(genmupluseta)<2.3&abs(genmuminuseta)<2.3)']
					plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def ratio_cross_section_pt(args=None):
	plots = []
	for obs in ['abs(zy)']:
		for year in ['16']:
			d = ({
				'input_modules' : ['InputRoot', 'InputFastNLO'],
				'fastnlo_files' : ['work/'+obs+'.tab','work/'+obs+'.tab'],
				'pdf_sets' : 'NNPDF30_nlo_as_0118',
				'uncertainty_style' : ['kHessianAsymmetric','kAsymmetricSixPoint'],
				'uncertainty_type' : ['PDF', 'Scale'],
				'files' : ['files/'+year+'/unfolded_data_'+obs+'_mean.root', 'files/'+year+'/uncertainties_'+obs+'.root'],
				'folders' : '',
				'nicks' : ['data', 'errors'],
				'x_expressions': ['unfolded','Total'],
				'y_errors' : True,
				'fastnlo_nicks' : ['nnpdf_pdf','nnpdf_scale'],
				'x_errors': [1],
				'y_lims': [0.8,1.3],
				'lumis':  lumi[year],
				'nicks_whitelist' : ['div'],
				'energies' : [13],
				'lines' : [1],
				'alphas' : [0.6, 0.6, 1],
				'step' : True,
				'zorder' : ['div_data','div_nnpdf_pdf','div_nnpdf_scale'],
				'labels' : ['PDFUnc', 'ScaleUnc','Data'],
				'legend' : 'upper right',
				'markers': ['fill','fill','.'],
				#'x_bins' : ['30 40 50 60 80 100 120 140 170 200 1000'],
				#'x_lims' : [30,1000],
				'analysis_modules' : ['Errorband', 'Divide', 'PrintBinContent'],
				'errorband_histogram_nicks' : ['data errors errors'],
				'errorband_result_nicks' : ['uncertainties'],
				'errorband_percentage_error' : True,
				'divide_numerator_nicks' : ['nnpdf_pdf','nnpdf_scale','uncertainties'],
				'divide_denominator_nicks' : ['nnpdf_pdf','nnpdf_scale','nnpdf_pdf'],
				'divide_result_nicks' : ['div_nnpdf_pdf','div_nnpdf_scale','div_data'],
				"divide_tgraphs" : [True, True, False],
				'y_label' : 'Ratio to NNPDF30',
				'colors' : ['orange','lightblue', 'black'], 
				"filename" : 'ratio_pt_'+obs,
				'x_log' : True,		
				#'x_ticks' : [30, 40, 60, 100, 200, 400, 1000],
				#'www' : 'cross_sections_20'+year,
			})
			if obs == 'zpt':
				d['x_bins'] = ['30 40 50 60 80 100 120 140 170 200 1000']
				d['files'] = ['files/'+year+'/unfolded_data_'+obs+'_0_mean.root', 'files/'+year+'/uncertainties_'+obs+'.root'],
				d.update({'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV'})
				d['x_lims'] = [30,1000]
				plots.append(d)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				d.update({'x_label' : r'|$\\mathit{y}_Z$|',
					  'fastnlo_files' : ['work/abszy.tab','work/abszy.tab'],
				})
				d['x_log'] = False
				plots.append(d)
			elif obs == 'zy':
				d['x_bins'] = ['46,-2.3,2.3']
				plots.append(d)
			elif obs == 'zmass':
				d['x_bins'] = ['20,81,101']
				plots.append(d)
			elif obs == 'phistareta':
				d['x_bins'] = [binsphistar],
				d.update({'x_label' : r'$\\phi^*_\\eta$'})
				d['x_lims'] = [0.02,10]
				plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def comp_cross_section_pt(args=None):
	plots = []
	for year in years:
		d = ({
			'files' : ['files/'+year+'/unfolded_data_zpt_0_mean.root','work/zpt.root','work/zpt_CT14.root','work/zpt_hera.root','work/zpt_abm.root'],
			'folders' : ['','','','',''],
			'nicks' : ['data', 'nnpdf','ct14','hera','abm'],
			'x_expressions': ['unfolded','0','0','0','0'],
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			#'nicks_whitelist' : ['uncertainties','simunc', 'nnpdf','ct10','ratio'],
			'y_errors' : False,
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			
			'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['.','_','_','_','_','_','_','_','_','_'],	
			'labels' : ['Data', 'NNPDF30','CT14','HERAPDF20','ABM11'],
			'x_bins' : ['30 40 50 60 80 100 120 140 170 200 1000'],
			'analysis_modules' : ['PrintBinContent', 'Ratio'],
			'ratio_numerator_nicks' : ['data','data','data','data'],
			'ratio_denominator_nicks' : ['nnpdf','ct14','hera','abm'],
			'y_subplot_label' : 'Data/MC',
			'colors' : ['black', 'red', 'blue', 'green', 'purple','red','blue','green','purple'], 
			"filename" : 'sim_comp_pt',
			#'scale_factors' : '
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
def comp_unfolding(args=None):
	plots = []
	for obs in observe:
		for year in years:
			d = ({
				'files' : ['files/'+year+'/unfolded_data_'+obs+'_mean.root','files/'+year+'/signal_'+obs+'_mean.root'],
				'folders' : ['',''],
				'nicks' : ['Unfolded', 'signal'],
				'x_expressions': ['unfolded','signal'],
				'y_errors' : False,
				'x_errors': [1],
			#'y_lims' : [0.001, 6],
				'markers': ['d', 'd'],
				'lumis':  lumi[year],
				'energies' : [13],
				'labels' : ['Unfolded Data', 'Data'],
				'analysis_modules' : ['NormalizeByBinWidth','PrintBinContent', 'Ratio'],
				'histograms_to_normalize_by_binwidth' : 'signal',
				'colors' : ['blue', 'black'], 
				"filename" : 'unfolding_comp_'+obs,
				'subplot_legend' : 'upper right',
				'y_subplot_lims' : [0.90,1.10],
				'y_log' : True,
				'scale_factors' :['1',scalefactors[year]],
				#'www' : 'cross_sections_20'+year,
			})
			if obs == 'zpt':
				d['x_bins'] = ['30 40 50 60 80 100 120 140 170 200 1000']
				d['x_ticks'] = [30, 40, 60, 100, 200, 400, 1000]
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['filename'] = 'unfolding_comp_'+obs+'_'+str(i)
					d2['files'] = ['files/'+year+'/unfolded_data_'+obs+'_'+str(i)+'_mean.root','files/'+year+'/signal_'+obs+'_'+str(i)+'_mean.root'],
					d2['x_log'] = True
					d2['y_lims'] = [0.001, 6]
					d2.update({
						'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
						'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$",
					})
					plots.append(d2)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				d.update({
					'y_label' : r"$\\frac{d\\sigma}{d|y_\\mathrm{Z}|}$ / pb",
					'x_label' : r'|$\\mathit{y}_Z$|'
				})
				plots.append(d)
			elif obs == 'phistareta':
				d['x_bins'] = [binsphistar],
				d['x_log'] = True
				d.update({
					'x_label': r'$\\phi^*_\\eta$',
					'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb"
				})
				plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def comp_cross_section_y(args=None):
	plots = []
	for year in years:
		d = ({
			'files' : ['files/'+year+'/unfolded_data_abs(zy)_mean.root','work/abszy.root','work/abszy_CT14.root','work/abszy_hera.root','work/abszy_abm.root'],
			'folders' : ['','','','',''],
			'nicks' : ['data', 'nnpdf','ct14','hera','abm'],
			'x_expressions': ['unfolded','0','0','0','0'],
			'x_label' : r'|$\\mathit{y}_Z$|',
			'y_errors' : False,
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
			'labels' : ['Data', 'NNPDF30','CT14','HERAPDF20','ABM11'],
			'x_bins' : ['23,0,2.3'],
			'analysis_modules' : ['PrintBinContent','Ratio'],
			'ratio_numerator_nicks' : ['data','data','data','data'],
			'ratio_denominator_nicks' : ['nnpdf','ct14','hera','abm'],
			'colors' : ['black', 'red', 'blue', 'green', 'purple','red','blue','green','purple'], 
			"filename" : 'sim_comp_y',
			'y_subplot_lims' : [0.90,1.10],
			'y_subplot_label' : 'Data/MC',
			'y_log' : True,
			'legend' : 'lower left',
			'y_label' : r"$\\frac{d\\sigma}{d|y_\\mathrm{Z}|}$ / pb",
			#'www' : 'cross_sections_20'+year,
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def uncertainties_y(args=None):
	plots = []
	for year in years:
		d = ({
			'files' : ['files/'+year+'/uncertainties_zpt_1.root','files/'+year+'/uncertainties_zpt_2.root','files/'+year+'/uncertainties_zpt_3.root','files/'+year+'/uncertainties_zpt_4.root'],
			'folders' : '',
			'nicks' : ['bin1', 'bin2', 'bin3', 'bin4'],
			'x_expressions': 'Statistical',
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			'y_errors' : False,
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			#'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['o','d','^','s'],	
			'labels' : [r"$|y_\\mathrm{Z}|<0.6$", r"$0.6<|y_\\mathrm{Z}|<1.2$", r"$1.2<|y_\\mathrm{Z}|<1.8$", r"$1.8<|y_\\mathrm{Z}|<2.3$"],
			'x_bins' : [binzpt],
			'x_ticks' : [30, 40, 60, 100, 200, 400, 1000],
			'x_lims' : [30,1000],
			'analysis_modules' : ['PrintBinContent'],
			'colors' : ['black', 'red', 'blue', 'green'], 
			"filename" : 'uncertainties_y',
			'x_log' : True,
			'y_label' : "Stat Uncertainty / %",
			#'www' : 'cross_sections_20'+year,
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def comp_cross_section_pt_over_y(args=None):
	plots = []
	for year in years:
		d = ({
			'files' : ['files/'+year+'/unfolded_data_zpt_1_mean.root','files/'+year+'/unfolded_data_zpt_2_mean.root','files/'+year+'/unfolded_data_zpt_3_mean.root', 'files/'+year+'/unfolded_data_zpt_4_mean.root','work/y0_zpt.root','work/y1_zpt.root','work/y2_zpt.root','work/y3_zpt.root'],
			'folders' : '',
			'nicks' : ['data1', 'data2','data3','data4', 'nnpdf1', 'nnpdf2', 'nnpdf3', 'nnpdf4'],
			'x_expressions': ['unfolded','unfolded','unfolded','unfolded','0','0','0','0'],
			'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			#'nicks_whitelist' : ['uncertainties','simunc', 'nnpdf','ct10','ratio'],
			'y_errors' : False,
			'x_errors': [0,0,0,0,1,1,1,1],
			'y_lims' : [0.0005, 6000],
			'lumis':  lumi[year],
			'energies' : [13],
			#'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['o','d','^','s','_','_','_','_','o','d','^','s'],	
			'legend' : 'None',
			'plot_modules' : ['PlotMplZJet', 'PlotMplLegendTable'],
			'x_bins' : ['30 40 50 60 80 100 120 140 170 200 1000'],
			#'x_lims' : [30,1000],
			"legend_table_row_headers" : [r"$|y_\\mathrm{Z}|<0.6\\cdot 10^{3}$", r"$0.6<|y_\\mathrm{Z}|<1.2\\cdot 10^{2}$", r"$1.2<|y_\\mathrm{Z}|<1.8\\cdot 10^{1}$", r"$1.8<|y_\\mathrm{Z}|<2.3$"],
			"legend_table_column_headers" : ['Data', 'NNPDF'],
			'analysis_modules' : ['PrintBinContent', 'Ratio'],
			'ratio_numerator_nicks' : ['data1','data2','data3','data4'],
			'ratio_denominator_nicks' : ['nnpdf1','nnpdf2','nnpdf3','nnpdf4'],
			'y_subplot_label' : 'Data/MC',
			'colors' : ['black','red','blue','green','black','red','blue','green','black','red','blue','green'], 
			"filename" : 'sim_comp_pt_over_y',
			#'scale_factors' : '
			#'subplot_legend' : 'upper right',
			'x_log' : True,
			'y_subplot_lims' : [0.90,1.10],
			'scale_factors' : [1000, 100,10, 1,1000,100,10, 1],
			'y_log' : True,
			'x_ticks' : [30, 40, 60, 100, 200, 400, 1000],
			'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}d|y_\\mathrm{Z}|}$ / pb $\\mathrm{GeV}^{-1}$",
			#'www' : 'cross_sections_20'+year,
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
	
def comp_cross_section_phistar(args=None):
	plots = []
	for year in years:
		d = ({
			'files' : ['files/'+year+'/unfolded_data_phistareta_mean.root','work/phistareta.root','work/phistareta_CT14.root','work/phistareta_hera.root','work/phistareta_abm.root'],
			'folders' : '',
			'nicks' : ['data', 'nnpdf','ct14','hera','abm'],
			'x_expressions': ['unfolded','0','0','0','0'],
			'x_label' : r'$\\phi^*_\\eta$',
			'y_errors' : False,
			'x_errors': [1],
			'lumis':  lumi[year],
			'energies' : [13],
			#'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
			'labels' : ['Data', 'NNPDF30','CT14','HERAPDF20','ABM11'],
			'x_bins' : [binsphistar],
			'analysis_modules' : ['Ratio','PrintBinContent'],
			'ratio_numerator_nicks' : ['data','data','data','data'],
			'ratio_denominator_nicks' : ['nnpdf','ct14','hera','abm'],
			'colors' : ['black', 'red', 'blue', 'green', 'purple','red','blue','green','purple'], 
			"filename" : 'sim_comp_phistar',
			'y_subplot_lims' : [0.90,1.10],
			'y_subplot_label' : 'Data/MC',
			'y_lims' : [0.1, 8500],
			'y_log' : True,
			'x_log' : True,
			'legend' : 'lower left',
			#'x_ticks' : [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,10],
			#'scale_factors' :[scalefactors[year],'1'],
			'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb",
			#'www' : 'cross_sections_20'+year,
		})
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]



def plot_uncertainties(args=None, export=False):
	plots = []
	for year in years:
		for obs in observe:
			d = ({
				'files' : ['files/'+year+'/Trigger_uncertainty_'+obs+'.root','files/'+year+'/ID_uncertainty_'+obs+'.root','files/'+year+'/uncertainty_Lumi_'+obs+'.root','files/'+year+'/bkg_uncertainty_'+obs+'.root','files/'+year+'/poisson_uncertainty_'+obs+'.root'],
				'folders' : '',
				'x_expressions': ['reldiffup','reldiffup','lumi','relbkg','error'],
				'y_errors' : False,
				'x_errors': [1],
				'markers': ['d'],
				'nicks' : ['Trigger', 'ID', 'Lumi', 'Bkg','Poisson'],
				'labels' : ['Trigger Efficiency', 'ID+Iso+trk Efficiency', 'Lumi', 'Background','Statistical','Total'],
				'analysis_modules' : ['AverageHistograms', 'PrintBinContent'],
				'to_average_nicks' : ['Trigger', 'ID', 'Lumi', 'Bkg','Poisson'],
				'average_result_nick' : 'Total',
				'averaging_method' : 'rmssum',
				#'output_dir' : 'files/'+year+'/',
				"filename" : 'uncertainties_'+obs,
				'y_lims' : [0,12],
				'y_label' : "Rel. Uncertainty / %",
				'scale_factors' :['100','100','1','50','100'],
			
			})
			if export:
				d['plot_modules'] = ['ExportRoot']
				d['file_mode']= ('RECREATE')
				d['output_dir'] = 'files/'+year+'/'
			#else: 	
				#d['www'] = 'cross_sections_20'+year
			if obs == 'zpt':
				d['x_bins'] = ['30 40 50 60 80 100 120 140 170 200 1000']
				d['x_ticks'] = [30, 40, 60, 100, 200, 400, 1000],
				d['x_log'] = True,
				d['x_lims'] = [30,1000],
				d['x_label'] = r'$\\mathit{p}_{T}^{Z}$ / GeV'
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['files'] = ['files/'+year+'/Trigger_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/ID_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/uncertainty_Lumi_zpt.root','files/'+year+'/bkg_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/poisson_uncertainty_'+obs+'_'+str(i)+'.root']
					d2["filename"] = 'uncertainties_'+obs if i == 0 else 'uncertainties_'+obs+'_'+str(i)
					plots.append(d2)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				d['x_label'] = r'|$\\mathit{y}_{Z}$|'
				plots.append(d)
			elif obs == 'phistareta':
				d['x_bins'] = [binsphistar],
				d.update({'x_label' :  r'$\\phi^*_\\eta$'})
				d['x_log'] = True,
				d['x_lims'] = [0.02,10],
				plots.append(d)
			
	return [PlottingJob(plots=plots, args=args)]

def get_rootfiles(args=None):
	plotting_jobs = []
	plotting_jobs += get_signal(args)
	plotting_jobs += get_bkg_uncertainty(args)
	plotting_jobs += unfold(args)
	plotting_jobs += get_IDTrigger_uncertainties(args)
	plotting_jobs += get_poisson_uncertainty(args)
	plotting_jobs += plot_uncertainties(args,export=True)
	return(plotting_jobs)

def compare_datapdf(args=None):
	plotting_jobs = []
	plotting_jobs += comp_cross_section_pt(args)
	#plotting_jobs += ratio_cross_section_pt(args)
	plotting_jobs += comp_cross_section_y(args)
	plotting_jobs += comp_sim_pt(args)
	plotting_jobs += plot_uncertainties(args,export=False)
	plotting_jobs += comp_cross_section_pt_over_y(args)
	plotting_jobs += comp_cross_section_phistar(args)
	plotting_jobs += comp_unfolding(args)
	return(plotting_jobs)


def simple_plot(args=None):
	plots = []
	d = ({
		'files' : ['plots/signal_zmass.root','work/mc15_ PhiStarEta.root'],
		'folders' : ['','zcuts_L1L2L3/ntuple'],
		#'nicks': ['CorrectedData', 'UncorrectedData','MC'],
		#'nicks_whitelist' : 'GenZ',
		'analysis_modules' : ['Ratio'],
		#'labels': ['GenZ'],
		#'ratio_numerator_nicks' : ['CorrectedData','UncorrectedData'],
		#'ratio_denominator_nicks' : ['MC','MC'], 
		#'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
		#'weights' : 'mu1pt>22&mu2pt>22&abs(mu1eta)<2.3&abs(mu2eta)<2.3',
		#'subplot_legend': 'upper right',
		#'y_subplot_lims': [0.5, 2],
		'x_errors': [1],
		'labels' : ['Data', 'MC'],
		'lumis':  lumi[year], 
		#'plot_modules': ['ExportRoot'],
		#'markers': ['.','.','bar','o','o'],
		#'x_bins' : ['10 20 30 40 50 60 80 100 120 140 170 200 1000'],
		#'x_bins' : ['50,0,300'],
		'filename' : ' PhiStarEta',
		'x_label' : r'$\\mathit{m}^{Z}$ / GeV',
		#'y_log': True,
		#'x_log': True,
		'y_subplot_label' : 'Data/MC',
		#'colors' : ['black', 'red', 'lightblue', 'black', 'red'],
		'x_expressions': ['signal','zmass'],
		#'x_ticks' : [40, 60, 100, 140, 200, 1000],
		#'scale_factors' :scalefactors[year],
		#'www' : 'cross_sections_2015',
		'x_bins' : ['20,81,101'],
		})
	plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def zmass(args=None):
	plots = []
	d = ({
		'files' : ['work/mc16_momID.root','work/mc16_genzproducer.root'],
		'zjetfolders' : ['genleptoncuts','genleptoncuts'],
		'algorithms' : [''],
		'corrections' : [''],
		'cutlabel' : True,
		'markers': ['.','_'],
		#'x_log' : True,
		#'labels' : ['Reco+Gen Cuts', 'Only Gen Cuts'],
		'labels' : ['New Approach', 'Status 1 Muons'],
		#'weights' : 'mu1pt>22&mu2pt>22&abs(mu1eta)<2.3&abs(mu2eta)<2.3',
		#'subplot_legend': 'upper right',
		#'y_subplot_lims': [0.5, 2],
		'x_errors': [1],
		#'markers': ['_', 'd','d'],
		#'weights' : ['leptonSFWeight','1'],
		'analysis_modules' : ['PrintBinContent', 'Ratio'],
		#'markers' : ['bar','d','.','.'],
		'x_label' : r"$m_\\mathrm{genZ}$ / GeV",
		#'x_bins' : ['0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.115 0.130 0.145 0.165 0.190 0.220 0.26 0.310 0.390 0.520 0.7 1.0 1.15 1.5 2.0 2.5 3.25 5 10'],
		'y_subplot_label' : 'Data/Reco',
		'y_subplot_lims' : [0.5,1.5],
		#'colors': ['skyblue', 'red', 'blue', 'black'],
		#'x_log': True,
		'x_expressions': ['genzmass', 'genzmass'],
		#'x_ticks' : [40, 60, 100, 140, 200, 1000],
		'x_bins' : ['1,81,101'],
		})
	plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def npv(args=None):
	plots = []
	d = ({
		'files' : ['work/mc16_665.root', 'work/data16_leptoncuts.root'],
		'zjetfolders' : ['zcuts'],
		'corrections' : ['L1L2L3'],
		'analysis_modules' : ['NormalizeToUnity'],
		'x_expressions': 'npv',
		'filename' : 'npv',
		#'www' : "Matrix"
	})
	plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def matrix(args=None):
	plots = []
	d = ({
		'files' : ['work/mc16_Iso04.root'],
		'zjetfolders' : ['allzcuts'],
		'corrections' : ['L1L2L3'],
		'y_expressions' : ['genzpt'],
		'x_expressions': ['zpt'],
		#'weights' : '',
		'y_bins' : ['30 40 50 60 80 100 120 140 170 200 1000'],
		'labels' : 'None',
		'x_bins' : ['30 40 50 60 80 100 120 140 170 200 1000'],
		'x_log' : True,
		'y_log' : True,
		'z_log' : True,
		'filename' : 'responsematrix',

		'z_lims' : [1,1e5],
		#'x_ticks' : [0.02, 0.1, 1, 5],
		#'y_ticks' : [0.02, 0.1, 1, 5],
		##'www' : 'cross_sections_2015',
		###'www' : "Matrix"
	})
	plots.append(d)
	return [PlottingJob(plots=plots, args=args)]





