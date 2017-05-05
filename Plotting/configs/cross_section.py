# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files

import argparse
import copy
import math
import os

# TODO to more general location
y_bins = ['0','0.4','0.8','1.2', '1.6', '2.0'] #Z rapidity bins for double differential measurements
observe = ['zpt', 'abs(zy)', 'phistareta'] #Variables to be plotted
years = ['16'] #Datasample for lumi
binzpt = '40 45 50 55 60 70 75 80 90 110 130 150 170 200 250 400' #Binning in zpt
binsphistar = '0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.115 0.130 0.145 0.165 0.190 0.220 0.26 0.310 0.35 0.4 0.45 0.50 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 1.0 1.25 1.5 2 3 4 6 12 25' #Binning in phistar
tickszpt = [40, 60, 100, 200, 400] #Ticks for zpt plots
ticksphistar = [0.4,0.6,1,2,4,10,25] #Ticks for phistar plots
modes = ['mean'] #Modes, currently only the mean value
theory = 'theo_3' #Folder for theory predictions 
fsr_factor = '1.079' #Preliminary FSR assumption, constant factor
lumi = {'15': [2.169127], #Lumi of the Data used
	'16': [12.5], # Run BCD 
	#'16' : [6.138487502] #Run EF
	#'16' : [7.544015569] #Run G
	'16H':[8.746001362] #Run H
	}
scalefactors = {'15': '0.0004610419548178884', #basically 1/Lumi can also include efficiencys if not treaded elsewhere
		'16' : '7.9831e-05', #Run BCD 
		#'16' : '0.00016290657913275652' #Run EF
		#'16' : '0.00013255539982038442' #Run G
		'16H' :	0.00011433796527231776
}

#Input Files:
input_data = "/storage/b/afriedel/Excalibur/data16_ICHEP_tl.root"
input_mc = "/storage/b/afriedel/Excalibur/mc16_Spring16.root"

def get_bkg_uncertainty(args=None):
	"Currently calculates only relative background contribution, factor of the contribution is chosen as uncertainty in plot_uncertainties"
	plots = []

	for obs in observe:
		for year in years:
			d = ({
				'files' : [input_data, '/storage/b/afriedel/Excalibur/data16_ICHEP_bkg_tl.root', '/storage/b/afriedel/Excalibur/mc16_bkg_ZZ_tl.root','/storage/b/afriedel/Excalibur/mc16_bkg_ZW_tl.root','/storage/b/afriedel/Excalibur/mc16_bkg_WW_tl.root','/storage/b/afriedel/Excalibur/mc16_bkg_ttJets_tl.root', '/storage/b/afriedel/Excalibur/mc16_bkg_tW_tbarW_tl.root'],
				'zjetfolders' : 'zcuts',
				'algorithms' : [''],
				'corrections' : '',
				'x_expressions' : obs,
				'nicks' : ['data', 'misid', 'ZZ', 'ZW', 'WW', 'ttJets', 'tW'],
				'legend' : None,
				'nicks_whitelist' : ['bkg'],
				'analysis_modules' : ['SumOfHistograms','Divide','PrintBinContent'],
				'divide_denominator_nicks' : ['data'],
				"divide_numerator_nicks" : ['bkg'],
				"divide_result_nicks" : ['relbkg'],	
				'x_errors': [1],
				'weights' : ['(leptonSFWeight)*(leptonTriggerSFWeight)'],
				'markers': 'd',
				'lumis': lumi[year],
				'y_subplot_label' : 'Bkg/Data', 
				'y_subplot_lims': [0, 0.1],
				"sum_nicks" : ['misid ZZ ZW WW ttJets tW'],
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
	"Get uncertainties for ID and Trigger. For this purpose, input data needs different pipelines for mean value and variations up/down variations (here upwards variation is higher, check this for other IDs"
	plots = []
	for sf in ['ID', 'Trigger']:
		for obs in observe:
			for year in years:		
				d = ({
					'files' : [input_data],
					'folders' : ['leptoncuts_mean/ntuple','leptoncuts_'+sf+'up/ntuple'],
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
					'x_lims' : [40,400],
					'plot_modules': ['ExportRoot'],
					'file_mode': ('RECREATE'),
					'analysis_modules' : ['SumOfHistograms','Divide','PrintBinContent'],
					'output_dir' : 'files/'+year+'/',
					"filename" : sf+'_uncertainty_'+obs,
					'x_log' : True,
					'y_label' : "Rel. Uncertainty / %",
				})	
				if obs == 'zpt':
					d['x_bins'] = [binzpt]
					for i in range(len(y_bins)):
						d2 = copy.deepcopy(d)
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
					d['folders'] = ['leptoncuts_mean/ntuple','leptoncuts_'+sf+'up/ntuple'],
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

def get_unfold_uncertainty(args=None):
	"Statistical uncertainty on the unfolded data, deviates from the one of the input data and is calculated in the unfolding module"
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
                                        d3['filename'] = 'poisson_uncertainty_'+obs+'_'+str(i)
					d3[ 'files'] = ['files/16/unfolded_data_'+obs+'_'+str(i)+'_mean.root']
                                        plots.append(d3)

	return [PlottingJob(plots=plots, args=args)]

def print_results(args=None):
	"Write cross section and uncertainties in a .txt file optimised to input in xFitter"
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
				'scale_factors' :[fsr_factor,'1','50','100','100'],
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
	"Subtract the background from the input data"
	plots = []
	for obs in observe:
		for year in years:
			for mode in modes:
				d = ({
					'files' : [input_data, '/storage/b/afriedel/Excalibur/data16_ICHEP_bkg_tl.root','/storage/b/afriedel/Excalibur/mc16_bkg_ZZ_tl.root','/storage/b/afriedel/Excalibur/mc16_bkg_ZW_tl.root','/storage/b/afriedel/Excalibur/mc16_bkg_WW_tl.root','/storage/b/afriedel/Excalibur/mc16_bkg_ttJets_tl.root', '/storage/b/afriedel/Excalibur/mc16_bkg_tW_tbarW_tl.root'],
					'folders' : 'zcuts/ntuple',
					'x_expressions': obs,
					'weights' : ['(leptonSFWeight)*(leptonTriggerSFWeight)'],
					'nicks' : ['data', 'misid', 'ZZ', 'ZW', 'WW', 'ttJets', 'tW'],
					'nicks_blacklist' : ['bkg'],
					'analysis_modules' : ['SumOfHistograms','PrintBinContent'],
					'lumis': lumi[year],
					"sum_nicks" : ['data misid ZZ ZW WW ttJets tW','misid ZZ ZW WW ttJets tW'],
					"sum_scale_factors" : ["1 -1 -1 -1 -1 -1 -1","1 1 1 1 1 1"],
					"sum_result_nicks" : ['signal','bkg'],
					'plot_modules': ['ExportRoot'],
					'file_mode': ('RECREATE'),
					'output_dir' : 'files/'+year+'/',
					'filename' : 'signal_'+obs+'_'+mode,
				})
				if obs == 'zpt':
					d['folders'] = 'leptoncuts/ntuple'
					d['x_bins'] = ['30 35 '+binzpt+ ' 1000']
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
					d['x_bins'] = [binsphistar+' 100'],
					d['folders'] = 'leptoncuts/ntuple'
					for i in range(len(y_bins)):
                                                d3 = copy.deepcopy(d)
                                                d3['weights'] =  '(leptonSFWeight*leptonTriggerSFWeight)*('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+'&zpt>5)' if i is not 0 else '(leptonSFWeight*leptonTriggerSFWeight)*(zpt>5)'
                                                d3['filename'] = 'signal_'+obs+'_'+str(i)+'_'+mode
                                                plots.append(d3)
	return [PlottingJob(plots=plots, args=args)]

def unfold(args=None):
	"Do the unfolding of the input data using the input MC. See the unfold analysis module for mor information"
	plots = []
	for obs in observe:
		for year in years:
			for mode in ['mean']:
				d = ({
					'files' : ['files/'+year+'/signal_'+obs+'_'+mode+'.root',input_mc,input_mc,input_mc],
					'folders' : ['' ,'leptoncuts/ntuple','genleptoncuts/ntuple','allleptoncuts/ntuple'],
					'analysis_modules': ['Unfolding','NormalizeByBinWidth', 'PrintBinContent'],
					'plot_modules' : ['ExportRoot'],
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
					'libRooUnfold': os.environ['EXCALIBURPATH']+'/RooUnfold/libRooUnfold.so',
					'labels' : 'None',
					'unfolding_method' : 'dagostini',
					'unfolding_iterations' : 4,
					'x_log' : True,
					'y_log' : True,
					'z_lims' : [1,1e5],
					'y_errors' : True,
					'nicks' : ['data','mc_reco', 'mc_gen','responsematrix'],
					'output_dir' : 'files/16/',
					'filename' : 'unfolded_data_'+obs+'_'+mode,
					'scale_factors' : [scalefactors[year], scalefactors[year], scalefactors[year], scalefactors[year]],
				})
				if obs == 'zpt':
					d['x_bins'] = ['30 35 '+binzpt+' 1000']
					d['y_expressions'] = [None,None,None,'genzpt'],
			    		d['x_expressions'] = ['signal', 'zpt','genzpt', 'zpt'],
			    		d['y_bins'] = [None, None,None, '30 35 '+binzpt+' 1000'],
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
					d['x_bins'] =  [binsphistar+' 100'],
					d['y_expressions'] = [None,None,None,'genphistareta'],
			    		d['x_expressions'] = ['signal', 'phistareta','genphistareta', 'phistareta'],
			    		d['y_bins'] = [None, None,None,binsphistar+' 100'],
					d['folders'] = ['' ,'leptoncuts/ntuple','genleptoncuts/ntuple','allleptoncuts/ntuple'],
					for i in range(len(y_bins)):
                                                d3 = copy.deepcopy(d)
                                                if i != 0:
                                                        d3['weights'] = ['1', '('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+'&zpt>5)*(leptonSFWeight)','('+y_bins[i-1]+'<abs(genzy)&abs(genzy)<'+y_bins[i]+'&genzpt>5)','('+y_bins[i-1]+'<abs(zy)&abs(zy)<'+y_bins[i]+'&'+y_bins[i-1]+'<abs(genzy)&abs(genzy)<'+y_bins[i]+'&zpt>5&genzpt>5)']
                                                d3['files'] = ['files/16/signal_'+obs+'_'+str(i)+'_'+mode+'.root',input_mc,input_mc,input_mc]
                                                d3['filename'] = 'unfolded_data_'+obs+'_'+str(i)+'_'+mode
                                                d3['unfold_file'] = ['files/'+year+'/cov_mat_'+obs+'_'+str(i)+'.root'],
                                                plots.append(d3)

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
	"Calculate uncertainties on the PDFs with the prescribed methods of the sets (https://github.com/hep-mirrors/h1fitter/blob/master/FastNLO/include/fastnlotk/fastNLOConstants.h)"
	plots = []
	for obs in ['phistar']:
		for year in ['16']:
			d = ({
				'input_modules' : ['InputFastNLO'],
				'fastnlo_files' : ['files/'+theory+'/'+obs+'.tab', 'files/'+theory+'/'+obs+'.tab','files/'+theory+'/'+obs+'.tab'],
				'pdf_sets' : ['NNPDF30_nlo_as_0118','CT14nlo', 'abm11_5n_nlo'],
				'uncertainty_style' : ['kMCSampling','kHessianCTEQCL68','kHessianSymmetric'],
				'uncertainty_type' : ['PDF', 'PDF','PDF'],
				'fastnlo_nicks' : ['nnpdf','ct14', 'abm'],
				'energies' : [13],
				'markers': [' '],
				'y_errors' : False,
				'lines': [1.0], 
				'labels' : ['NNPDF3.0','CT14','ABM11'],
				'line_widths' : ['2.5'],
				'line_styles': ['--', '-','-.'],
				'analysis_modules' : ['SplitGraphComponents','Divide', 'PrintBinContent'],
				'split_graph_nicks' : ['nnpdf','ct14', 'abm'],
				'divide_numerator_nicks' : ['nnpdf_yehigh','ct14_yehigh','abm_yehigh','nnpdf_yelow','ct14_yelow','abm_yelow'],
                                'divide_denominator_nicks' : ['nnpdf','ct14','abm', 'nnpdf','ct14','abm'],
                                'divide_result_nicks' : ['nnpdf_unc_up','ct14_unc_up', 'abm_unc_up', 'nnpdf_unc_down','ct14_unc_down', 'abm_unc_down'],
				'nicks_whitelist' : ['unc'],
				"filename" : 'pdf_unc_'+obs,
				'x_log' : True,
				'y_label' : "Rel. PDF Uncertainty / %",
				'y_lims' : [0.95,1.05],
				'y_ticks' : [0.95, 0.975, 1, 1.025, 1.05],
				'colors' : ['blue','red','purple'],
				'step' : True,
			})
			if obs == 'zpt':
                                d.update({'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV'})
                                d['x_lims'] = [40,400]
                                d['x_ticks'] = tickszpt
                        elif obs == 'abs(zy)':
                                d.update({'x_label' : r'|$\\mathit{y}_Z$|',
                                })
                                d['x_log'] = False
                        elif obs == 'phistar':
                                d.update({'x_label' : r'$\\phi^*_\\eta$'})
                                d['x_lims'] = [0.4,25]
				d['x_ticks'] = ticksphistar

			plots.append(d)
        return [PlottingJob(plots=plots, args=args)]
def scale_unc(args=None):
	"Scale uncertainties (Attention: Only works correctly with Hoppet)"
	plots = []
	for obs in ['phistar']:
		for year in ['16']:
			d = ({
				'input_modules' : ['InputFastNLO'],
				'fastnlo_files' : ['files/'+theory+'/'+obs+'.tab'],
				'pdf_sets' : 'NNPDF30_nlo_as_0118',
				'uncertainty_style' : ['kAsymmetricSixPoint'],
				'uncertainty_type' : ['Scale'],
				'fastnlo_nicks' : ['nnpdf_scale'],
				'x_errors': [1],
				'energies' : [13],
				'markers': ['fill'],
				'labels' : 'None',
				'analysis_modules' : ['Divide','PrintBinContent'],
				'divide_numerator_nicks' : ['nnpdf_scale'],
                                'divide_denominator_nicks' : ['nnpdf_scale'],
                                'divide_result_nicks' : ['uncertainty'],
				'divide_tgraphs' : True,
				'nicks_whitelist' : ['uncertainty'],
				"filename" : 'scale_unc_'+obs,
				'x_log' : True,
				'y_label' : "Rel. Scale Uncertainty / %",
				'y_lims' : [0.9,1.1],
				'y_ticks' : [0.9, 0.95, 1, 1.05, 1.1],
				'y_tick_labels' : ['-10','-5','0','5','10'],
				'colors' : ['none'],
				'edgecolors' : ['blue'],
				'step' : True,
				'hatch' : ['none'],
			})
			if obs == 'zpt':
                                d.update({'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV'})
                                d['x_lims'] = [40,400]
                                d['x_ticks'] = tickszpt
                        elif obs == 'abszy':
                                d.update({'x_label' : r'|$\\mathit{y}_Z$|',
                                          'fastnlo_files' : ['files/theo_1/abszy_27.tab'],
                                })
                                d['x_log'] = False
                        elif obs == 'phistar':
                                d.update({'x_label' : r'$\\phi^*_\\eta$'})
                                d['x_lims'] = [0.4,25]
				d['x_ticks'] = ticksphistar

			plots.append(d)
        return [PlottingJob(plots=plots, args=args)]

def ratio_cross_section(args=None):
	"Print data and different theory predictions as well as theory uncertainties as a ratio to CT14 predictions. More than one plot at a time currently not possible due to bug in HOPPET interface"
	plots = []
	for obs in ['zpt']:
		for year in ['16']:
			d = ({
				'input_modules' : ['InputRoot', 'InputFastNLO'],
				'fastnlo_files' : ['files/'+theory+'/'+obs+'.tab','files/'+theory+'/'+obs+'.tab'],
				'pdf_sets' : ['CT14nlo', 'CT14nlo', 'NNPDF30_nlo_as_0118', 'HERAPDF20_NLO_ALPHAS_118', 'abm11_5n_nlo'],
				'uncertainty_style' : ['kHessianCTEQCL68','kAsymmetricSixPoint', None, None, None],
				'uncertainty_type' : ['PDF', 'Scale', None, None, None],
				'files' : ['files/'+year+'/unfolded_data_'+obs+'_mean.root', 'files/'+year+'/uncertainties_'+obs+'.root', 'files/'+year+'/poisson_uncertainty_'+obs+'.root'],
				'folders' : '',
				'nicks' : ['data', 'sys', 'stat'],
				'x_expressions': ['unfolded','Total', 'error'],
				'y_errors' : [True, True, True, True, False, False, False],
				'fastnlo_nicks' : ['ct14_pdf','ct14_scale', 'nnpdf', 'hera', 'abm'],
				'scale_factors' : [fsr_factor, '1', '1'],
				'x_errors': [1],
				'y_lims': [0.6,1.5],
				'lumis':  lumi[year],
				'nicks_whitelist' : ['div'],
				'energies' : [13],
				'lines' : [1],
				'nicks_for_binning' : ['stat'],
                                'constant' : [2.0],
                                'constant_nicks' : ['FSR'],
				'to_average_nicks' : ['stat', 'FSR'],
                                'average_result_nick' : 'uncor',
                                'averaging_method' : 'rmssum',
				'alphas' : [1,0.4,1, 1, 1, 1, 1],
				'step' : True,
				'hatch' : [None, None,'/', '|',None,None,None],
				'zorder' : [9,1,2,3,4,5,6],
				'labels' : ['Data', 'Syst. Exp. Unc.','CT14 PDF Unc.', 'Scale Unc.', 'NNPDF 3.0', 'HERAPDF 2.0', 'ABM11','Syst exp. Unc.'],
				'legend' : 'upper left',
				'markers': ['.', 'fill', 'fill','fill','.', '.', '.'],
				'analysis_modules' : ['GetConstant','AverageHistograms','Errorband','PrintBinContent','Divide'],
				'errorband_histogram_nicks' : ['data sys sys', 'data uncor uncor'],
				'errorband_result_nicks' : ['unc_sys', 'unc_stat'],
				'errorband_percentage_error' : True,
				'divide_numerator_nicks' : ['unc_stat','unc_sys','ct14_pdf','ct14_scale', 'nnpdf', 'hera', 'abm'],
				'divide_denominator_nicks' : ['ct14_pdf','ct14_pdf','ct14_pdf','ct14_pdf','ct14_pdf','ct14_pdf','ct14_pdf'],
				'divide_result_nicks' : ['div_stat', 'div_sys','div_ct14_pdf','div_ct14_scale', 'div_nnpdf', 'div_hera', 'div_abm'],
				"divide_tgraphs" : [False, True, True, True, False, False, False],
				'y_label' : 'Ratio to CT14',
				#'edgecolors' : ['black', 'gold','red','steelblue', 'blue', 'green', 'purple'],
				'colors' : ['black', 'gold', 'red', 'steelblue', 'blue', 'green', 'purple'], 
				"filename" : 'ratio_'+obs,
				'x_log' : True,		
			})
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				d['x_lims'] = [40,400]
                                d['x_ticks'] = tickszpt
				d.update({'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV'})
				for i in [1]:
					d2 = copy.deepcopy(d)
				 	d2['texts'] = [y_bins[i-1]+r' $\\leq$ |$\\mathit{y}^Z$| < '+y_bins[i]] if i != 0 else ['']
                                        d2['texts_x'] = [0.75]
                                        d2['texts_y'] = [0.97]
					if(i == 0):
						d2['files'] = ['files/'+year+'/unfolded_data_'+obs+'_'+str(i)+'_mean.root', 'files/'+year+'/uncertainties_'+obs+'.root','files/'+year+'/poisson_uncertainty_'+obs+'_0.root'],
						d2['fastnlo_files'] = ['files/'+theory+'/'+obs+'.tab','files/'+theory+'/'+obs+'.tab', 'files/'+theory+'/'+obs+'.tab','files/'+theory+'/'+obs+'.tab','files/'+theory+'/'+obs+'.tab']
					else:
						d2['files'] = ['files/'+year+'/unfolded_data_'+obs+'_'+str(i)+'_mean.root', 'files/'+year+'/uncertainties_'+obs+'_'+str(i)+'.root','files/'+year+'/poisson_uncertainty_'+obs+'_'+str(i)+'.root'],
                                                d2['fastnlo_files'] = ['files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab','files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab','files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab','files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab','files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab']
						d2["filename"] = 'ratio_pt_'+obs+'_'+str(i)
					plots.append(d2)
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
			elif obs == 'phistar':
				d['x_bins'] = [binsphistar],
				d.update({'x_label' : r'$\\phi^*_\\eta$'})
				d['x_lims'] = [0.4,25]
				d['x_ticks'] = ticksphistar
				for i in [1]:
                                        d2 = copy.deepcopy(d)
                                        d2['texts'] = [y_bins[i-1]+r' $\\leq$ |$\\mathit{y}^Z$| < '+y_bins[i]] if i != 0 else ['']
                                        d2['texts_x'] = [0.75]
                                        d2['texts_y'] = [0.97]
                                        if(i == 0):
                                                d2['files'] = ['files/'+year+'/unfolded_data_phistareta_'+str(i)+'_mean.root', 'files/'+year+'/uncertainties_phistareta.root','files/'+year+'/poisson_uncertainty_phistareta_0.root'],
                                                d2['fastnlo_files'] = ['files/'+theory+'/'+obs+'.tab','files/'+theory+'/'+obs+'.tab', 'files/'+theory+'/'+obs+'.tab','files/'+theory+'/'+obs+'.tab','files/'+theory+'/'+obs+'.tab']
                                        else:
                                                d2['files'] = ['files/'+year+'/unfolded_data_phistareta_'+str(i)+'_mean.root', 'files/'+year+'/uncertainties_phistareta_'+str(i)+'.root','files/'+year+'/poisson_uncertainty_phistareta_'+str(i)+'.root'],
                                                d2['fastnlo_files'] = ['files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab','files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab','files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab','files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab','files/'+theory+'/y'+str(i-1)+'_'+obs+'.tab']
                                                d2["filename"] = 'ratio_pt_'+obs+'_'+str(i)
                                        plots.append(d2)
	return [PlottingJob(plots=plots, args=args)]

def comp_cross_section_single_diff(args=None):
	"Prints results for single differential measurements"
	plots = []
	for year in years:
		for obs, obs2 in zip(['zpt', 'phistar'], ['zpt', 'phistareta']):
			d = ({
				'files' : ['files/'+year+'/unfolded_data_'+obs2+'_0_mean.root','files/'+theory+'/'+obs+'_NNPDF30_nlo_as_0118.root','files/'+theory+'/'+obs+'_CT14nlo_as_0118.root','files/'+theory+'/'+obs+'_HERAPDF20_NLO_ALPHAS_118.root','files/'+theory+'/'+obs+'_abm11_5n_nlo.root'],
				'folders' : ['','','','',''],
				'nicks' : ['data', 'nnpdf','ct14','hera','abm'],
				'x_expressions': ['unfolded','0','0','0','0'],
				'y_errors' : False,
				'lumis':  lumi[year],
				'energies' : [13],
				'zorder' : [10,2,3,4,5,6,7,8,9],
				'markers': ['.','2','x','+','3','2','x','+','3'],
				'line_styles' : ['none', '-','-','-','-','-','-','-','-'],
				'step' : True,	
				'labels' : ['Data','NNPDF30','CT14','HERAPDF20','ABM11'],
				'analysis_modules' : ['Ratio','PrintBinContent'],
				'scale_factors': [fsr_factor, '1', '1', '1', '1'],
				'ratio_numerator_nicks' : ['data','data','data','data'],
				'ratio_denominator_nicks' : ['nnpdf','ct14','hera','abm'],
				'y_subplot_label' : 'Data/Theory',
				'colors' : ['black', 'blue', 'red', 'green', 'purple','blue','red','green','purple'], 
				"filename" : 'sim_comp_'+obs2,
				'x_log' : True,
				'y_subplot_lims' : [0.9,1.1],
				'y_subplot_ticks' : [0.9, 0.95, 1,1.05, 1.1],
				'y_log' : True,
			})
			if(obs=='zpt'):	
				d['x_bins'] = [binzpt]
				d['x_ticks'] = tickszpt
                                d['x_lims'] = [40,400]
                                d['y_lims'] = [0.001, 4]
				d['x_label'] = r'$\\mathit{p}_{T}^{Z}$ / GeV'
				d['y_label'] = r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}}$ / pb $\\mathrm{GeV}^{-1}$"
			elif(obs=='phistar'):
				d['x_bins'] = [binsphistar]
                                d['x_ticks'] = ticksphistar
				d['x_lims'] = [0.4,25]
                                d['y_lims'] = [0.01, 1000]
				d['y_label']= r"$\\frac{d\\sigma}{d\\phi^*_\\eta}$ / pb"
				d['x_label'] = r'$\\phi^*_\\eta$'		
			plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
def comp_unfolding_methods(args=None):
	"Compares different methods of unfolding, needs to run unfolding with the desired methods and to change the output filenames accordingly."
	plots = []
	for obs in ['zpt', 'phistareta']:
		for year in years:
			d = ({
				'files' : ['files/16/unfolded_data_'+obs+'_mean.root', 'files/16/unfolded_data_2iter_'+obs+'_mean.root', 'files/16/unfolded_data_6iter_'+obs+'_mean.root''files/16/unfolded_data_matrixinv_'+obs+'_mean.root','files/16/unfolded_data_binbybin_'+obs+'_mean.root'],
				'folders' : [''],
				'nicks' : ['Unfolded','2iter','6iter','matrixinv', 'binbybin'],
				'x_expressions': ['unfolded'],
				'y_errors' : False,
				'y_label' : "Ratio to DAgostini (4 iterations)",
				'x_errors': [1],
				'markers' : ['^', 'o', '*', 'v'],
				'y_lims' : [0.98, 1.03],
				'lumis':  lumi[year],
				'energies' : [13],
				'nicks_whitelist' : ['div'],
				'legend' :'upper left', 
				'labels' : ["DAgostini (2 Iterations)", "DAgostini (6 Iterations)", 'Matrix Inversion', 'Bin by Bin'],
				'analysis_modules' : ['Divide', 'PrintBinContent'],
				'divide_numerator_nicks' : ['2iter','6iter','matrixinv', 'binbybin'],
				'divide_denominator_nicks' : ['Unfolded','Unfolded','Unfolded','Unfolded'],
				'divide_result_nicks' : ['div_2iter','div_6iter','div_matrixinv', 'div_binbybin'],
				"filename" : 'unfolding_comp_'+obs,
			})
			if obs == 'zpt':
				d['x_bins'] = ['30 35 '+binzpt+' 1000']
				d['x_ticks'] = [30, 60, 100, 200, 400, 1000]
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					if (i == 0):
                                                d2['legend'] ='upper right'
					d2['texts'] = [y_bins[i-1]+r' $\\leq$ |$\\mathit{y}^Z$| < '+y_bins[i]] if i != 0 else ['']
                                        d2['texts_x'] = [0.75]
                                        d2['texts_y'] = [0.97]
					d2['files'] = ['files/16/unfolded_data_'+obs+'_'+str(i)+'_mean.root', 'files/16/unfolded_data_2iter_'+obs+'_'+str(i)+'_mean.root', 'files/16/unfolded_data_6iter_'+obs+'_'+str(i)+'_mean.root','files/16/unfolded_data_matrixinv_'+obs+'_'+str(i)+'_mean.root','files/16/unfolded_data_binbybin_'+obs+'_'+str(i)+'_mean.root'],
					d2['filename'] = 'unfolding_methods_comp_'+obs+'_'+str(i)
					d2['x_log'] = True
					d2.update({
						'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
					})
					plots.append(d2)
			elif obs == 'phistareta':
				d['x_ticks'] = [0.3,0.6,1,2,4,10,25, 100]
				d['x_bins'] = ['0.3 0.35 '+binsphistar+' 100'],
				d['x_lims'] = [0.3,100]
				d['x_log'] = True
				d.update({
					'x_label': r'$\\phi^*_\\eta$',
				})
				for i in range(len(y_bins)):
                                        d3 = copy.deepcopy(d)
					if (i == 0):
                                                d3['legend'] ='upper right'
					d3['texts'] = [y_bins[i-1]+r' $\\leq$ |$\\mathit{y}^Z$| < '+y_bins[i]] if i != 0 else ['']
                                        d3['texts_x'] = [0.75]
                                        d3['texts_y'] = [0.97]
                                        d3['filename'] = 'unfolding_methods_comp_'+obs+'_'+str(i)
                                        d3['files'] = ['files/16/unfolded_data_'+obs+'_'+str(i)+'_mean.root', 'files/16/unfolded_data_2iter_'+obs+'_'+str(i)+'_mean.root', 'files/16/unfolded_data_6iter_'+obs+'_'+str(i)+'_mean.root','files/16/unfolded_data_matrixinv_'+obs+'_'+str(i)+'_mean.root','files/16/unfolded_data_binbybin_'+obs+'_'+str(i)+'_mean.root']	
					plots.append(d3)
	return [PlottingJob(plots=plots, args=args)]
def comp_unfolding(args=None):
	"Comparison of data before and after unfolding. To check influence of bins outside phistar, you can change bins to only unfold the observed range"
	plots = []
	for obs in observe:
		for year in years:
			d = ({
				'files' : ['files/16/unfolded_data_'+obs+'_mean.root','files/'+year+'/signal_'+obs+'_mean.root'],
				'folders' : ['',''],
				'nicks' : ['Unfolded', 'signal'],
				'x_expressions': ['unfolded','signal'],
				'x_errors': [1],
				'markers': ['.', '_'],
				'lumis':  lumi[year],
				'energies' : [13],
				'labels' : ['Unfolded Data', 'Data'],
				'analysis_modules' : ['NormalizeByBinWidth','PrintBinContent', 'Ratio'],
				'histograms_to_normalize_by_binwidth' : 'signal',
				'colors' : ['blue', 'red', 'black'], 
				'ratio_denominator_no_errors' : False,
				"filename" : 'unfolding_comp_'+obs,
				'legend' : 'upper right',
				'y_subplot_lims' : [0.80,1.20],
				'y_subplot_ticks' : [0.8, 0.9, 1,1.1, 1.2],
				'y_subplot_label' : 'Unf./Data',
				'y_log' : True,
			})
			if obs == 'zpt':
				d['x_bins'] = ['30 35 '+binzpt+' 1000']
				d['x_ticks'] = [30, 60, 100, 200, 400, 1000]
				d['y_lims'] = [0.1, 1e5]
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					if (i == 0):
                                                d2['legend'] ='upper right'
						d2['y_lims'] = [1, 1e5]
						d2['y_subplot_lims'] = [0.90,1.10],
						d2['y_subplot_ticks'] = [0.9, 0.95, 1, 1.05, 1.1]
					d2['texts'] = [y_bins[i-1]+r' $\\leq$ |$\\mathit{y}^Z$| < '+y_bins[i]] if i != 0 else ['']
                                        d2['texts_x'] = [0.03]
                                        d2['texts_y'] = [0.97]
					d2['filename'] = 'unfolding_comp_'+obs+'_'+str(i)
					d2['files'] = ['files/16/unfolded_data_'+obs+'_'+str(i)+'_mean.root','files/'+year+'/signal_'+obs+'_'+str(i)+'_mean.root'],
					d2['x_log'] = True
					d2.update({
						'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
						'y_label' : 'Events / GeV'
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
				d['x_ticks'] = [0.3,0.6,1,2,4,10,25, 100]
				d['x_bins'] = ['0.3 0.35 '+binsphistar+' 100'],
				d['x_lims'] = [0.3,100]
				d['y_lims'] = [1, 1e7]
				d['x_log'] = True
				d.update({
					'x_label': r'$\\phi^*_\\eta$',
				})
				for i in range(len(y_bins)):
                                        d3 = copy.deepcopy(d)
					if (i == 0):
                                                d3['legend'] ='upper right'
						d3['y_lims'] = [10, 1e7]
						d3['y_subplot_lims'] = [0.90,1.10],
						d3['y_subplot_ticks'] = [0.9, 0.95, 1, 1.05, 1.1]
					d3['texts'] = [y_bins[i-1]+r' $\\leq$ |$\\mathit{y}^Z$| < '+y_bins[i]] if i != 0 else ['']
                                        d3['texts_x'] = [0.03]
                                        d3['texts_y'] = [0.97]
                                        d3['filename'] = 'unfolding_comp_'+obs+'_'+str(i)
                                        d3['files'] = ['files/16/unfolded_data_'+obs+'_'+str(i)+'_mean.root','files/'+year+'/signal_'+obs+'_'+str(i)+'_mean.root'],
                                        plots.append(d3)
	return [PlottingJob(plots=plots, args=args)]

def comp_cross_section_double_diff(args=None):
	"prints double differential cross sections"
	plots = []
	for obs, obs2 in zip(['zpt', 'phistareta'], ['zpt', 'phistar']):
		
		d = ({
			'files' : ['files/16/unfolded_data_'+obs+'_1_mean.root','files/16/unfolded_data_'+obs+'_2_mean.root','files/16/unfolded_data_'+obs+'_3_mean.root', 'files/16/unfolded_data_'+obs+'_4_mean.root','files/16/unfolded_data_'+obs+'_5_mean.root','files/'+theory+'/y0_'+obs2+'_CT14nlo_as_0118.root','files/'+theory+'/y1_'+obs2+'_CT14nlo_as_0118.root','files/'+theory+'/y2_'+obs2+'_CT14nlo_as_0118.root','files/'+theory+'/y3_'+obs2+'_CT14nlo_as_0118.root','files/'+theory+'/y4_'+obs2+'_CT14nlo_as_0118.root'],
			'folders' : '',
			'nicks' : ['data1', 'data2','data3','data4', 'data5','nnpdf1', 'nnpdf2', 'nnpdf3', 'nnpdf4', 'nnpdf5'],
			'x_expressions': ['unfolded','unfolded','unfolded','unfolded','unfolded','0','0','0','0','0'],
			'y_errors' : False,
			'x_errors': [0,0,0,0,0,1,1,1,1,1],
			'lumis':  lumi['16'],
			'energies' : [13],
			'markers': ['o','d','^','s','*','_','_','_','_','_','o','d','^','s','*'],	
			'legend' : 'None',
			#'plot_modules' : ['PlotMplZJet', 'PlotMplLegendTable'],
			#"legend_table_row_headers" : [r"$|y^\\mathrm{Z}|<0.4 \\ (\\cdot 10^{5})$", r"$0.4<|y^\\mathrm{Z}|<0.8 \\ (\\cdot 10^{4})$", r"$0.8<|y^\\mathrm{Z}|<1.2 \\ (\\cdot 10^{3})$",  r"$1.2<|y^\\mathrm{Z}|<1.6 \\ (\\cdot 10^{2})$",r"$1.6<|y^\\mathrm{Z}|<2.0 \\ (\\cdot 10^{1})$",r"$2.0<|y^\\mathrm{Z}|<2.3$"],
			#"legend_table_row_headers" : ['test1', 'test2', 'test3', 'test4'],
			#"legend_table_column_headers" : ['Data', 'CT14'],
			#'legend_table_invert' : False,
			'analysis_modules' : ['Ratio','PrintBinContent'],
			'ratio_numerator_nicks' : ['data1','data2','data3','data4','data5'],
			'ratio_denominator_nicks' : ['nnpdf1','nnpdf2','nnpdf3','nnpdf4','nnpdf5'],
			'y_subplot_label' : 'Data/Theory',
			'colors' : ['black','blue','red','green','purple', 'black','blue','red','green','purple', 'black','red','blue','green','purple'],
			"filename" : 'sim_comp_'+obs+'_over_y',
			'x_log' : True,
			'y_subplot_lims' : [0.60,1.40],
			'y_subplot_ticks' : [0.6, 0.8, 1, 1.2, 1.4],
			'scale_factors' : [fsr_factor+'e4', fsr_factor+'e3', fsr_factor+'e2', fsr_factor+'e1',fsr_factor, 10000, 1000,100,10, 1],
			'y_log' : True,
		})
		if(obs == 'zpt'):
			d.update({
				'x_label' : r'$\\mathit{p}_{T}^{Z}$ / GeV',
				'y_label' : r"$\\frac{d\\sigma}{d\\mathit{p}_{T}^{Z}d|y_\\mathrm{Z}|}$ / pb $\\mathrm{GeV}^{-1}$",
				'y_lims' : [0.00001, 60000],
				'x_bins' : [binzpt],	
				'x_ticks' : tickszpt,
				'x_lims' : [40, 400]
			})
		if(obs == 'phistareta'):
                        d.update({
                                'x_label' : r'$\\phi^*_\\eta$',
                                'y_label' : r"$\\frac{d\\sigma}{d\\phi^*_\\eta d|y_\\mathrm{Z}|}$ / pb ",
                                'y_lims' : [0.00001, 10000000],
				'x_bins' : [binsphistar],
				'x_ticks' : ticksphistar,
				'x_lims' : [0.4, 25]	
                        })

		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
	
def plot_uncertainties(args=None, export=False):
	"Export=true creates root file with uncertainties, for uage in ratio_cross_section. Export=False plots the uncertainties"
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
				'labels' : ['Trigger Efficiency', 'Reconstruction Efficiency', 'Background','Statistical','Luminosity', 'Final State Radiation','Total'],
				'analysis_modules' : ['GetConstant','' 'AverageHistograms', 'PrintBinContent'],
				'nicks_for_binning' : ['ID','ID'],
				'constant' : [2.5, 2.0],
				'constant_nicks' : ['Lumi','FSR'],
				'legend' : 'upper left',
				'formats' : ['png'],
				'to_average_nicks' : ['Trigger', 'ID', 'Bkg','Poisson', 'Lumi', 'FSR'],
				'average_result_nick' : 'Total',
				'markers' : ['.','d','s','^','v','*','o'],
				'averaging_method' : 'rmssum',
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
			if obs == 'zpt':
				d['x_bins'] = [binzpt]
				d['x_ticks'] = tickszpt,
				d['x_log'] = True,
				d['x_lims'] = [40,400],
				d['x_label'] = r'$\\mathit{p}_{T}^{Z}$ / GeV'
				for i in range(len(y_bins)):
					d2 = copy.deepcopy(d)
					d2['files'] = ['files/'+year+'/Trigger_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/ID_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/bkg_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/poisson_uncertainty_'+obs+'_'+str(i)+'.root']
					d2["filename"] = 'uncertainties_'+obs if i == 0 else 'uncertainties_'+obs+'_'+str(i)
					d2['texts'] = [y_bins[i-1]+r' $\\leq$ |$\\mathit{y}^Z$| < '+y_bins[i]] if i != 0 else ['']
                               		d2['texts_x'] = [0.75]
                                	d2['texts_y'] = [0.97]
					plots.append(d2)
			elif obs == 'abs(zy)':
				d['x_bins'] = ['23,0,2.3']
				d['x_label'] = r'|$\\mathit{y}_{Z}$|'
				plots.append(d)
			elif obs == 'phistareta':
				d['x_bins'] = [binsphistar],
				d['x_ticks'] = ticksphistar,
				d.update({'x_label' :  r'$\\phi^*_\\eta$'})
				d['x_log'] = True,
				d['x_lims'] = [0.4,25],
				for i in range(len(y_bins)):
                                        d3 = copy.deepcopy(d)
                                        d3['files'] = ['files/'+year+'/Trigger_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/ID_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/bkg_uncertainty_'+obs+'_'+str(i)+'.root','files/'+year+'/poisson_uncertainty_'+obs+'_'+str(i)+'.root']
                                        d3["filename"] = 'uncertainties_'+obs if i == 0 else 'uncertainties_'+obs+'_'+str(i)
                                        d3['texts'] = [y_bins[i-1]+r' $\\leq$ |$\\mathit{y}^Z$| < '+y_bins[i]] if i != 0 else ['']
                                        d3['texts_x'] = [0.75]
                                        d3['texts_y'] = [0.97]	
					plots.append(d3)
			
	return [PlottingJob(plots=plots, args=args)]

def get_rootfiles(args=None):
	plotting_jobs = []
	plotting_jobs += get_signal(args)
	plotting_jobs += get_bkg_uncertainty(args)
	plotting_jobs += unfold(args)
	plotting_jobs += get_IDTrigger_uncertainties(args)
	plotting_jobs += get_unfold_uncertainty(args)
	plotting_jobs += plot_uncertainties(args,export=True)
	return(plotting_jobs)

def compare_datapdf(args=None):
	plotting_jobs = []
	plotting_jobs += comp_cross_section_single_diff(args)
	#plotting_jobs += ratio_cross_section(args) #Does not work automatically...
	plotting_jobs += plot_uncertainties(args,export=False)
	plotting_jobs += comp_cross_section_double_diff(args)
	plotting_jobs += comp_unfolding(args)
	return(plotting_jobs)







