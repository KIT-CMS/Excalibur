# -*- coding: utf-8 -*-

"""
"""

import Artus.HarryPlotter.harryparser as harryparser
import Artus.Utility.tools as tools
import Excalibur.Plotting.utility.toolsZJet as toolsZJet

class HarryParserZJet(harryparser.HarryParser):

	def __init__(self, **kwargs):
		super(HarryParserZJet, self).__init__()

		self.set_defaults(plot_modules=["PlotMplZJet"])
		self.set_defaults(input_modules="InputRootZJet")

		self.add_argument('--list-functions', action='store_true', default=False,
			help="Print the available json and python plot functions with comments/documentation")

	def parse_known_args(self, args=None, namespace=None):
		known_args, unknown_args = super(HarryParserZJet, self).parse_known_args(args=args, namespace=namespace)

		if known_args.list_functions:
			toolsZJet.print_jsons_and_functions(
				json_path = tools.get_environment_variable("JSONCONFIGS"),
				python_path = tools.get_environment_variable("PYTHONCONFIGS"),
			)

		return known_args, unknown_args
