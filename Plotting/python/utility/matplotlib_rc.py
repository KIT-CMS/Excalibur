# -*- coding: utf-8 -*-

"""
	Some settings for MPL
"""

import copy
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


class MplStyles():
	# Raw style without any settings
	raw = {}

	"""
	# Default settings from Excalibur 1 / CalibFW
	default = {
		# font size
		'font.size': 11,
		'text.fontsize': 11,
		'legend.fontsize': 10,
		'xtick.labelsize': 10,
		'ytick.labelsize': 10,
		'axes.labelsize': 11,
		'lines.markersize': 3,
		'lines.linewidth': 0.4,

		'grid.color': 'gray',
		'grid.linestyle': '-',
		'grid.linewidth': 0.5,
		'image.cmap': 'Blues',

		# linewidth
		'axes.linewidth': 0.4,   # thickness of main box lines
		'axes.formatter.limits': (-3, 3.1),
		# 'patch.linewidth':  1.5:   # thickness of legend pictures and border
		# 'grid.linewidth':   1.3:   # thickness of grid lines
		# 'lines.linewidth':  2.5:   # thickness of error bars
		# 'lines.markersize': 2.5:   # size of markers
		'text.usetex': False,
		'legend.numpoints': 1,
		'legend.fancybox': False,
		'legend.shadow': False,
		'legend.borderpad': 0.3,	# border whitespace in fontsize units
		#legend.markerscale   : 1.0	# the relative size of legend markers vs. original
		'legend.labelspacing': 0.2,	# the vertical space between the legend entries in fraction of fontsize
		#legend.handlelength  : 2.	 # the length of the legend lines in fraction of fontsize
		#legend.handleheight  : 0.7	 # the height of the legend handle in fraction of fontsize
		'legend.handletextpad': 0.4,	# the space between the legend line and legend text in fraction of fontsize
		#legend.borderaxespad : 0.5   # the border between the axes and legend edge in fraction of fontsize
		#legend.columnspacing : 2.	# the border between the axes and legend edge in fraction of fontsize
		#legend.shadow		: False
		#legend.frameon	   : True   # whether or not to draw a frame around legend
		#legend.framealpha	: 1.0	# opacity of of legend frame
		#legend.scatterpoints : 3 # number of scatter points

		'font.family': 'sans-serif',
		'font.serif': ['Computer Modern Roman'],
		'font.sans-serif': ['Computer Modern Sans serif'],
		'font.cursive': ['Computer Modern Roman'],
		'font.monospace': ['Computer Modern Typewriter'],
		'mathtext.sf': 'sans',
		'mathtext.rm': 'sans',
		'figure.dpi': 600,
		'savefig.dpi': 600,
	}
	"""

	poster = copy.deepcopy(raw)
	poster.update({
		'font.size': 75,
	})


def getstyle(style=None):
	styles = MplStyles()
	if not style or not hasattr(styles, style):
		return {}
	else:
		log.debug("Using rc style '{}' with following settings:".format(style))
		log.debug(" "+"\n ".join(["{}: {}".format(key, value) for key, value in getattr(styles, style).iteritems()]))
		return getattr(styles, style)
