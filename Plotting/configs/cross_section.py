# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files

import argparse
import copy
import math

# TODO to more general location
y_bins = ['0','0.4','0.8','1.2', '1.6', '2.0', '2.4']
observe = ['zpt', 'abs(zy)', 'phistareta']
years = ['16']
#binzpt = '30 35 40 45 50 55 60 70 80 100 120 140 170 200 1000'
binzpt = '30 35 40 45 50 55 60 70 75 80 90 110 130 150 170 200 250 400'
#binzpt = '30 40 50 60 80 100 120 140 170 200 1000'
binsphistar = '0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.115 0.130 0.145 0.165 0.190 0.220 0.26 0.310 0.390 0.500 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 1.0 1.25 1.5 2 3 4 6 12 25'
modes = ['mean']
theory = 'theo_3'
lumi = {'15': [2.169127], 
	'16': [12.6], # Run BCD
	#'16' : [6.138487502] #Run EF
	#'16' : [7.544015569] #Run G
		 '16H' :	[8.746001362] #Run H
	}
scalefactors = {'15': '0.0004610419548178884', 
		'16' : '7.955607033853327e-05', #Run BCD 
		#'16' : '0.00016290657913275652' #Run EF
		#'16' : '0.00013255539982038442' #Run G
		'16H' :	0.00011433796527231776
}
scalefactors_fsr = {
                '16' : '8.576939943197271e-05', #Run BCD 
}

input_data = "work/data16_ICHEP_tl.root"
input_mc = "work/mc16_Spring16_ml.root"

def get_bkg_uncertainty(args=None):
	plots = []

	for obs in observe:
		for year in years:
			d = ({
				'files' : [input_data, 'work/data16_ICHEP_bkg_tl.root', 'work/mc16_bkg_ZZ_tl.root','work/mc16_bkg_ZW_tl.root','work/mc16_bkg_WW_tl.root','work/mc16_bkg_ttJets_tl.root', 'work/mc16_bkg_Ztautau_tl.root'],
				'zjetfolders' : 'zcuts',
				'algorithms' : [''],
				'corrections' : '',
				'x_expressions' : obs,
				'nicks' : ['data', 'misid', 'ZZ', 'ZW', 'WW', 'ttJets', 'Ztautau'],
				'legend' : None,
				'nicks_whitelist' : ['bkg'],
				'analysis_modules' : ['SumOfHistograms','Divide','PrintBinContent'],
				'divide_denominator_nicks' : ['data'],
				"divide_numerator_nicks" : ['bkg'],
				"divide_result_nicks" : ['relbkg'],	
				'x_errors': [1],
				'weights' : ['(leptonSFWeight)*(leptonTriggerSFWeight)','(leptonSFWeight)*(leptonTriggerSFWeight)', 'leptonSFWeight'],
				'markers': 'd',
				'lumis': lumi[year],
				'y_subplot_label' : 'Bkg/Data', 
				'y_subplot_lims': [0, 0.1],
				"sum_nicks" : ['misid ZZ ZW WW ttJets Ztautau'],
				"sum_scale_factors" : ["1 1 1 1 1 1"],
				"sum_result_nicks" : ['bkg'],
				'output_dir' : 'files/'+year,
				"filename" : 'bkg_uncertainty_'+obs,
				'plot_modules': ['ExportRoot'],
				'file_mode': ('RECREATE'),
				'y_log' : True,
			})
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['weights'] = ['(leptonSFWeight)*(leptonTriggerSFWeight)*('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')' if i is not 0 else '(leptonSFWeight)*(leptonTriggerSFWeight)'] 
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
				for i in range(len(y_bins)):
                                        d2 = copy.deepcopy(d)
                                        d2['weights'] = ['(leptonSFWeight)*(leptonTriggerSFWeight)*(zpt>5&'+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')' if i is not 0 else '(leptonSFWeight)*(leptonTriggerSFWeight)*(zpt>5)']
                                        d2['filename'] = 'bkg_uncertainty_'+obs+'_'+str(i)
                                        plots.append(d2)

				plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def get_IDTrigger_uncertainties(args=None):
	plots = []
	for sf in ['ID','Trigger']:
		for obs in observe:
			for year in years:		
				d = ({
					#'files' : ['files/'+year+'/unfolded_data_'+obs+'_mean.root','files/'+year+'/unfolded_data_'+obs+'_'+sf+'up.root','files/'+year+'/unfolded_data_'+obs+'_'+sf+'down.root'],
					'files' : [input_data,input_data],
					'folders' : ['zcuts_mean/ntuple','zcuts_'+sf+'up/ntuple'],
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
					d['x_bins'] = [binzpt]
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
					d['folders'] = ['zcuts_mean/ntuple','zcuts_'+sf+'up/ntuple'],
					d['x_bins'] = [binsphistar],
					for i in range(len(y_bins)):
						d3 = copy.deepcopy(d)
						d3['weights'] =  '(leptonSFWeight*leptonTriggerSFWeight)*('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+'&zpt>5)' if i is not 0 else '(leptonSFWeight*leptonTriggerSFWeight)*(zpt>5)'       
					 	d3['filename'] = sf+'_uncertainty_'+obs+'_'+str(i)
                                                plots.append(d3)
				elif obs == 'mu1pt':
					d['x_bins'] = ['27 37 47 57 67 77 87 107 125 150'],
					plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
'''def get_unfold_uncertainty(args=None):
	plots = []
	for obs in ['zpt']:
		for year in years:		
			d = ({
				'files' : ['files/'+year+'/cov_mat_'+obs+'.root', input_data],
				'folders' : ['', 'zcuts_mean/ntuple'],
				'analysis_modules' : ['GetErrorFromCovMat','Divide', 'StatisticalErrors', 'SumOfHistograms','PrintBinContent'],
				'divide_denominator_nicks' : ['data'],
				"divide_numerator_nicks" : ['matrix'],
				"divide_result_nicks" : ['stat'],
				'weights' : ['1','leptonSFWeight*leptonTriggerSFWeight'],
				'plot_modules': ['ExportRoot'],	
				"sum_nicks" : ['stat data'],
                                "sum_scale_factors" : ["100 1"],
				'stat_error_nicks' : ['data'],
				'stat_error_relative' :True,
                                'stat_error_relative_percent' : True,
                                "sum_result_nicks" : ['error'],
				'output_dir' : 'files/'+year+'/',
				'nicks' : ['matrix', 'data'],
				'filename' : 'poisson_uncertainty_'+obs,
				'x_expressions': ['cov_matrix', obs],
				'scale_factors' : ['1', scalefactors[year]]
			})
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['weights'] = ['1','leptonSFWeight*leptonTriggerSFWeight*('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')' if i is not 0 else 'leptonSFWeight*leptonTriggerSFWeight']
					d2['filename'] = 'poisson_uncertainty_'+obs+'_'+str(i)
					d2['files'] = ['files/'+year+'/cov_mat_'+obs+'_'+str(i)+'.root',input_data],
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
				d['folders'] = ['', 'leptoncuts/ntuple']
				d['weights'] = ['1', 'leptonSFWeight*leptonTriggerSFWeight*(zpt>5)']
				for i in range(len(y_bins)):
                                        d2 = copy.deepcopy(d)
                                        d2['weights'] = ['1', 'leptonSFWeight*leptonTriggerSFWeight*(zpt>5&'+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')' if i is not 0 else 'leptonSFWeight*leptonTriggerSFWeight*(zpt>5)']
                                        d2['filename'] = 'poisson_uncertainty_'+obs+'_'+str(i)
					d2['files'] = ['files/'+year+'/cov_mat_'+obs+'_'+str(i)+'.root',input_data],
                                        plots.append(d2)
				plots.append(d)
	return [PlottingJob(plots=plots, args=args)]'''

def get_unfold_uncertainty(args=None):
	plots = []
	for obs in observe:
		for year in years:		
			d = ({
				'files' : ['files/16/unfolded_data_'+obs+'_mean.root'],
				'folders' : [''],
				'analysis_modules' : ['StatisticalErrors', 'PrintBinContent'],
				'stat_error_relative' :True,
				'stat_error_relative_percent' : True,
				'plot_modules': ['ExportRoot'],
				'output_dir' : 'files/'+year+'/',
				'nicks' : ['error'],
				'labels' : 'error',
				'filename' : 'poisson_uncertainty_'+obs,
				'x_expressions': 'unfolded',
			})
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					#d2['weights'] = '('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')' if i is not 0 else '1'
					d2['filename'] = 'poisson_uncertainty_'+obs+'_'+str(i)
					d2[ 'files'] = ['files/16/unfolded_data_'+obs+'_'+str(i)+'_mean.root']
					plots.append(d2)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				plots.append(d)
			elif obs == 'zy':
				d['x_bins'] = ['46,-2.3,2.3']
				plots.append(d)
			elif obs == 'phistareta':
				d['x_bins'] = [binsphistar],
				for i in range(len(y_bins)):
                                        d3 = copy.deepcopy(d)
                                        #d2['weights'] = ['(zpt>5'+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')' if i is not 0 else 'zpt>5']
                                        d3['filename'] = 'poisson_uncertainty_'+obs+'_'+str(i)
					d3[ 'files'] = ['files/16/unfolded_data_'+obs+'_'+str(i)+'_mean.root']
                                        plots.append(d3)

	return [PlottingJob(plots=plots, args=args)]

def print_results(args=None):
	plots = []
	for obs in observe:
		for year in years:		
			d = ({
				'files' : ['files/'+year+'/unfolded_data_'+obs+'_mean.root', 'files/'+year+'/poisson_uncertainty_'+obs+'.root', 'files/'+year+'/bkg_uncertainty_'+obs+'.root','files/'+year+'/ID_uncertainty_'+obs+'.root','files/'+year+'/Trigger_uncertainty_'+obs+'.root'],
				'folders' : [''],
				'analysis_modules' : ['PrintResults'],
				'filename' : 'results_'+obs+'_'+year,
				'nicks' : ['a', 'b', 'c','d', 'e'],
				'x_expressions': ['unfolded','error','relbkg','reldiffup','reldiffup'],
				'scale_factors' :['1','1','50','100','100'],
				})
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['files'] = ['files/'+year+'/unfolded_data_'+obs+'_'+str(i)+'_mean.root', 'files/'+year+'/poisson_uncertainty_'+obs+'_'+str(i)+'.root', 'files/'+year+'/bkg_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/ID_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/Trigger_uncertainty_'+obs+'_'+str(i)+'.root']
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
				d['x_bins'] = [binsphistar]
				for i in range(len(y_bins)):
                                        d3 = copy.deepcopy(d)
                                        d3['files'] = ['files/'+year+'/unfolded_data_'+obs+'_'+str(i)+'_mean.root', 'files/'+year+'/poisson_uncertainty_'+obs+'_'+str(i)+'.root', 'files/'+year+'/bkg_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/ID_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/Trigger_uncertainty_'+obs+'_'+str(i)+'.root']
                                        d3['filename'] = 'results_'+obs+'_'+str(i)+'_'+year
                                        plots.append(d3)
	return [PlottingJob(plots=plots, args=args)]

def get_signal(args=None):
	plots = []
	for obs in observe:
		for year in years:
			for mode in modes:
				d = ({
					'files' : [input_data, 'work/data16_ICHEP_bkg_tl.root','work/mc16_bkg_ZZ_tl.root','work/mc16_bkg_ZW_tl.root','work/mc16_bkg_WW_tl.root','work/mc16_bkg_ttJets_tl.root', 'work/mc16_bkg_Ztautau_tl.root',],
					'folders' : 'zcuts/ntuple',
					'x_expressions': obs,
					'weights' : ['(leptonSFWeight)*(leptonTriggerSFWeight)', '(leptonSFWeight)*(leptonTriggerSFWeight)','leptonSFWeight'],
					'y_errors' : False,
					'nicks' : ['data', 'misid', 'ZZ', 'ZW', 'WW', 'ttJets', 'Ztautau'],
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
					"sum_nicks" : ['data misid ZZ ZW WW ttJets Ztautau','misid ZZ ZW WW ttJets Ztautau'],
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
					d['folders'] = 'leptoncuts/ntuple'
					d['x_bins'] = ['20 25 '+binzpt]
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
					d['x_bins'] = ['0.01 '+binsphistar],
					d['folders'] = 'leptoncuts/ntuple'
					for i in range(len(y_bins)):
                                                d3 = copy.deepcopy(d)
                                                d3['weights'] =  '(leptonSFWeight*leptonTriggerSFWeight)*('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+'&zpt>5)' if i is not 0 else '(leptonSFWeight*leptonTriggerSFWeight)*(zpt>5)'
                                                d3['filename'] = 'signal_'+obs+'_'+str(i)+'_'+mode
                                                plots.append(d3)
	return [PlottingJob(plots=plots, args=args)]

def unfold(args=None):
	plots = []
	for obs in observe:
		for year in years:
			for mode in ['mean']:
				d = ({
					'files' : ['files/'+year+'/signal_'+obs+'_'+mode+'.root',input_mc,input_mc,input_mc],
					'folders' : ['' ,'leptoncuts/ntuple','genleptoncuts/ntuple','allleptoncuts/ntuple'],
					'analysis_modules': ['Unfolding','NormalizeByBinWidth','PrintBinContent'],
					'plot_modules' : ['ExportRoot'],
			    		# configure input and output nicks:
					'weights' : ['1','leptonSFWeight','1','1'],
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
					'y_errors' : True,
					'nicks' : ['data','mc_reco', 'mc_gen','responsematrix'],
					#'x_bins' : ['23,0,2.3'],
					'output_dir' : 'files/16/',
					'filename' : 'unfolded_data_'+obs+'_'+mode,
					'scale_factors' : [scalefactors_fsr[year], scalefactors[year], scalefactors[year], scalefactors[year]],
				})
				if obs == 'zpt':
					d['x_bins'] = ['20 25 '+binzpt]
					d['y_expressions'] = [None,None,None,'genzpt'],
			    		d['x_expressions'] = ['signal', 'zpt','genzpt', 'zpt'],
			    		d['y_bins'] = [None, None,None, '20 25 '+binzpt],
					for i in range(len(y_bins)):
						d2 = copy.deepcopy(d)
						if i != 0:
							d2['weights'] = ['1', '('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+')*(leptonSFWeight)','('+y_bins[i-1]+'<abs(genzy)&abs(genzy)<'+y_bins[i]+')','('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+'&'+y_bins[i-1]+'<abs(genzy)&abs(genzy)<'+y_bins[i]+')']
						d2['files'] = ['files/16/signal_'+obs+'_'+str(i)+'_'+mode+'.root',input_mc,input_mc,input_mc]
						d2['filename'] = 'unfolded_data_'+obs+'_'+str(i)+'_'+mode
						d2['unfold_file'] = ['files/'+year+'/cov_mat_'+obs+'_'+str(i)+'.root'],
						plots.append(d2)
				elif obs == 'abs(zy)':
					d['x_bins'] = ['23,0,2.3']
					d['y_expressions'] = [None,None,None,'abs(genzy)'],
			    		d['x_expressions'] = ['signal', 'abs(zy)','abs(genzy)', 'abs(zy)'],
			    		d['y_bins'] = [None, None,None, '23,0,2.3'],
					d['folders'] = ['' ,'zcuts/ntuple','genzcuts/ntuple','allzcuts/ntuple'],
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
					d['x_bins'] =  ['0.01 '+binsphistar],
					d['y_expressions'] = [None,None,None,'genphistareta'],
			    		d['x_expressions'] = ['signal', 'phistareta','genphistareta', 'phistareta'],
			    		d['y_bins'] = [None, None,None, '0.01 '+binsphistar],
					d['folders'] = ['' ,'leptoncuts/ntuple','genleptoncuts/ntuple','allleptoncuts/ntuple'],
					for i in range(len(y_bins)):
                                                d3 = copy.deepcopy(d)
                                                if i != 0:
                                                        d3['weights'] = ['1', '('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+'&zpt>5)*(leptonSFWeight)','('+y_bins[i-1]+'<abs(genzy)&abs(genzy)<'+y_bins[i]+'&genzpt>5)','('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+'&'+y_bins[i-1]+'<abs(genzy)&abs(genzy)<'+y_bins[i]+'&zpt>5&genzpt>5)']
                                                d3['files'] = ['files/16/signal_'+obs+'_'+str(i)+'_'+mode+'.root',input_mc,input_mc,input_mc]
                                                d3['filename'] = 'unfolded_data_'+obs+'_'+str(i)+'_'+mode
                                                d3['unfold_file'] = ['files/'+year+'/cov_mat_'+obs+'_'+str(i)+'.root'],
                                                plots.append(d3)

					plots.append(d)
	return [PlottingJob(plots=plots, args=args)]

def get_fsr_correction(args=None):
	plots = []
	for year in ['16',]:
		for obs in ['abs(genzy)']:
			d = ({
				'files' : ['work/mc16_Spring16_ml.root','work/mc16_origmuonsNLO.root'],
				'folders' : ['genzcuts/ntuple'],
				'nicks' : ['postfsr', 'prefsr'],
				'x_expressions': [obs],
				'labels' : ['factor'],
				'x_errors': [1],
				'title' : 'Simulation',
				'plot_modules' : ['ExportRoot'],
				'file_mode': ('RECREATE'),
				'output_dir' : 'files/'+year+'/',
				'energies' : [13],
				'markers': ['.','_','_','_','_','_','_','_','_','_','_'],	
				'weights' : 'genzmass>81.2&genzmass<101.2',
				'analysis_modules' : ['Divide', 'SumOfHistograms', 'FunctionPlot', 'PrintBinContent'],
				'divide_numerator_nicks' : ['prefsr', 'prefsr'],
				'divide_denominator_nicks' : ['prefsr','postfsr'],
				'divide_result_nicks' : ['one','div'],
				"sum_nicks" : ['div one'],
        	    	        "sum_scale_factors" : ["1 -1"],
        	                "sum_result_nicks" : ['factor'],	
				'nicks_blacklist' : ['div','fsr', 'one'],
				'colors' : ['black'],
				'functions': ['[0]'],
                		'function_fit': ['factor'],
                		'function_parameters': ['0.07'],
                		'function_ranges': ['30,1000'],
                		'function_nicknames': ['fit'],
				"filename" : 'correction_fsr_'+obs,
				'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
			})
			if obs == 'genzpt':
                                d['x_bins'] = [binzpt]
				d['function_ranges'] = ['30,1000']
                        elif obs == 'abs(genzy)':
				d['function_ranges'] = ['0,2.3']
				d['x_expressions'] = 'abs(genzy)'
                                d['x_bins'] = ['23,0,2.3']
                                plots.append(d)
                        elif obs == 'zy':
                                d['x_bins'] = ['46,-2.3,2.3']
                                plots.append(d)
                        elif obs == 'zmass':
                                d['x_bins'] = ['20,81,101']
                                plots.append(d)
                        elif obs == 'genphistareta':
                                d['x_bins'] = [binsphistar],
				d['function_ranges'] = ['0.5,25']
                                d['folders'] = 'genleptoncuts/ntuple'
                                d['weights'] = '(genzpt>5)'
                                plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def pdf_unc(args=None):

	plots = []
	for obs in ['zpt']:
		for year in ['16']:
			d = ({
				'input_modules' : ['InputFastNLO'],
				'fastnlo_files' : ['files/'+theory+'/'+obs+'_27.tab', 'files/'+theory+'/'+obs+'_27.tab','files/'+theory+'/'+obs+'_27.tab','files/'+theory+'/'+obs+'_27.tab'],
				'pdf_sets' : ['NNPDF30_nlo_as_0118','CT14nlo','HERAPDF20_NLO_EIG', 'abm11_5n_nlo'],
				'uncertainty_style' : ['kMCSampling','kHessianCTEQCL68','kHessianAsymmetric','kHessianSymmetric'],
				'uncertainty_type' : ['PDF', 'PDF','PDF','PDF'],
				'fastnlo_nicks' : ['nnpdf','ct14','hera', 'abm'],
				'energies' : [13],
				'markers': ['fill'],
				#'line_widths' : ['1'],
				#'plot_modules' : ['ExportRoot'],
				#'file_mode': ('RECREATE'),
				'lines': [1.0], 
				'labels' : ['NNPDF3.0','CT14','HERAPDF2.0','ABM11'],
				'analysis_modules' : ['Divide','PrintBinContent'],
				'divide_numerator_nicks' : ['nnpdf','ct14','hera','abm'],
                                'divide_denominator_nicks' : ['nnpdf','ct14','hera','abm'],
                                'divide_result_nicks' : ['nnpdf_unc','ct14_unc','hera_unc', 'abm_unc'],
				'divide_tgraphs' : True,
				'nicks_whitelist' : ['unc'],
				"filename" : 'pdf_unc_'+obs,
				#'x_ticks' : [30, 40, 60, 100, 200, 400, 1000],
				'x_log' : True,
				#'www' : 'cross_sections_20'+year,
				'y_label' : "Rel. PDF Uncertainty / %",
				'y_lims' : [0.9,1.10],
				#'y_ticks' : [0.9, 0.95, 1, 1.05, 1.1],
				#'y_tick_labels' : ['-10','-5','0','5','10'],
				'colors' : ['none'],
				'edgecolors' : ['blue','red', 'green', 'purple'],
				'step' : True,
				'hatch' : ['none'],
			})
			if obs == 'zpt':
                                d.update({'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV'})
                                d['x_lims'] = [30,1000]
                                d['x_ticks'] = [30, 40, 60, 100, 200, 400, 1000]
                        elif obs == 'abs(zy)':
                                d.update({'x_label' : r'|$\\mathit{y}_Z$|',
                                })
                                d['x_log'] = False
                        elif obs == 'phistareta':
                                d.update({'x_label' : r'$\\phi^*_\\eta$'})
                                d['x_lims'] = [0.02,10]

			plots.append(d)
        return [PlottingJob(plots=plots, args=args)]


def scale_unc(args=None):

	plots = []
	for obs in ['zpt']:
		for year in ['16']:
			d = ({
				'input_modules' : ['InputFastNLO'],
				'fastnlo_files' : ['files/'+theory+'/'+obs+'_27.tab'],
				'pdf_sets' : 'NNPDF30_nlo_as_0118',
				'uncertainty_style' : ['kAsymmetricSixPoint'],
				'uncertainty_type' : ['Scale'],
				'fastnlo_nicks' : ['nnpdf_scale'],
				'x_errors': [1],
				'energies' : [13],
				'markers': ['fill'],
				#'line_widths' : ['1'],
				'labels' : 'None',
				'analysis_modules' : ['Divide','PrintBinContent'],
				'divide_numerator_nicks' : ['nnpdf_scale'],
                                'divide_denominator_nicks' : ['nnpdf_scale'],
                                'divide_result_nicks' : ['uncertainty'],
				'divide_tgraphs' : True,
				'nicks_whitelist' : ['uncertainty'],
				"filename" : 'scale_unc_'+obs,
				#'x_ticks' : [30, 40, 60, 100, 200, 400, 1000],
				'x_log' : True,
				#'www' : 'cross_sections_20'+year,
				'y_label' : "Rel. Scale Uncertainty / %",
				'y_lims' : [0.9,1.1],
				'y_ticks' : [0.9, 0.95, 1, 1.05, 1.1],
				'y_tick_labels' : ['-10','-5','0','5','10'],
				'colors' : ['none'],
				'edgecolors' : ['blue'],
				#'alphas' : '0.5',
				'step' : True,
				'hatch' : ['none'],
			})
			if obs == 'zpt':
                                d.update({'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV'})
                                d['x_lims'] = [30,1000]
                                d['x_ticks'] = [30, 40, 60, 100, 200, 400, 1000]
                        elif obs == 'abs(zy)':
                                d.update({'x_label' : r'|$\\mathit{y}_Z$|',
                                          'fastnlo_files' : ['files/'+theory+'/abszy.tab','files/'+theory+'/abszy.tab'],
                                })
                                d['x_log'] = False
                        elif obs == 'phistareta':
                                d.update({'x_label' : r'$\\phi^*_\\eta$'})
                                d['x_lims'] = [0.02,10]

			plots.append(d)
        return [PlottingJob(plots=plots, args=args)]



def sys_unc(args=None):
	plots = []
	for obs in ['zpt']:
		for year in ['16']:
			d = ({
				'input_modules' : ['InputRoot','InputFastNLO'],
				'fastnlo_files' : ['files/'+theory+'/'+obs+'_27.tab','files/'+theory+'/'+obs+'_27.tab'],
				'pdf_sets' : 'NNPDF30_nlo_as_0118',
				'uncertainty_style' : ['kHessianAsymmetric','kAsymmetricSixPoint'],
				'uncertainty_type' : ['PDF', 'Scale'],
				'fastnlo_nicks' : ['nnpdf_pdf','nnpdf_scale'],
				'stat_error_nicks' : ['nnpdf_pdf','nnpdf_scale'],
				'stat_error_relative' :True,
                                'stat_error_relative_percent' : True,
				'x_errors': [1],
				'energies' : [13],
				'markers': ['d'],
				'files' : ['files/'+year+'/correction_fsr_'+obs+'.root'],
                                'folders' : '',
                                'nicks' : ['fsr'],
				'y_errors' : False,
                                'x_expressions': ['factor'],
				'to_average_nicks' : ['nnpdf_pdf', 'nnpdf_scale', 'fsr'],
                                'average_result_nick' : 'Total',
                                'averaging_method' : 'rmssum',
				#'line_widths' : ['1'],
				'labels' : ['FSR', 'PDF Unc.', 'Scale Unc.', 'Total'],
				'analysis_modules' : ['ConvertToHistogram','StatisticalErrors', 'AverageHistograms', 'PrintBinContent'],
				'colors' : ['black','red', 'blue', 'yellow'], 
		'lumis':  lumi[year],
                        'energies' : [13],
		"filename" : 'sys_unc_'+obs,
				#'x_ticks' : [30, 40, 60, 100, 200, 400, 1000],
				'x_log' : True,
				#'www' : 'cross_sections_20'+year,
				'y_label' : "Rel. Uncertainty / %",
                                'scale_factors' :['1','1','30'],

			})
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				d['files'] = ['files/'+year+'/correction_fsr_'+obs+'_0.root'],
				d.update({'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV'})
				d['x_lims'] = [30,1000]
				d['x_ticks'] = [30, 40, 60, 100, 200, 400, 1000]
				plots.append(d)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				d.update({'x_label' : r'|$\\mathit{y}_Z$|',
					  'fastnlo_files' : ['files/'+theory+'/abszy.tab','files/'+theory+'/abszy.tab'],
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


def ratio_cross_section_pt(args=None):
	plots = []
	for obs in ['zpt']:
		for year in ['16']:
			d = ({
				'input_modules' : ['InputRoot', 'InputFastNLO'],
				'fastnlo_files' : ['files/'+theory+'/'+obs+'_27.tab','files/'+theory+'/'+obs+'_27.tab'],
				'pdf_sets' : 'CT14nlo',
				'uncertainty_style' : ['kHessianAsymmetricMax','kAsymmetricSixPoint'],
				'uncertainty_type' : ['PDF', 'Scale'],
				'files' : ['files/'+year+'/unfolded_data_'+obs+'_mean.root', 'files/'+year+'/uncertainties_'+obs+'.root', 'files/'+year+'/poisson_uncertainty_'+obs+'.root'],
				'folders' : '',
				'nicks' : ['data', 'sys', 'stat'],
				'x_expressions': ['unfolded','Total', 'error'],
				'y_errors' : True,
				'fastnlo_nicks' : ['nnpdf_pdf','nnpdf_scale'],
				'x_errors': [1],
				'y_lims': [0.8,1.3],
				'lumis':  lumi[year],
				'nicks_whitelist' : ['div'],
				'energies' : [13],
				'lines' : [1],
				'alphas' : [1, 1, 0.5, 1],
				'step' : True,
				'hatch' : ['/', '-','none', 'none'],
				#'line_widths' : ['1'],
				'zorder' : ['div_sys', 'div_nnpdf_pdf','div_nnpdf_scale', 'div_stat'],
				'labels' : ['PDF Unc.', 'Scale Unc.','Syst exp. Unc.', 'Data'],
				'legend' : 'upper right',
				'markers': ['fill','fill','fill', '.'],
				#'x_bins' : [binzpt],
				#'x_lims' : [30,1000],
				'analysis_modules' : ['Errorband', 'Divide', 'PrintBinContent'],
				'errorband_histogram_nicks' : ['data sys sys', 'data stat stat'],
				'errorband_result_nicks' : ['unc_sys', 'unc_stat'],
				'errorband_percentage_error' : True,
				'divide_numerator_nicks' : ['nnpdf_pdf','nnpdf_scale','unc_sys','unc_stat'],
				'divide_denominator_nicks' : ['nnpdf_pdf','nnpdf_scale','nnpdf_pdf','nnpdf_pdf'],
				'divide_result_nicks' : ['div_nnpdf_pdf','div_nnpdf_scale','div_sys', 'div_stat'],
				"divide_tgraphs" : [True, True, True, False],
				'y_label' : 'Ratio to NNPDF30',
				'edgecolors' : ['red','blue', 'lime', 'black'],
				'colors' : ['red', 'blue', 'lime', 'black'], 
				"filename" : 'ratio_pt_'+obs,
				'x_log' : True,		
				#'x_ticks' : [30, 40, 60, 100, 200, 400, 1000],
				#'www' : 'cross_sections_20'+year,
			})
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				d['files'] = ['files/'+year+'/unfolded_data_'+obs+'_0_mean.root', 'files/'+year+'/uncertainties_'+obs+'.root','files/'+year+'/poisson_uncertainty_'+obs+'_0.root'],
				d.update({'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV'})
				d['x_lims'] = [30,1000]
				d['x_ticks'] = [30, 40, 60, 100, 200, 400, 1000]
				plots.append(d)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				d.update({'x_label' : r'|$\\mathit{y}_Z$|',
					  'fastnlo_files' : ['files/'+theory+'/abszy.tab','files/'+theory+'/abszy.tab'],
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
			'files' : ['files/'+year+'/unfolded_data_zpt_0_mean.root','files/'+theory+'/zpt_NNPDF30_nlo_as_0118.root','files/'+theory+'/zpt_CT14nlo_as_0118.root','files/'+theory+'/zpt_HERAPDF20_NLO_ALPHAS_118.root','files/'+theory+'/zpt_abm11_5n_nlo.root'],
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
			'labels' : ['Data','NNPDF30','CT14','HERAPDF20','ABM11'],
			'x_bins' : [binzpt],
			'analysis_modules' : ['Ratio','PrintBinContent'],
			'ratio_numerator_nicks' : ['data','data','data','data'],
			'ratio_denominator_nicks' : ['nnpdf','ct14','hera','abm'],
			'y_subplot_label' : 'Data/Theory',
			'colors' : ['black', 'red', 'blue', 'green', 'purple','red','blue','green','purple'], 
			"filename" : 'sim_comp_pt',
			#'scale_factors' : '
			#'subplot_legend' : 'upper right',
			'x_log' : True,
			'y_subplot_lims' : [0.80,1.2],
			'y_subplot_ticks' : [0.8, 0.9, 1, 1.1, 1.2],
			'y_log' : True,
			'x_ticks' : [40, 60, 100, 200, 400],
			'x_lims' : [40,400],
			'y_lims' : [0.001, 4],
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
				'files' : ['files/16/unfolded_data_'+obs+'_mean.root','files/'+year+'/signal_'+obs+'_mean.root'],
				'folders' : ['',''],
				'nicks' : ['Unfolded', 'signal'],
				'x_expressions': ['unfolded','signal'],
				#'y_errors' : False,
				'x_errors': [1],
			#'y_lims' : [0.001, 6],
				'markers': ['.', '.'],
				'lumis':  lumi[year],
				'energies' : [13],
				'labels' : ['Unfolded Data', 'Data'],
				'analysis_modules' : ['NormalizeByBinWidth','PrintBinContent', 'Ratio'],
				'histograms_to_normalize_by_binwidth' : 'signal',
				'colors' : ['black', 'red'], 
				"filename" : 'unfolding_comp_'+obs,
				'subplot_legend' : 'upper right',
				'y_subplot_lims' : [0.90,1.10],
				'y_subplot_label' : 'Unf./Data',
				'y_log' : True,
				'scale_factors' :['1',scalefactors_fsr[year]],
				#'www' : 'cross_sections_20'+year,
			})
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				d['x_ticks'] = [30, 40, 60, 100, 200, 400, 1000]
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['filename'] = 'unfolding_comp_'+obs+'_'+str(i)
					d2['files'] = ['files/16/unfolded_data_'+obs+'_'+str(i)+'_mean.root','files/'+year+'/signal_'+obs+'_'+str(i)+'_mean.root'],
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
			'files' : ['files/'+year+'/unfolded_data_abs(zy)_mean.root','files/'+theory+'/abszy.root','files/'+theory+'/abszy.root','files/'+theory+'/abszy_hera_27.root','files/'+theory+'/abszy_abm_27.root'],
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
			'analysis_modules' : ['Ratio','PrintBinContent'],
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

def comp_cross_section_double_diff(args=None):
	plots = []
	for obs, obs2 in zip(['zpt', 'phistareta'], ['zpt', 'phistar']):
		
		d = ({
			'files' : ['files/16/unfolded_data_'+obs+'_1_mean.root','files/16/unfolded_data_'+obs+'_2_mean.root','files/16/unfolded_data_'+obs+'_3_mean.root', 'files/16/unfolded_data_'+obs+'_4_mean.root','files/16/unfolded_data_'+obs+'_5_mean.root','files/16/unfolded_data_'+obs+'_6_mean.root','files/'+theory+'/y0_'+obs2+'_CT14nlo_as_0118.root','files/'+theory+'/y1_'+obs2+'_CT14nlo_as_0118.root','files/'+theory+'/y2_'+obs2+'_CT14nlo_as_0118.root','files/'+theory+'/y3_'+obs2+'_CT14nlo_as_0118.root','files/'+theory+'/y4_'+obs2+'_CT14nlo_as_0118.root','files/'+theory+'/y5_'+obs2+'_CT14nlo_as_0118.root'],
			'folders' : '',
			'nicks' : ['data1', 'data2','data3','data4', 'data5','data6','nnpdf1', 'nnpdf2', 'nnpdf3', 'nnpdf4', 'nnpdf5', 'nnpdf6'],
			'x_expressions': ['unfolded','unfolded','unfolded','unfolded','unfolded','unfolded','0','0','0','0','0','0'],
			#'nicks_whitelist' : ['uncertainties','simunc', 'nnpdf','ct10','ratio'],
			'y_errors' : False,
			'x_errors': [0,0,0,0,0,0,1,1,1,1,1,1],
			'lumis':  lumi['16'],
			'energies' : [13],
			#'zorder' : ['nnpdf','ct14','hera','abm','data'],
			'markers': ['o','d','^','s','*','v','_','_','_','_','_','_','o','d','^','s','*','v'],	
			'legend' : 'None',
			'plot_modules' : ['PlotMplZJet', 'PlotMplLegendTable'],
			#'x_lims' : [30,1000],
			"legend_table_row_headers" : [r"$|y^\\mathrm{Z}|<0.4 \\ (\\cdot 10^{5})$", r"$0.4<|y^\\mathrm{Z}|<0.8 \\ (\\cdot 10^{4})$", r"$0.8<|y^\\mathrm{Z}|<1.2 \\ (\\cdot 10^{3})$",  r"$1.2<|y^\\mathrm{Z}|<1.6 \\ (\\cdot 10^{2})$",r"$1.6<|y^\\mathrm{Z}|<2.0 \\ (\\cdot 10^{1})$",r"$2.0<|y^\\mathrm{Z}|<2.3$"],
			#"legend_table_row_headers" : ['test1', 'test2', 'test3', 'test4'],
			"legend_table_column_headers" : ['Data', 'CT14'],
			'legend_table_invert' : False,
			'analysis_modules' : ['Ratio','PrintBinContent'],
			'ratio_numerator_nicks' : ['data1','data2','data3','data4','data5', 'data6'],
			'ratio_denominator_nicks' : ['nnpdf1','nnpdf2','nnpdf3','nnpdf4','nnpdf5', 'nnpdf6'],
			'y_subplot_label' : 'Data/Theo.',
			'colors' : ['black','red','blue','green','purple', 'cyan','black','red','blue','green','purple', 'cyan','black','red','blue','green','purple', 'cyan'], 
			"filename" : 'sim_comp_'+obs+'_over_y',
			#'scale_factors' : '
			#'subplot_legend' : 'upper right',
			'x_log' : True,
			'y_subplot_lims' : [0.80,1.20],
			'y_subplot_ticks' : [0.8, 0.9, 1, 1.1, 1.2],
			'scale_factors' : [100000, 10000, 1000, 100,10, 1,100000, 10000, 1000,100,10, 1],
			'y_log' : True,
			#'www' : 'cross_sections_20'+year,
		})
		if(obs == 'zpt'):
			d.update({
				'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
				'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}d|y_\\mathrm{Z}|}$ / pb $\\mathrm{GeV}^{-1}$",
				'y_lims' : [0.00001, 600000],
				'x_bins' : [binzpt],	
				'x_ticks' : [40, 60, 100, 200, 400],
				'x_lims' : [40, 400]
			})
		if(obs == 'phistareta'):
                        d.update({
                                'x_label' : r'$\\phi^*_\\eta$',
                                'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta d|y_\\mathrm{Z}|}$ / pb ",
                                'y_lims' : [0.00001, 100000000],
				'x_bins' : [binsphistar],
				'x_ticks' : [0.5, 1, 2, 5, 12, 25],
				'x_lims' : [0.5, 25]	
                        })

		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
	
def comp_cross_section_phistar(args=None):
	plots = []
	for year in years:
		d = ({
			'files' : ['files/'+year+'/unfolded_data_phistareta_0_mean.root','files/'+theory+'/phistar_NNPDF30_nlo_as_0118.root','files/'+theory+'/phistar_CT14nlo_as_0118.root','files/'+theory+'/phistar_HERAPDF20_NLO_ALPHAS_118.root','files/'+theory+'/phistar_abm11_5n_nlo.root'],
			'folders' : ['','', '', '', ''],
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
			'histograms_to_normalize_by_binwidth' : 'data',
			'ratio_numerator_nicks' : ['data','data','data','data'],
			'ratio_denominator_nicks' : ['nnpdf','ct14','hera','abm'],
			'colors' : ['black', 'red', 'blue', 'green', 'purple','red','blue','green','purple'], 
			"filename" : 'sim_comp_phistar',
			'y_subplot_lims' : [0.80,1.20],
			'y_subplot_label' : 'Data/MC',
			'y_lims' : [0.01, 3000],
			#'weights' : ['(leptonSFWeight*leptonTriggerSFWeight)*(zpt>5)', '1', '1', '1', '1'],
			'y_log' : True,
			'x_lims' : [0.5, 25],
			'x_log' : True,
			'legend' : 'lower left',
			'x_ticks' : [0.5, 1, 2, 5, 12, 25],
			#'scale_factors' :[scalefactors_fsr[year],'1'],
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
				'files' : ['files/'+year+'/Trigger_uncertainty_'+obs+'.root','files/'+year+'/ID_uncertainty_'+obs+'.root','files/'+year+'/bkg_uncertainty_'+obs+'.root','files/'+year+'/poisson_uncertainty_'+obs+'.root'],
				'folders' : '',
				'x_expressions': ['reldiffup','reldiffup','relbkg','error'],
				'y_errors' : False,
				'x_errors': [1],
				'markers': ['d'],
				'nicks' : ['Trigger', 'ID', 'Bkg','Poisson'],
				'labels' : ['Trigger Efficiency', 'Reconstruction Efficiency', 'Background','Statistical','Lumi', 'Final State Radiation','Total'],
				'analysis_modules' : ['GetConstant','AverageHistograms', 'PrintBinContent'],
				'nicks_for_binning' : ['ID','ID'],
				'constant' : [2.6, 2.0],
				'constant_nicks' : ['Lumi','FSR'],
				'to_average_nicks' : ['Trigger', 'ID', 'Bkg','Poisson', 'Lumi', 'FSR'],
				'average_result_nick' : 'Total',
				'averaging_method' : 'rmssum',
				#'output_dir' : 'files/'+year+'/',
				"filename" : 'uncertainties_'+obs,
				'y_lims' : [0,13],
				'lumis':  lumi[year],
	                        'energies' : [13],
				'y_label' : "Rel. Uncertainty / %",
				'scale_factors' :['100','100','50','1'],
			
			})
			if export:
				d['plot_modules'] = ['ExportRoot']
				d['file_mode']= ('RECREATE')
				d['output_dir'] = 'files/'+year+'/'
				d['to_average_nicks'] = ['Trigger', 'ID', 'Lumi', 'Bkg', 'FSR'] #Remove Stat Uncertainty and take it separately 
			#else: 	
				#d['www'] = 'cross_sections_20'+year
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				d['x_ticks'] = [30, 40, 60, 100, 200, 400, 1000],
				d['x_log'] = True,
				d['x_lims'] = [30,1000],
				d['x_label'] = r'$\\mathit{p}_{T}^{Z}$ / GeV'
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['files'] = ['files/'+year+'/Trigger_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/ID_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/bkg_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/poisson_uncertainty_'+obs+'_'+str(i)+'.root']
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
				for i in range(len(y_bins)):
                                        d2 = copy.deepcopy(d)
                                        d2['files'] = ['files/'+year+'/Trigger_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/ID_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/bkg_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/poisson_uncertainty_'+obs+'_'+str(i)+'.root']
                                        d2["filename"] = 'uncertainties_'+obs if i == 0 else 'uncertainties_'+obs+'_'+str(i)
                                        plots.append(d2)
				plots.append(d)
			
	return [PlottingJob(plots=plots, args=args)]

def get_rootfiles(args=None):
	plotting_jobs = []
	plotting_jobs += get_signal(args)
	plotting_jobs += get_bkg_uncertainty(args)
	plotting_jobs += unfold(args)
#	plotting_jobs += get_fsr_correction(args)
	plotting_jobs += get_IDTrigger_uncertainties(args)
	plotting_jobs += get_unfold_uncertainty(args)
	plotting_jobs += plot_uncertainties(args,export=True)
	return(plotting_jobs)

def compare_datapdf(args=None):
	plotting_jobs = []
	plotting_jobs += comp_cross_section_pt(args)
	#plotting_jobs += ratio_cross_section_pt(args)
	plotting_jobs += comp_cross_section_y(args)
	#plotting_jobs += comp_sim_pt(args)
	plotting_jobs += plot_uncertainties(args,export=False)
	plotting_jobs += comp_cross_section_pt_over_y(args)
	plotting_jobs += comp_cross_section_phistar(args)
	plotting_jobs += comp_unfolding(args)
	return(plotting_jobs)


def simple_plot(args=None):
	plots = []
	d = ({
		'files' : ['plots/signal_zmass.root','work/mc15_ PhiStarEta.root'],
		'folders' : ['','zcuts/ntuple'],
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
		'files' : ['work/mc16_addstatus.root','work/mc16_addstatus.root'],
		'zjetfolders' : ['genleptoncuts','genleptoncuts'],
		'algorithms' : [''],
		'corrections' : [''],
		'cutlabel' : True,
		'markers': ['.','_'],
		#'x_log' : True,
		'title' : 'Simulation',
		#'labels' : ['Pre FSR', 'After FSR'],
		'labels' : ['Reco+Gen Cuts', 'Gen Cuts'],
		#'weights' : ['validgenzfound>0.5','genzfound>0.5'],
		'plot_modules' : ['PlotMplZJet', 'PlotMplRectangle'],
		'rectangle_x' : [71,81.2,101.2,111],
		'rectangle_alpha' : [0.2],
		'rectangle_color' : ["red"],
		#'subplot_legend': 'upper right',
		#'y_subplot_lims': [0.5, 2],
		'lumis':  lumi['16'],
		'x_errors': [1],
		#'markers': ['_', 'd','d'],
		'weights' : ['leptonSFWeight*(nmuons>1)','1'],
		'texts': [r'$\\mathit{p}_{T}^{\\mu}$ > 27 GeV',r'$\\mathit{|\\eta|}^{\\mu}$ < 2.3'],
		'texts_x': [0.03],
		'texts_y': [0.97,0.92],
		'texts_size': [12],
		'analysis_modules' : [ 'Ratio', 'PrintBinContent'],
		#'markers' : ['bar','d','.','.'],
		'x_label' : r"$m_\\mathrm{genZ}$ / GeV",
		#'x_bins' : ['0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.115 0.130 0.145 0.165 0.190 0.220 0.26 0.310 0.390 0.520 0.7 1.0 1.15 1.5 2.0 2.5 3.25 5 10'],
		#'y_subplot_label' : 'Data/Reco',
		'y_subplot_lims' : [0.75,1.1],
		#'colors': ['skyblue', 'red', 'blue', 'black'],
		#'x_log': True,
		'filename' : 'zmass_stat1_genreco',
		'x_expressions': ['genzmass', 'genzmass'],
		#'x_ticks' : [40, 60, 100, 140, 200, 1000],
		'x_bins' : ['40,71,111'],
		#'x_bins' : ['0 81 101 100000'],
		#'x_bins' : ['1,-1000000,1000000'],
		#"www" : "MC-Studies",
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
'''def matrix(args=None):
	plots = []
	d = ({
		'files' : ['work/mc16_Iso04.root'],
		'zjetfolders' : ['allzcuts'],
		'corrections' : ['L1L2L3'],
		'y_expressions' : ['genzpt'],
		'x_expressions': ['zpt'],
		#'weights' : '',
		'y_bins' : [binzpt],
		'labels' : 'None',
		'x_bins' : [binzpt],
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
	return [PlottingJob(plots=plots, args=args)]'''





