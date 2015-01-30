# -*- coding: utf-8 -*-

"""
"""

import Artus.HarryPlotter.input_modules.inputroot as inputroot

class InputRootZJet(inputroot.InputRoot):

	def modify_argument_parser(self, parser, args):
		super(InputRootZJet, self).modify_argument_parser(parser, args)

		# special arguemnts for custom zjet folder naming conventions
		self.input_options.add_argument("--zjetfolders", type=str, nargs='*', default=None,
		                                help="zjet folders (all, incut....")
		self.input_options.add_argument("--algorithms", type=str, nargs='*', default=None,
		                                help="jet algorithms.")
		self.input_options.add_argument("--corrections", type=str, nargs='*', default=None,
		                                help="correction levels.")


	def prepare_args(self, parser, plotData):
		super(InputRootZJet, self).prepare_args(parser, plotData)
		
		zjetlist =  ["algorithms", "corrections", "zjetfolders"]
		self.prepare_list_args(plotData, zjetlist)
		if all( [plotData.plotdict[i] != None for i in ] zjetlist):
			for algo, corr, folder in ([plotData.plotdict[i] for i in zjetlist]):
				print algo, corr
				#plotData.plotdict['folders'] = 
