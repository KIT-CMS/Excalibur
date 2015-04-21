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
		self.set_defaults(input_module="InputRootZJet")

		self.add_argument("plot", type=str, nargs='?', default='zmass',
                          help="""Name of the plot. x-/y-expressions and output filename 
                          are constructed from this, if not explicitly given. 
                          Default is '%(default)s'.""")

		self.add_argument("--debug", action='store_true', help="short for --log-level debug")

		self.add_argument('--list-functions', action='store_true', default=False,
			help="Print the available json and python plot functions with comments/documentation")

	def parse_known_args(self, args=None, namespace=None):
		known_args, unknown_args = super(HarryParserZJet, self).parse_known_args(args=args, namespace=namespace)
		# set debug output
		if known_args.debug == True and known_args.log_level == self.get_default('log_level'):
			known_args.log_level = 'debug'

		if known_args.list_functions:
			toolsZJet.print_jsons_and_functions(
				json_path = tools.get_environment_variable("JSONCONFIGS"),
				python_path = tools.get_environment_variable("PYTHONCONFIGS"),
			)

		return known_args, unknown_args
