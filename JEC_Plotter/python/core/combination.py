import os
import time
import ROOT

from .quantities import BinSpec, QUANTITIES

from array import array
from copy import deepcopy

from Artus.Utility.tfilecontextmanager import TFileContextManager
from Excalibur.Plotting.utility.expressionsZJet import ExpressionsDictZJet
from Artus.HarryPlotter.analysis_modules.tgraphfromhistograms import HistogramGroupIterator

import Excalibur.Plotting.harryinterface as harryinterface



CHANNEL_SPEC = {
    'Zmm' : {
        'label': r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"
    },
    'Zee' : {
        'label': r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"
    }
}

ALPHA_UPPER_BIN_EDGES = [0.1, 0.15, 0.2, 0.3, 0.4]

ETA_BIN_EDGES_BARREL = [0, 1.3]
ETA_BIN_EDGES_WIDE = [0, 0.783, 1.305, 1.93,
                      2.5, 2.964, 3.2, 5.191]
ETA_BIN_EDGES_NARROW = [0.000, 0.261, 0.522, 0.783, 1.044, 1.305,
                        1.479, 1.653, 1.930, 2.172, 2.322, 2.500,
                        2.650, 2.853, 2.964, 3.139, 3.489, 3.839,
                        5.191]

class CombinationDirect(object):
    """Create a ROOT file containing histograms for specified quantities.

    This class uses ROOT directly for creating the output.
    """
    _expr_dict_zjet = ExpressionsDictZJet()

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

    def __init__(self,
                 sample_data,
                 sample_mc,
                 global_selection,
                 alpha_upper_bin_edges,
                 eta_binnings,
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
        :param eta_binnings: a list of lists indicating the eta bin edges (each list must be given in ascending order!)
        :type eta_binnings: list of float
        :param correction_folders: list of ZJet correction levels (e.g. ``['L1L2L3']``)
        :type correction_folders: list of str
        :param pileup_subtraction_algorithm: name of algorithm used for pileup subtraction (e.g. ``'CHS'``) (only used as label)
        :type pileup_subtraction_algorithm: str
        :param inclusive_eta_bin: whether to include plots for the entire eta range in addition to the sub-bins.
        :type inclusive_eta_bin: bool
        """

        self._sample_data = sample_data
        self._sample_mc = sample_mc

        self._channel = self._sample_data['channel']
        assert self._sample_mc['channel'] == self._channel

        self._basename = basename
        self._correction_folders = correction_folders
        self._pu_algorithm = pileup_subtraction_algorithm
        self._alpha_upper_bin_edges = alpha_upper_bin_edges
        self._eta_binnings = eta_binnings
        self._selection = global_selection

        # check that the eta binning specification is correct
        try:
            # first two levels must be iterable
            iter(self._eta_binnings)
            iter(self._eta_binnings[0])
        except ValueError:
            raise ValueError("'eta_binnings' must be a list of lists of bin edges!")

        self._global_cuts = self._selection.weights_string if self._selection is not None else None

        self._alpha_cut_dicts = [
            {
                'cut_string' : '(alpha<{})'.format(_alpha_upper),
                'label_string': 'a' + str(int(100 * _alpha_upper))
            }
            for _alpha_upper in self._alpha_upper_bin_edges
        ]

        self._eta_cut_dicts = []
        for _eta_bin_edges in self._eta_binnings:
            self._eta_cut_dicts += [
                {
                    'eta_hi': _eta_hi,  # only used for display
                    'eta_lo': _eta_lo,  # only used for display
                    'cut_string': "({0}<=abs(jet1eta)&&abs(jet1eta)<{1})".format(_eta_lo, _eta_hi),
                    'label_string': "eta_{0:0>2d}_{1:0>2d}".format(int(round(10 * _eta_lo)), int(round(10 * _eta_hi))),
                }
                for (_eta_lo, _eta_hi) in zip(_eta_bin_edges[:-1], _eta_bin_edges[1:])
            ]

        self._output_filename = "_".join((self._basename,
                                     self._sample_data['channel'],
                                     self._sample_data['source_label'],
                                     time.strftime("%Y-%m-%d", time.localtime()))) + ".root"

    def _prepare(self):
        '''prepare the Merlin dictionaries used for "plotting" to the ROOT file.'''
        self._comb_dicts = []
        for _alpha_cut_dict in self._alpha_cut_dicts:
            for _eta_cut_dict in self._eta_cut_dicts:
                    for _quantity, _quantity_label in self._quantity_labels.iteritems():

                        _configuration_label = '_'.join([_quantity_label,  # TODO: assert key in dict?
                                                         self._pu_algorithm,
                                                         _alpha_cut_dict['label_string'],
                                                         _eta_cut_dict['label_string']])

                        self._comb_dicts.append(
                            dict(
                                configuration_label=_configuration_label,

                                x_expression='zpt',
                                x_label='zpt',
                                x_bins=QUANTITIES['zpt'].bin_spec,

                                weights='&&'.join((
                                    self._global_cuts or "1.0",
                                    _alpha_cut_dict['cut_string'],
                                    _eta_cut_dict['cut_string']
                                )),
                            )
                        )

                        if isinstance(_quantity, tuple):
                            # 2D histogram
                            self._comb_dicts[-1].update(
                                dict(
                                    x_expression=_quantity[0],
                                    x_label=_quantity[0],
                                    # TODO: make more general (?)
                                    x_bins=BinSpec.make_equidistant(25, (0.5, 25.5)),

                                    y_expression=_quantity[1],
                                    y_label=_quantity[1],
                                )
                            )
                        elif _quantity is None:
                            pass
                        else:
                            # assume 1D histogram (or `None` for raw event number)
                            self._comb_dicts[-1].update(
                                dict(
                                    y_expression=_quantity,
                                    y_label=_quantity,
                                )
                            )

    @staticmethod
    def _create_root_histogram(name, root_object_class_name, x_bin_spec, y_bin_spec=None):

        _root_obj_class = getattr(ROOT, root_object_class_name)
        _root_obj_args = [name, name, x_bin_spec.n_bins, array("d", x_bin_spec.bin_edges)]

        if y_bin_spec is not None:
            _root_obj_args.extend([y_bin_spec.n_bins, array("d", y_bin_spec.bin_edges)])

        #if 'Profile' in root_object_class_name:
        #    _root_obj_args.append('')
        #print "Calling ctor for '{}' with args: {}".format(root_object_class_name, _root_obj_args)
        _root_obj = _root_obj_class(*_root_obj_args)
        #print "Returning ROOT object:", _root_obj

        return _root_obj


    @staticmethod
    def _profile_to_tgrapherrors(tge_label, profile_x, profile_y):
        _histo_iter = HistogramGroupIterator(
            histograms=(profile_x, profile_y),
            skip=HistogramGroupIterator.SKIP_ANY
        )
        _tge = ROOT.TGraphErrors()
        for _i, _bincont in enumerate(_histo_iter):
            (_xm, _xe), (_ym, _ye) = _bincont
            _tge.SetPoint(_i, _xm, _ym)
            _tge.SetPointError(_i, _xe, _ye)
        _tge.SetName(tge_label)
        _tge.SetTitle(tge_label)
        return _tge


    def run(self, require_confirmation=True):
        """Create the combination file from the plot dicts"""

        self._prepare()

        _root_file_data = ROOT.TFile(self._sample_data['file'])
        _root_file_mc = ROOT.TFile(self._sample_mc['file'])

        _zjet_folder = self._selection.zjet_folder

        print "\nCreating combination file...\n"
        print "Using data sample at: {}".format(self._sample_data['file'])
        print "Using MC sample at: {}".format(self._sample_mc['file'])
        print "Using cut folder: {}".format(_zjet_folder)
        print "Using global weight string: '{}'".format(self._global_cuts)
        print "\nAlpha upper bin edges: {}".format(self._alpha_upper_bin_edges)
        print "Eta binnings:"
        for _ecd in self._eta_cut_dicts:
            print "{} -> eta in [{}, {}]".format(_ecd['label_string'], _ecd['eta_lo'], _ecd['eta_hi'])
        print "\nCorrection levels: {}".format(self._correction_folders)
        print "\nTotal number of objects: "
        print "    3 (data, mc, ratio)"
        print "  * {} (no. of requested output quantities)".format(len(self._quantity_labels.keys()))
        print "  * {} (alpha bins)".format(len(self._alpha_cut_dicts))
        print "  * {} (eta bins)".format(len(self._eta_cut_dicts))
        print "  * {} (correction levels)".format(len(self._correction_folders))
        print "-------------------------------"
        print "  = {}".format(3 * len(self._comb_dicts) * len(self._correction_folders))

        print "\nOutput file name: {}".format(self._output_filename)

        if os.path.exists(self._output_filename):
            raise IOError("File '{}' exists: will not overwrite!")

        if require_confirmation:
            _answer = ''
            while _answer.lower() not in ('y', 'yes', 'no', 'n'):
                if _answer:
                    print "Please answer 'yes'/'y' or 'no'/'n':"
                _answer = raw_input("Is this correct? [yes/no] >")

            if _answer in ('no', 'n'):
                print "Aborted by user."
                exit(1)

        _root_file_output = ROOT.TFile(self._output_filename, "RECREATE")

        for _corr_folder in self._correction_folders:
            print "Processing correction level '{}'...".format(_corr_folder)

            _root_ntuple_data = _root_file_data.Get("{}_{}/ntuple".format(_zjet_folder, _corr_folder))

            # no residuals in MC -> use L1L2L3 instead
            if _corr_folder == "L1L2L3Res":
                _root_ntuple_mc = _root_file_mc.Get("{}_{}/ntuple".format(_zjet_folder, "L1L2L3"))
            else:
                _root_ntuple_mc = _root_file_mc.Get("{}_{}/ntuple".format(_zjet_folder, _corr_folder))

            for _pd in self._comb_dicts:

                _plot_label = "{}_{}".format(_pd['configuration_label'], _corr_folder)

                print "\tProcessing '{}'...".format(_plot_label)
                _weights = self._expr_dict_zjet.replace_expressions(_pd['weights'])
                _x_expr = self._expr_dict_zjet.replace_expressions(_pd['x_expression'])
                _y_expr = _pd.get('y_expression')

                # -- distinguish two main cases: 1D histos and 2D profiles
                if _y_expr is not None:
                    # if y_expression given -> 2D profile
                    _y_expr = self._expr_dict_zjet.replace_expressions(_y_expr)

                    # -- create the (temporary) profile histos
                    _data_prof_y_label = "Data_{}_y_prof".format(_plot_label)
                    _data_prof_x_label = "Data_{}_x_prof".format(_plot_label)
                    _data_prof_y_obj = self._create_root_histogram(_data_prof_y_label,
                                                                   "TProfile",
                                                                   _pd['x_bins'])
                    _data_prof_x_obj = _data_prof_y_obj.Clone(_data_prof_x_label)

                    _mc_prof_y_label = "MC_{}_y_prof".format(_plot_label)
                    _mc_prof_x_label = "MC_{}_x_prof".format(_plot_label)
                    _mc_prof_y_obj = self._create_root_histogram(_mc_prof_y_label,
                                                                 "TProfile",
                                                                 _pd['x_bins'])
                    _mc_prof_x_obj = _mc_prof_y_obj.Clone(_mc_prof_x_label)

                    # -- fill the profile histos from the TTree
                    _root_ntuple_data.Project(_data_prof_y_label, "{}:{}".format(_y_expr, _x_expr), _weights, "prof goff")
                    _root_ntuple_mc.Project(_mc_prof_y_label, "{}:{}".format(_y_expr, _x_expr), _weights, "prof goff")
                    _root_ntuple_data.Project(_data_prof_x_label, "{}:{}".format(_x_expr, _x_expr), _weights, "prof goff")
                    _root_ntuple_mc.Project(_mc_prof_x_label, "{}:{}".format(_x_expr, _x_expr), _weights, "prof goff")

                    _data_prof_y = _root_file_output.Get(_data_prof_y_label)
                    _mc_prof_y = _root_file_output.Get(_mc_prof_y_label)
                    _data_prof_x = _root_file_output.Get(_data_prof_x_label)
                    _mc_prof_x = _root_file_output.Get(_mc_prof_x_label)


                    # -- create ratio histogram
                    _ratio_obj = _data_prof_y_obj.ProjectionX().Clone("Ratio_{}".format(_plot_label))
                    _ratio_obj.Divide(_mc_prof_y_obj.ProjectionX())
                    _ratio_obj.SetTitle("Ratio_{}".format(_plot_label))

                    # -- convert data, mc profiles to TGraphErrors
                    _tge_data = self._profile_to_tgrapherrors("Data_{}".format(_plot_label), _data_prof_x, _data_prof_y)
                    _tge_mc = self._profile_to_tgrapherrors("MC_{}".format(_plot_label), _mc_prof_x, _mc_prof_y)
                else:
                    # if y_expression not given -> 1D histogram

                    # -- create the 1D histos
                    _data_label = "Data_{}".format(_plot_label)
                    _data_obj = self._create_root_histogram(_data_label,
                                                            "TH1D",
                                                            _pd['x_bins'])

                    _mc_label = "MC_{}".format(_plot_label)
                    _mc_obj = self._create_root_histogram(_mc_label,
                                                          "TH1D",
                                                          _pd['x_bins'])

                    # -- fill the profile histos from the TTree
                    _root_ntuple_data.Project(_data_label, "{}".format(_x_expr), _weights, "goff")
                    _root_ntuple_mc.Project(_mc_label, "{}".format(_x_expr), _weights, "goff")

                    # -- create ratio histogram
                    _ratio_obj = _data_obj.Clone("Ratio_{}".format(_plot_label))
                    _ratio_obj.Divide(_mc_obj)
                    _ratio_obj.SetTitle("Ratio_{}".format(_plot_label))

                    # -- convert data, mc profiles to TGraphErrors
                    _tge_data = _data_obj
                    _tge_mc = _mc_obj

                # -- write out everything
                _tge_data.Write()
                _tge_mc.Write()
                _ratio_obj.Write()

        print 'Done!'
        print 'Output file is: {}'.format(self._output_filename)
        _root_file_output.Close()


class CombinationMerlin(object):
    """Create a ROOT file containing histograms for specified quantities.

    This class constructs and passes plot config dictionaries to Merlin,
    which then creates the combination file.
    """

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

        self._global_cuts = "1.0"
        if self._selection is not None:
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
                                     self._sample_data['source_label'],
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
        """generator yielding prepared Merlin dictionaries in batches of ``n_plots_per_batch``"""
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