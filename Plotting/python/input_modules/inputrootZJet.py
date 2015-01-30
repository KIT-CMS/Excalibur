# -*- coding: utf-8 -*-

"""
"""

import Artus.HarryPlotter.input_modules.inputroot as inputroot

class InputRootZJet(inputroot.InputRoot):

	def modify_argument_parser(self, parser, args):
		super(InputRootZJet, self).modify_argument_parser(parser, args)

		# special arguemnts for custom zjet folder naming conventions
		self.zjet_input_options = parser.add_argument_group("ZJet input options")
		self.zjet_input_options.add_argument("--zjetfolders", type=str, nargs='*', default=None,
		                                help="zjet folders (all, incut....")
		self.zjet_input_options.add_argument("--algorithms", type=str, nargs='*', default=None,
		                                help="jet algorithms.")
		self.zjet_input_options.add_argument("--corrections", type=str, nargs='*', default=None,
		                                help="correction levels.")


	def prepare_args(self, parser, plotData):
		super(InputRootZJet, self).prepare_args(parser, plotData)
		
		# this is needed so one can put together the folder name like in the old
		# merlin plotting
		zjetlist =  ["algorithms", "corrections", "zjetfolders"]
		self.prepare_list_args(plotData, zjetlist)
		if all( [plotData.plotdict[i] != None for i in  zjetlist]):
			folders = []
			for algo, corr, folder in zip([plotData.plotdict[i] for i in zjetlist]):
				folders.append("%s_%s%s" % (folder, algo, corr))
