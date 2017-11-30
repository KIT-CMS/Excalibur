import Excalibur.Plotting.harryinterface as harryinterface

import time

from copy import deepcopy

CHANNEL_SPEC = {
    'Zmm' : {
        'label': r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"
    },
    'Zee' : {
        'label': r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"
    }
}

ALPHA_UPPER_BIN_EDGES = [0.1, 0.15, 0.2, 0.3, 0.4]

ETA_BIN_EDGES_WIDE = [0, 0.783, 1.305, 1.93,
                      2.5, 2.964, 3.2, 5.191]
ETA_BIN_EDGES_NARROW = [0.000, 0.261, 0.522, 0.783, 1.044, 1.305,
                        1.479, 1.653, 1.930, 2.172, 2.322, 2.500,
                        2.650, 2.853, 2.964, 3.139, 3.489, 3.839,
                        5.191]

class Combination(object):
    """Create a ROOT file containing histograms for specified quantities."""

    _quantity_labels = {
        # just raw number of events -> None
        None: 'RawNEvents',

        # 1D histograms
        'ptbalance': 'PtBal',
        'mpf': 'MPF',
        'rawmpf': 'MPF-notypeI',
        'zmass': 'ZMass',
        'npumean': 'Mu',
        'rho': 'Rho',
        'npv': 'NPV',

        # 2D histograms
        ("npumean", "rho"): "rho_vs_npumean",
        ("npumean", "npv"): "npv_vs_npumean",
    }

    _ZPT_BINNING = "30 40 50 60 85 105 130 175 230 300 400 500 700 1000 1500"

    def __init__(self,
                 sample_data,
                 sample_mc,
                 global_selection,
                 alpha_upper_bin_edges,
                 eta_bin_edges,
                 basename="combination_ZJet",
                 correction_folders=('L1L2L3',),
                 pileup_subtraction_algorithm='CHS'):
        """

        :param sample_data: `jercplot.core.sample.Sample` object containing the data
        :type sample_data: `jercplot.core.sample.Sample` object
        :param sample_mc: `jercplot.core.sample.Sample` object containing the MC
        :type sample_mc: `jercplot.core.sample.Sample` object
        :param global_selection: `jercplot.core.selection.CutSet` object specifying the selection cuts
        :type global_selection: `jercplot.core.selection.CutSet` object
        :param basename: base name of the generated output file (combination file)
        :type basename: str
        :param alpha_upper_bin_edges: list of upper bin edges for the inclusive alpha binning
        :type alpha_upper_bin_edges: list of float
        :param eta_bin_edges: list indicating the eta bin edges (must be given in ascending order!)
        :type eta_bin_edges: list of float
        :param correction_folders: list of ZJet correction levels (e.g. ``['L1L2L3']``)
        :type correction_folders: list of str
        :param pileup_subtraction_algorithm: name of algorithm used for pileup subtraction (e.g. ``'CHS'``) (only used as label)
        :type pileup_subtraction_algorithm: str
        """

        self._sample_data = sample_data
        self._sample_mc = sample_mc

        self._channel = self._sample_data['channel']
        assert self._sample_mc['channel'] == self._channel

        self._basename = basename
        self._correction_folders = correction_folders
        self._pu_algorithm = pileup_subtraction_algorithm
        self._alpha_upper_bin_edges = alpha_upper_bin_edges
        self._eta_bin_edges = eta_bin_edges
        self._selection = global_selection

        self._global_cuts = self._selection.weights_string

        self._alpha_cut_dicts = [
            {
                'cut_string' : '(alpha<{})'.format(_alpha_upper),
                'label_string': 'a' + str(int(100 * _alpha_upper))
            }
            for _alpha_upper in self._alpha_upper_bin_edges
        ]

        self._eta_cut_dicts = [
            {
                'cut_string': "({0}<=abs(jet1eta)&&abs(jet1eta)<{1})".format(_eta_lo, _eta_hi),
                'label_string': "eta_{0:0>2d}_{1:0>2d}".format(int(round(10 * _eta_lo)), int(round(10 * _eta_hi))),
            }
            for (_eta_lo, _eta_hi) in zip(self._eta_bin_edges[:-1], self._eta_bin_edges[1:])
        ]

        # additional eta bins
        self._eta_cut_dicts += [
            # standard ZJet barrel region with jet1eta<1.3
            {
                'cut_string': "(0<=abs(jet1eta)&&abs(jet1eta)<1.3)",
                'label_string': "eta_00_13",
            }
        ]

        _output_filename = "_".join((self._basename,
                                     self._sample_data['channel'],
                                     self._sample_dataself['source_label'],
                                     time.strftime("%Y-%m-%d", time.localtime())))

        self._export_root_merlin_base_dict = {
            'files': [self._sample_data['file'], self._sample_mc['file']],
            'plot_modules': ['ExportRoot'],
            'filename': _output_filename,
            'nicks': ['data', 'mc'],
            'zjetfolders': ['basiccuts'], # TODO: add global zpt cuts
            #'tree_draw_options': ['prof'],  # TODO: remove?
            # ratio
            'analysis_modules': ['Ratio'],
            'ratio_numerator_nicks': ['data'],
            'ratio_denominator_nicks': ['mc'],
            'ratio_denominator_no_errors': False,
        }

        # this gets filled by _prepare()
        self._export_root_merlin_dicts = []

    @staticmethod
    def apply_double_profile(plotDict, args=None):
        """
        Plot <y> vs <x>, i.e. use mean/err for X&Y per X bin

        :param plotDict: the HarryPlotter job information
        :param args: the command line arguments

        :note: This modifies `plotDict` inplace.
        """
        if not 'prof' in plotDict['tree_draw_options'] or 'profs' in plotDict['tree_draw_options']:
            if isinstance(plotDict['tree_draw_options'], basestring):
                plotDict['tree_draw_options'] = [plotDict['tree_draw_options']]
            plotDict['tree_draw_options'].append('prof')
        # Parameter List Expansion
        #   the x vs x profile must be an exakt match of y vs x
        #   we thus must replicate all settings for their position to match
        # settings we need to replicate in a controlled fashion
        input_root_opts = ['nicks', 'x_expressions', 'y_expressions', 'z_expressions', 'x_bins', 'y_bins', 'z_bins',
                           'scale_factors', 'files', 'directories', 'folders', 'weights', 'friend_trees',
                           'tree_draw_options']

        # make sure all n-length (non-0,1) objects have the same size
        opt_n_length_max = max(len(plotDict.get(opt_name, ())) for opt_name in input_root_opts if
                               not isinstance(plotDict.get(opt_name), str))

        assert opt_n_length_max > 0, 'Cannot expand empty plot definition'
        for opt_name in input_root_opts:
            if opt_name not in plotDict or isinstance(plotDict[opt_name], str):
                continue
            assert len(plotDict[opt_name]) <= 1 or len(plotDict[
                                                           opt_name]) == opt_n_length_max, "Replication requires all input_root options to be either of 0, 1 or same max length ('%s' is %d/%d)" % (
            opt_name, len(plotDict[opt_name]), opt_n_length_max)
            # TODO: dunno if checking for None is required, saw this in HP - MF@20151130
            if not plotDict[opt_name] or plotDict[opt_name][0] is None:
                continue
            if len(plotDict[opt_name]) == 1:
                plotDict[opt_name] = plotDict[opt_name] * opt_n_length_max
            # never modify inplace - input may be mutable and used elsewhere/recursively
            plotDict[opt_name] = plotDict[opt_name][:] * 2
        if not plotDict.get('nicks') or plotDict['nicks'][0] is None:
            plotDict['nicks'] = ["nick%d" % nick for nick in xrange(len(plotDict['y_expressions']))]
        # X-Y Profile matching
        # explicitly create new x profiles
        plotDict['y_expressions'] = plotDict['y_expressions'][:opt_n_length_max] + plotDict['x_expressions'][
                                                                                   opt_n_length_max:]
        plotDict['nicks'] = plotDict['nicks'][opt_n_length_max:] + ['%s_x_prof' % nick for nick in
                                                                    plotDict['nicks'][:opt_n_length_max]]
        # create new y vs <x> graphs
        plotDict['analysis_modules'] = plotDict.get('analysis_modules', [])[:]
        plotDict['analysis_modules'].insert(0, 'TGraphFromHistograms')
        plotDict['tgraph_strip_empty'] = 'any'
        plotDict['tgraph_y_nicks'] = plotDict['nicks'][:opt_n_length_max]
        plotDict['tgraph_x_nicks'] = plotDict['nicks'][opt_n_length_max:]
        plotDict['tgraph_result_nicks'] = ['%s_vs_x_prof' % nick for nick in plotDict['nicks'][:opt_n_length_max]]
        # disable source plots
        plotDict['nicks_blacklist'] = [r'^%s$' % nick for nick in plotDict['nicks']]
        return plotDict

    def _prepare(self):
        '''prepare the Merlin dictionaries used for "plotting" to the ROOT file.'''
        for _alpha_cut_dict in self._alpha_cut_dicts:
            for _eta_cut_dict in self._eta_cut_dicts:
                for _corr_folder in self._correction_folders:

                    _plot_dict_alpha_eta_corr = deepcopy(self._export_root_merlin_base_dict)

                    _plot_dict_alpha_eta_corr.update({
                        'corrections': [_corr_folder],
                        'file_mode': 'UPDATE',  # default: update ROOT file instead of recreating it
                        'weights': '&&'.join((
                            self._global_cuts or "1.0",
                            _alpha_cut_dict['cut_string'],
                            _eta_cut_dict['cut_string']
                        )),
                        'x_expressions': ['zpt'],
                        'x_bins': self._ZPT_BINNING,  # custom binning defined in HarryPlotter/Merlin
                        'no_weight': True,  # remove reweights in MC
                    })

                    for _quantity, _quantity_label in self._quantity_labels.iteritems():
                        _plot_label_suffix = '_'.join([_quantity_label,  # TODO: assert key in dict?
                                                       self._pu_algorithm,
                                                       _alpha_cut_dict['label_string'],
                                                       _eta_cut_dict['label_string'],
                                                       _corr_folder])

                        _plot_dict_quantity = deepcopy(_plot_dict_alpha_eta_corr)
                        _plot_dict_quantity['labels'] = ['_'.join([_dmr, _plot_label_suffix]) for _dmr in ['Data', 'MC', 'Ratio']]

                        if isinstance(_quantity, tuple):
                            # 2D histogram
                            _plot_dict_quantity.update({
                                'x_expressions': [_quantity[0]],
                                'x_label': _quantity[0],
                                'x_bins': "25,0.5,25.5", # TODO: make more general (?)
                                'y_expressions': [_quantity[1]],
                                'y_label': _quantity[1],
                                #'cutlabel': True,  # TODO: gives a warning -> check
                                'legend': 'upper left',
                                'tree_draw_options': ['prof'],
                            })
                        elif _quantity is None:
                            pass
                        else:
                            # assume 1D histogram(or `None` for raw event number)
                            _plot_dict_quantity.update({
                                'y_expressions': [_quantity],
                                'y_label': _quantity,
                                'tree_draw_options': ['prof'],
                            })
                            self.apply_double_profile(_plot_dict_quantity)

                        self._export_root_merlin_dicts.append(_plot_dict_quantity)

        # recreate ROOT file on first plot (otherwise: update)
        self._export_root_merlin_dicts[0]['file_mode'] = 'RECREATE'

    def _get_plot_dicts_in_batches_of(self, n_plots_per_batch):
        """generator yielding prepares Merling dictionaries in batches of ``n_plots_per_batch``"""
        _sz = len(self._export_root_merlin_dicts)
        _n_batches = int(_sz//n_plots_per_batch)

        # round number of batches up if not divisible
        if _n_batches * n_plots_per_batch < _sz:
            _n_batches += 1

        for _ibatch in range(_n_batches):
            #print "Yielding slice [{}:{}]".format(_ibatch*n, min((_ibatch + 1)*n, _sz))
            yield self._export_root_merlin_dicts[_ibatch * n_plots_per_batch: min((_ibatch + 1)*n_plots_per_batch, _sz)]

    def run(self, n_plots_per_batch=40, merlin_args=None):
        """Run Merlin for all plot dicts"""
        self._prepare()
        if merlin_args is None:
            merlin_args = []

        _sz = len(self._export_root_merlin_dicts)
        _n_batches = int(_sz//n_plots_per_batch)

        # round number of batches up if not divisible
        if _n_batches * n_plots_per_batch < _sz:
            _n_batches += 1

        print "\nCreating combination file...\n"
        print "Total number of Merlin configs: {}".format(len(self._export_root_merlin_dicts))
        print "Running Merlin in batches of {} configs per run.\n".format(n_plots_per_batch)

        # start plotting in batches of n=10 plots
        for _i_batch, _plot_dict_batch in enumerate(self._get_plot_dicts_in_batches_of(n_plots_per_batch)):
            print "Running Merlin for batch {} of {}...\n".format(_i_batch + 1, _n_batches)
            harryinterface.harry_interface(_plot_dict_batch, merlin_args + ['--max-processes', '1'])