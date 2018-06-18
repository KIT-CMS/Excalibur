import abc
import itertools

import Excalibur.Plotting.harryinterface as harryinterface

from copy import deepcopy

from Excalibur.JEC_Plotter.core.quantities import BinSpec, CutSet, QUANTITIES

CHANNEL_SPEC = {
    'Zmm' : {
        'label': r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"
    },
    'Zee' : {
        'label': r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"
    }
}


"""
Private containers (one object per plot)
"""


class _PlotBase(object):
    _FORBIDDEN_KWARGS = {}

    DEFAULT_INFOBOX_TOPLEFT_XY = (0.65, 0.77)
    _INFOBOX_SPACING_Y = 0.05

    DEFAULT_CORRTEXT_TOPLEFT_XY = (0.68, 0.09)

    DEFAULT_Y_SUBPLOT_LIMS = [0.95, 1.05]
    DEFAULT_Y_SUBPLOT_LABEL = "Ratio"

    def __init__(self,
                 # -- mandatory args
                 basename,
                 quantities,
                 selection,
                 samples,
                 cut_sets,
                 jec_correction_string,
                 # -- optional args
                 show_cut_info_text=True,         # show cut info?
                 show_corr_folder_text=True,      # show JEC corr folder?
                 plot_label=None,     # label for upper-right
                 y_log_scale=False,   # apply log scale to y axis
                 upload_to_www=True,  # upload plot to www?
                 cut_info_text_topleft_xy=None,  # xy position of infobox
                 jec_corr_text_topleft_xy=None,  # xy position of JEC correction text
                 y_subplot_label=None,  # subplot y axis label
                 y_subplot_range=None,  # subplot y axis label
                 legend_position=None,  # legend position
                 ):

        # -- mandatory args
        self._basename = basename
        self._qs = quantities
        self._selection = selection
        self._samples = samples
        self._cut_sets = cut_sets
        self._jec_correction_string = jec_correction_string

        # -- optional args
        self._show_cut_info_text = show_cut_info_text
        self._show_corr_folder_text = show_corr_folder_text
        self._plot_label = plot_label
        self._y_log_scale = y_log_scale
        self._upload_to_www = upload_to_www
        self._cut_info_text_topleft_xy = cut_info_text_topleft_xy or self.DEFAULT_INFOBOX_TOPLEFT_XY
        self._jec_corr_text_topleft_xy = jec_corr_text_topleft_xy or self.DEFAULT_CORRTEXT_TOPLEFT_XY
        self._y_subplot_label = y_subplot_label or self.DEFAULT_Y_SUBPLOT_LABEL
        self._y_subplot_range = y_subplot_range or self.DEFAULT_Y_SUBPLOT_LIMS
        self._legend_position = legend_position

        self._nsamples = len(self._samples)
        if self._cut_sets is None or not self._cut_sets:
            self._cut_sets = [None]

        _ncutsets = len(self._cut_sets)
        if _ncutsets == 1:
            self._cut_sets = [self._cut_sets[0]] * self._nsamples

        if len(self._cut_sets) != self._nsamples:
            raise ValueError("Number of cuts ({}) must match "
                             "the number of samples ({}) provided!".format( len(self._cut_sets), self._nsamples))

        self._basic_weights_string = self._selection.weights_string

        self._channel = self._samples[0]['channel']
        assert all([_sample['channel'] == self._channel for _sample in self._samples])


        self._output_folder = "_".join([self._basename,
                                   self._channel,
                                   self._jec_correction_string,
                                   self._selection.name])

        self._output_filename = self._qs[0].name
        if len(self._qs) > 1:
            self._output_filename = "_".join(reversed([_q.name for _q in self._qs[1:]])) + "_vs_" + self._output_filename

        if not self._upload_to_www:
            self._output_filename = "_".join([self._basename, self._output_filename])

    def _validate_init_kwargs_raise(self, kwargs):
        _kwargs_keys = set(kwargs.keys())
        _forbidden = _kwargs_keys.intersection(self._FORBIDDEN_KWARGS)
        if _forbidden:
            raise ValueError("Forbidden kwargs for class '{}': {}".format(self.__class__.__name__, _forbidden))

    def _init_basic_dict(self):
        self._basic_dict = {
            # data
            'zjetfolders': [self._selection.zjet_folder],

            # binning
            'x_expressions': [self._qs[0].expression],
            'x_bins': self._qs[0].bin_spec.string if self._qs[0].bin_spec is not None else None,
            'x_label': self._qs[0].label,

            # formatting
            'x_lims': list(self._qs[0].bin_spec.range) if self._qs[0].bin_spec is not None else None,
            'title': None,
            'y_log': self._y_log_scale,
            'x_log': self._qs[0].log_scale,

            'dataset_title': self._plot_label,

            # web gallery options
            'filename': self._output_filename,

            # texts
            "texts": [
                CHANNEL_SPEC.get(self._channel, {}).get('label', ""),
            ],
            "texts_size": [
                20,
            ],
            "texts_x": [
                0.1, #self._cut_info_text_topleft_xy[0],
            ],
            "texts_y": [
                1.08, #self._cut_info_text_topleft_xy[1],
            ],

            'analysis_modules': [],

            # -- filled in per sample/cut group
            'nicks': [],
            'weights': [],
            'files': [],
            'labels': [],
            'corrections': [],
            'colors': [],
            'markers': [],
            'step': [],
            'line_styles': [],
            'y_errors': [],
            'x_errors': [],
            'stacks': [],
        }

        # if 'y' quantity is provided:
        if len(self._qs) > 1:
            self._basic_dict.update({
                # binning
                'y_expressions': [self._qs[1].expression],
                'y_bins': self._qs[1].bin_spec.string if self._qs[1].bin_spec is not None else None,
                'y_label': self._qs[1].label,

                'y_lims': list(self._qs[1].bin_spec.range) if self._qs[1].bin_spec is not None else None,
                'y_log': self._qs[1].log_scale,  # use quantity-based decision instead of kwarg
            })

        if self._legend_position:
            self._basic_dict['legend'] = self._legend_position

        if self._show_corr_folder_text:
            # add JEC correction folder info
            self._basic_dict['texts'].append(r"$\\bf{{{0}}}$".format(self._jec_correction_string))
            self._basic_dict['texts_size'].append(25)
            self._basic_dict['texts_x'].append(self._jec_corr_text_topleft_xy[0])
            self._basic_dict['texts_y'].append(self._jec_corr_text_topleft_xy[1])

        if self._show_cut_info_text:
            # add cut labels as text
            for _i, _cl in enumerate(self._selection.texts):
                self._basic_dict['texts'].append(_cl)
                self._basic_dict['texts_size'].append(15)
                self._basic_dict['texts_x'].append(self._cut_info_text_topleft_xy[0])
                self._basic_dict['texts_y'].append(self._cut_info_text_topleft_xy[1] - 0.07 - (_i + 1) * self._INFOBOX_SPACING_Y)

        if self._upload_to_www:
            self._basic_dict['www'] = self._output_folder


    @abc.abstractmethod
    def get_dict(self):
        raise NotImplementedError("Pure abstract method called!")

    @property
    def quantities(self):
        return self._qs

    @property
    def basename(self):
        return self._basename

    @property
    def selection(self):
        return self._selection

    @property
    def samples(self):
        return self._samples

    @property
    def jec_correction_string(self):
        return self._jec_correction_string

    @property
    def output_filename(self):
        return self._output_filename

    @property
    def output_folder(self):
        return self._output_folder


    def add_text(self, text, size, xy):
        assert len(xy) == 2
        self._basic_dict['texts'].append(text)
        self._basic_dict['texts_size'].append(size)
        self._basic_dict['texts_x'].append(xy[0])
        self._basic_dict['texts_y'].append(xy[1])
    

    def make_plot(self, args=None):
        _plot_dicts = [self.get_dict()]
        harryinterface.harry_interface(_plot_dicts, (args or []) + ['--max-processes', '1'])

class _Plot1D(_PlotBase):
    _FORBIDDEN_KWARGS = {}

    def __init__(self,
                 basename,            # base name of the plot
                 quantity,            # x-axis quantity
                 selection,           # selection to apply to samples
                 samples,             # data samples (N)
                 cut_sets,            # cut sets for the samples (N)
                 jec_correction_string,   # JEC correction string
                 # -- Plot1D args
                 normalize_to_first_histo=False,  # normalize all histos to first?
                 show_ratio_to_first=False,       # show the ratio to first in lower pad?
                 show_first_in_ratio=False,       # show the reference at 1.0 in ratio pad?
                 stacked=False,                   # stack histograms?
                 **kwargs):

        super(_Plot1D, self).__init__(
            basename=basename,
            quantities=[quantity],
            selection=selection,
            samples=samples,
            cut_sets=cut_sets,
            jec_correction_string=jec_correction_string,
            **kwargs)

        self._normalize_to_first_histo = normalize_to_first_histo
        self._show_ratio_to_first = show_ratio_to_first
        self._show_first_in_ratio = show_first_in_ratio
        self._stacked = stacked

        self._init_basic_dict()

    def _init_basic_dict(self):
        super(_Plot1D, self)._init_basic_dict()

        if self._show_ratio_to_first:
            self._basic_dict.update({
                'analysis_modules': ["Ratio"],
                'ratio_denominator_no_errors': False,
                'subplot_fraction': 25,
            })

    def get_dict(self):
        _d = deepcopy(self._basic_dict)

        for _i, (_sample, _cutset) in enumerate(zip(self._samples, self._cut_sets)):

            # skip quantities not available in certain channels
            if not all([_q.available_for_channel(_sample['channel']) for _q in self.quantities]):
                continue

            # skip quantities not available in certain source types (data/MC)
            if not all([_q.available_for_source_type(_sample['source_type']) for _q in self.quantities]):
                continue

            _d['nicks'].append("nick{}".format(_i))
            _d['files'].append(_sample['file'])
            _d['labels'].append("{source_type} ({source_label})".format(**_sample._dict))
            _d['corrections'].append(self._jec_correction_string)
            if _cutset is not None:
                _d['weights'].append(self._basic_weights_string + '&&' + _cutset.weights_string)
            else:
                _d['weights'].append(self._basic_weights_string)

            if hasattr(self, '_stacked') and self._stacked:
                _d['stacks'].append("single_stack")
                _d['markers'].append(_sample._dict.get('marker', 'bar'))
            else:
                _d['stacks'].append("stack{}".format(_i))
                _d['markers'].append(_sample._dict.get('marker', '_'))

            _d['step'].append(_sample._dict.get('step_flag', False))
            if _d['step'][-1]:
                _d['line_styles'].append(_sample._dict.get('line_styles', "-"))
            else:
                _d['line_styles'].append(_sample._dict.get('line_styles', ""))

            _d['colors'].append(_sample['color'])

            _d['y_errors'].append(True)
            _d['x_errors'].append(True)

            # default to 'L1L2L3' for Monte Carlo
            if self._jec_correction_string == 'L1L2L3Res' and _sample['source_type'] != 'Data':
                _d['corrections'][-1] = 'L1L2L3'
            elif self._jec_correction_string == 'L1L2Res' and _sample['source_type'] != 'Data':
                _d['corrections'][-1] = 'L1L2L3'

        if hasattr(self, '_show_ratio_to_first') and self._show_ratio_to_first:
            # determine the first index to show in the ratio plot
            _start_index = 1
            if self._show_first_in_ratio:
                _start_index = 0

            # compute the numerator and ratio result nicks
            _num_nicks = ["nick{}".format(i) for i in range(_start_index, self._nsamples)]
            _res_nicks = ["nick{}_over0".format(i) for i in range(_start_index, self._nsamples)]

            # update plot dict
            _d.update({
                "ratio_numerator_nicks": _num_nicks,
                "ratio_denominator_nicks": ["nick0"],
                "ratio_result_nicks": _res_nicks,
                "subplot_nicks": _res_nicks,
                "y_subplot_label": self._y_subplot_label,
                'y_subplot_lims': self._y_subplot_range,
                'y_errors': _d['y_errors'] + [True] * len(_num_nicks),
                'x_errors': _d['x_errors'] + [False] * len(_num_nicks),
            })

            # make sure subplot properties follow the main plot
            for _prop in ('colors', 'markers', 'step', 'line_styles', 'labels'):
                if _prop in _d and len(_d[_prop]) > _start_index:
                    _d[_prop] += [_d[_prop][i] for i in range(_start_index, self._nsamples)]

            # need to create a 'parallel' set of stacks for the ratios
            # to avoid stacking ratios and non-rations together...
            if 'stacks' in _d:
                _d['stacks'].extend(['stack_'+_stackname for _stackname in _res_nicks])

        if hasattr(self, '_normalize_to_first_histo') and self._normalize_to_first_histo and len(_d['files']) > 1:
            # just insert analysis module at front of list
            _d['analysis_modules'].insert(0, "NormalizeToFirstHisto")

        return _d

    def count_events(self, write_to_file=False):
        """
        Return the number of events passing the selection indicated by the `weights` plot keyword.
        :return:
        """
        import ROOT

        _d = self.get_dict()
        _filenames = _d['files']
        _weights = _d['weights']

        if len(_filenames) != len(_weights):
            if len(_weights) == 1:
                _weights = [_weights[0]]*len(_filenames)
            elif len(_filenames) == 1:
                _filenames = [_filenames[0]]*len(_weights)
            else:
                ValueError("Length of 'files' ({}) and 'weights' ({}) "
                           "plot dict entries do not match!".format(len(_filenames), len(_weights)))

        assert len(_filenames) == len(_weights)

        _results = dict(files=[], weights=[], event_count=[])
        for _filename, _weight_string in zip(_filenames, _weights):
            _file = ROOT.TFile(_filename)
            _ntuple = _file.Get("{}/ntuple".format(self._selection.zjet_folder + '_' + self._jec_correction_string))

            # count events after applying the `weights`
            _n_after_cuts = _ntuple.Draw(">>elist", _weight_string, "goff")
            _results['files'].append(_filename)
            _results['weights'].append(_weight_string)
            _results['event_count'].append(_n_after_cuts)

        if write_to_file:
            import json, os, datetime
            _eventcount_output_filename = _d['filename'] + '_eventcount.json'

            _plot_output_dir = _d.get("output_dir", None)
            if _plot_output_dir is None:
                _plot_output_dir = os.path.join(
                    "websync",
                    datetime.date.today().strftime("%Y_%m_%d"),
                    (_d.get("www", None) or "")
                )

            _plot_output_path = os.path.join(_plot_output_dir, _eventcount_output_filename)

            print "[JEC_Plotter] Writing event count report to: '{}'".format(_plot_output_path)
            with open(_plot_output_path, 'w') as _f:
                json.dump(_results, _f, indent=4)

        return _results


class _Plot1DFractions(_Plot1D):
    _FORBIDDEN_KWARGS = {'normalize_to_first_histo', 'show_ratio_to_first', 'show_first_in_ratio', 'stacked', 'y_log_scale'}

    def __init__(self,
                 # -- PlotBase args
                 basename,            # base name of the plot
                 quantity,            # x-axis quantity
                 selection,           # selection to apply to samples
                 sample,              # *one* data sample
                 cut_sets,            # cut sets for the different fractions
                 cut_set_colors,      # colors for the different fractions
                 cut_set_labels,      # labels for the different fractions
                 jec_correction_string,   # JEC correction string
                 # -- Plot1DFractions args
                 reference_cut_set,
                 y_label,
                 **kwargs):

        self._validate_init_kwargs_raise(kwargs)

        assert len(cut_set_colors) == len(cut_sets)
        assert len(cut_set_labels) == len(cut_sets)

        self._ref_cut_set = reference_cut_set
        self._y_label = y_label

        super(_Plot1DFractions, self).__init__(
            # -- PlotBase args
            basename=basename,
            quantity=quantity,
            selection=selection,
            samples=[sample] * (len(cut_sets)),
            cut_sets=cut_sets,
            jec_correction_string=jec_correction_string,
            y_log_scale=False,
            # -- Plot1D explicit args
            normalize_to_first_histo=False,
            show_ratio_to_first=True,
            show_first_in_ratio=True,
            stacked=False,
            **kwargs)

        self._cut_set_colors = cut_set_colors
        self._cut_set_labels = cut_set_labels

        self._init_basic_dict()

    def _init_basic_dict(self):
        super(_Plot1DFractions, self)._init_basic_dict()
        self._basic_dict.update({
            "subplot_fraction": 0,  # do not show lower plot axes
            "subplot_nicks": ["_dummy"],  # HARRYPLOTTER!!
            "ratio_denominator_no_errors": "false",
            "stacks": ["single_stack"],
            "markers": 'bar',
            "y_label": self._y_label,
            "y_lims": [0, 1.29],
            "y_log": False,

            "ratio_denominator_nicks": ["nick0"],  # divide by reference
            "nicks_blacklist": ["nick0_over0", "^nick0$"],  # do not plot reference
            "y_errors": True,
            "x_errors": None,
            "line_styles": None,
            "analysis_modules": ["Ratio"],

            'files': [self._samples[0]['file']],
            'step': [self._samples[0]._dict.get('step_flag', False)],

        })

    def get_dict(self):
        _d = deepcopy(self._basic_dict)

        # reference (total of fraction)
        _d['weights'].append(self._basic_weights_string)

        # default to 'L1L2L3' for Monte Carlo
        _corr_string = self._jec_correction_string
        if self._jec_correction_string == 'L1L2L3Res' and self._samples[0]['source_type'] != 'Data':
            _corr_string = 'L1L2L3'
        elif self._jec_correction_string == 'L1L2Res' and self._samples[0]['source_type'] != 'Data':
            _corr_string = 'L1L2L3'
        _d['corrections'] = [_corr_string]

        _numerator_nicks = ['nick0']
        _ratio_nicks = ['nick0_over0']
        for _i, (_frac_cutset) in reversed(list(enumerate(self._cut_sets))):
            # things to add later
            _numerator_nicks.append("nick{}".format(_i+1))
            _ratio_nicks.append("nick{}_over0".format(_i+1))

            # default to 'L1L2L3' for Monte Carlo
            _corr_string = self._jec_correction_string
            if self._jec_correction_string == 'L1L2L3Res' and _sample['source_type'] != 'Data':
                _corr_string = 'L1L2L3'
            elif self._jec_correction_string == 'L1L2Res' and _sample['source_type'] != 'Data':
                _corr_string = 'L1L2L3'

            if _frac_cutset is not None:
                _d['weights'].append(self._basic_weights_string + '&&' + _frac_cutset.weights_string)
            else:
                _d['weights'].append(self._basic_weights_string)


            _d['corrections'].append(_corr_string)
            _d['labels'].append(self._cut_set_labels[_i])
            _d['colors'].append(self._cut_set_colors[_i])
            #_d['y_errors'].append(True)
            _d['nicks_blacklist'].append("^{}$".format(_numerator_nicks[-1]))

        _d.update({
            "nicks":_numerator_nicks + _ratio_nicks,
            "ratio_numerator_nicks": _numerator_nicks,
            "ratio_result_nicks": _ratio_nicks,
        })

        return _d


class _Plot2D(_PlotBase):
    _FORBIDDEN_KWARGS = {'y_log_scale', 'quantities', 'quantity'}

    def __init__(self,
                 # -- PlotBase args
                 basename,            # base name of the plot
                 quantity_pair,       # x- and y-axis quantities
                 selection,           # selection to apply to samples
                 sample,              # *one* data sample
                 jec_correction_string,   # JEC correction string
                 **kwargs):

        self._validate_init_kwargs_raise(kwargs)

        assert len(quantity_pair) == 2
        super(_Plot2D, self).__init__(
            # -- PlotBase args
            basename=basename,
            quantities=list(quantity_pair),
            selection=selection,
            samples=[sample],
            cut_sets=[None],
            jec_correction_string=jec_correction_string,
            **kwargs)

        self._init_basic_dict()

    def _init_basic_dict(self):
        _PlotBase._init_basic_dict.im_func(self)
        self._basic_dict.update({
            'line_styles': ['-']
        })

    def get_dict(self):
        return _Plot1D.get_dict.im_func(self)  # same as 1D method


class _PlotProfile(_PlotBase):
    _FORBIDDEN_KWARGS = {'y_log_scale', 'normalize_to_first_histo', 'stacked'}

    def __init__(self,
                 basename,            # base name of the plot
                 quantity_pair,       # x- and y-axis quantities
                 selection,           # selection to apply to samples
                 samples,             # data samples (N)
                 cut_sets,            # cut sets for the samples (N)
                 jec_correction_string,   # JEC correction string
                 # -- Plot1D args
                 show_ratio_to_first=False,       # show the ratio to first in lower pad?
                 show_first_in_ratio=False,       # show the reference at 1.0 in ratio pad?
                 **kwargs):

        assert len(quantity_pair) == 2
        super(_PlotProfile, self).__init__(
            basename=basename,
            quantities=[quantity_pair[0], quantity_pair[1]],
            selection=selection,
            samples=samples,
            cut_sets=cut_sets,
            jec_correction_string=jec_correction_string,
            **kwargs)

        self._show_ratio_to_first = show_ratio_to_first
        self._show_first_in_ratio = show_first_in_ratio

        self._init_basic_dict()

    def _init_basic_dict(self):
        _PlotBase._init_basic_dict.im_func(self)
        self._basic_dict.update({
            'line_styles': ['-']
        })

        # set profile option
        self._basic_dict['tree_draw_options'] = 'prof'

        # acommodate ratio
        if self._show_ratio_to_first:
            self._basic_dict.update({
                'analysis_modules': ["Ratio"],
                'ratio_denominator_no_errors': False,
                'subplot_fraction': 25,
            })


    def get_dict(self):
        _d = _Plot1D.get_dict.im_func(self)  # same as 2D method

        # override markers for profile
        _d['markers'] = ['.']
        _d['step'] = [False]
        _d['line_styles'] = ""
        _d['x_errors'] = True
        del _d['y_bins']  # HARRYPLOTTER!!!

        return _d


class _PlotStackProfile(_PlotBase):
    _FORBIDDEN_KWARGS = {'normalize_to_first_histo', 'stacked', 'cut_sets'}

    # todo: implement cycler
    _COLORS_CYCLE = ['orange', 'royalblue', 'green', 'violet', 'teal', 'brown']
    _MARKERS_CYCLE = ['o', 's', 'd', '^', '*', 'v']

    def __init__(self,
                 basename,
                 quantity_x,
                 quantities_y,
                 selection,
                 sample_mc,
                 sample_data,
                 jec_correction_string,
                 y_label,
                 y_range,
                 show_data_mc_comparison_as=None,
                 colors_mc=None,
                 markers_data=None,
                 **kwargs):

        self._validate_init_kwargs_raise(kwargs)

        super(_PlotStackProfile, self).__init__(
            basename=basename,
            quantities=[quantity_x] + quantities_y,
            selection=selection,
            samples=[sample_mc, sample_data],
            cut_sets=[None, None],
            jec_correction_string=jec_correction_string,
            **kwargs)

        self._qx = self._qs[0]
        self._qys = self._qs[1:]

        self._sample_mc = self._samples[0]
        self._sample_data = self._samples[1]

        self._dmc_comparison_type = show_data_mc_comparison_as
        if self._dmc_comparison_type is not None:
            self._dmc_comparison_type = self._dmc_comparison_type.lower()

        #self._stacked = False

        self._y_label = y_label
        self._y_range = y_range
        if self._y_range is None:
            self._y_range = min([_q.bin_spec.range[0] for _q in self._qys]), max([_q.bin_spec.range[1] for _q in self._qys])

        self._colors_mc = colors_mc or self._COLORS_CYCLE
        self._markers_data = markers_data or self._MARKERS_CYCLE

        self._init_basic_dict()


    def _init_basic_dict(self):
        super(_PlotStackProfile, self)._init_basic_dict()

        self._basic_dict.update({
            'legend': "lower left",
            'y_lims': list(self._y_range),
            'y_label': self._y_label,

            # set the following for each sample/cut group in get_dict
            'y_expressions': [],
            'line_styles': [],
            'alphas': [],

            'tree_draw_options': 'prof'
        })


    def get_dict(self):
        _d = deepcopy(self._basic_dict)

        for _sample in (self._sample_mc, self._sample_data):
            for _i, _qy in enumerate(self._qys):

                # skip quantities not available in certain channels
                if not _qy.available_for_channel(_sample['channel']):
                    continue

                # skip quantities not available in certain source types (data/MC)
                if not _qy.available_for_source_type(_sample['source_type']):
                    continue

                _d['files'].append(_sample['file'])
                _d['corrections'].append(self._jec_correction_string)
                _d['weights'].append(self._basic_weights_string)

                #_d['markers'].append(self._sample._dict.get('marker', 'bar'))

                _d['y_expressions'].append(_qy.expression)

                _d['line_styles'].append("")
                _d['step'].append(True)

                if _sample['source_type'] == 'MC':
                    _d['nicks'].append("mc{}".format(_i))
                    _d['stacks'].append("stack_mc")
                    _d['markers'].append('bar')
                    _d['colors'].append(self._colors_mc[_i % len(self._colors_mc)])
                    _d['alphas'].append(1.0)
                    _d['x_errors'].append(False)
                    _d['labels'].append("{}".format(_qy.label))
                else:
                    _d['nicks'].append("data{}".format(_i))
                    _d['stacks'].append("stack_data")
                    _d['markers'].append(self._markers_data[_i % len(self._markers_data)])
                    _d['colors'].append('k')
                    _d['alphas'].append(1.0)
                    _d['x_errors'].append(True)
                    _d['labels'].append("{}".format(_qy.label))

                _d['y_errors'].append(True)

                # default to 'L1L2L3' for Monte Carlo
                if self._jec_correction_string == 'L1L2L3Res' and _sample['source_type'] != 'Data':
                    _d['corrections'][-1] = 'L1L2L3'
                elif self._jec_correction_string == 'L1L2Res' and _sample['source_type'] != 'Data':
                    _d['corrections'][-1] = 'L1L2L3'

        if self._dmc_comparison_type == 'ratio':
            _d['analysis_modules'].append("Ratio")
            _numer_nicks = ["data{}".format(i) for i in range(len(self._qys))]
            _denom_nicks = ["mc{}".format(i) for i in range(len(self._qys))]
            _res_nicks = ["ratio{}".format(i) for i in range(len(self._qys))]

            _d.update({
                "ratio_numerator_nicks": _numer_nicks,
                "ratio_denominator_nicks": _denom_nicks,
                "ratio_result_nicks": _res_nicks,
                "subplot_lines": [1.0],
                "subplot_nicks": _res_nicks,
                "y_subplot_label": "Data/MC",
                # 'y_subplot_lims': [0.5, 4.1],
                'y_subplot_lims': [0.75, 1.25],
                'subplot_fraction': 20,

                # -- extend
                'labels': _d['labels'] + [""] * len(_numer_nicks),
                'stacks': _d['stacks'] + ["ratio_stack_{}".format(_i) for _i in range(len(_numer_nicks))],
                'markers': _d['markers'] + [self._markers_data[_i % len(self._markers_data)] for _i in range(len(_numer_nicks))],
                'colors': _d['colors'] +  [self._colors_mc[_i % len(self._colors_mc)] for _i in range(len(_numer_nicks))],
                'alphas': _d['alphas'] + [1.0] * len(_numer_nicks),

                'y_errors': _d['y_errors'] + [True] * len(_numer_nicks),
                'x_errors': _d['x_errors'] + [False] * len(_numer_nicks),

                'step': _d['step'] + [True] * len(_numer_nicks),
                'line_styles': _d['line_styles'] + [""] * len(_numer_nicks),
            })
        elif self._dmc_comparison_type.startswith('difference'):
            _d['analysis_modules'].append("AddHistograms")
            _plus_nicks = ["data{}".format(i) for i in range(len(self._qys))]
            _minus_nicks = ["mc{}".format(i) for i in range(len(self._qys))]
            _res_nicks = ["diff{}".format(i) for i in range(len(self._qys))]

            _d.update({
                "add_nicks": ["{0} {1}".format(_pn, _mn) for _pn, _mn in zip(_plus_nicks, _minus_nicks)],
                "add_result_nicks": _res_nicks,
                "add_scale_factors": ["1.0 -1.0" for _ in _plus_nicks],
                "subplot_lines": [0.0],
                "subplot_nicks": _res_nicks,
                "y_subplot_label": "Data-MC",
                # 'y_subplot_lims': [0.5, 4.1],
                'y_subplot_lims': [-0.1, 0.1],
                'subplot_fraction': 20,
            })

            if 'percent' in self._dmc_comparison_type:
                _d.update({
                    "add_scale_factors": ["100.0 -100.0" for _ in _plus_nicks],
                    "y_subplot_label": "Data-MC (%)",
                    'y_subplot_lims': [100 * _l for _l in _d['y_subplot_lims']],
                })

            _new_nick_dict = {}
            _new_nick_dict['labels'] = [""] * len(_plus_nicks)
            _new_nick_dict['stacks'] = ["difference_stack_{}".format(_i) for _i in range(len(_plus_nicks))]
            _new_nick_dict['markers'] = [self._markers_data[_i % len(self._markers_data)] for _i in range(len(_plus_nicks))]
            _new_nick_dict['colors'] =  [self._colors_mc[_i % len(self._colors_mc)] for _i in range(len(_plus_nicks))]
            _new_nick_dict['alphas'] = [1.0] * len(_plus_nicks)
            _new_nick_dict['y_errors'] = [True] * len(_plus_nicks)
            _new_nick_dict['x_errors'] = [False] * len(_plus_nicks)
            _new_nick_dict['step'] = [True] * len(_plus_nicks)
            _new_nick_dict['line_styles'] = [""] * len(_plus_nicks)

            for _i_input_nick in range(len(_plus_nicks)):
                for _key in _new_nick_dict:
                    _new_pos = len(_plus_nicks) + 2*_i_input_nick
                    _d[_key].insert(_new_pos, _new_nick_dict[_key][_i_input_nick])

        if 'y_bins' in _d:
            del _d['y_bins']  # HARRYPLOTTER!!!

        return _d


class _PlotExtrapolation(_PlotBase):
    _FORBIDDEN_KWARGS = {'normalize_to_first_histo', 'show_ratio_to_first', 'show_first_in_ratio', 'stacked', 'y_log_scale'}

    # todo: implement cycler
    _LIGHT_COLORS_CYCLE = ['orange', 'royalblue', 'green']
    _DARK_COLORS_CYCLE = ['darkred', 'darkblue', 'darkgreen']

    def __init__(self,
                 # -- PlotBase args
                 basename,            # base name of the plot
                 response_quantities,
                 extrapolation_quantity,
                 selection,           # selection to apply to samples
                 sample_data,
                 sample_mc,
                 jec_correction_string,   # JEC correction string
                 # -- _PlotExtrapolation args
                 fit_function_range,
                 n_extrapolation_bins,
                 additional_cut_dict=None,
                 **kwargs):

        self._validate_init_kwargs_raise(kwargs)

        super(_PlotExtrapolation, self).__init__(
             basename=basename,                 # base name of the plot
             quantities=[extrapolation_quantity] + list(response_quantities),
             selection=selection,               # selection to apply to samples
             samples=[sample_data, sample_mc],  # data samples (N)
             cut_sets=[None, None],             # cut sets for the samples (N)
             jec_correction_string=jec_correction_string, # JEC correction string
             **kwargs)

        self._qys = response_quantities
        self._qx = extrapolation_quantity

        self._sample_data = sample_data
        self._sample_mc = sample_mc

        self._add_cut_dict = additional_cut_dict

        self._function_range = fit_function_range
        assert len(self._function_range) == 2

        self._data_source_label = self._sample_data._dict['source_label']
        self._mc_source_label = self._sample_mc._dict['source_label']

        self._bin_spec = BinSpec.make_equidistant(n_extrapolation_bins, self._function_range)

        self._channel = self._sample_data['channel']
        assert self._sample_data["channel"] == self._sample_mc["channel"]

        # compute y variable limits
        self._y_range = None
        for _qy in self._qys:
            _bs = _qy.bin_spec
            if _bs is None:
                continue
            _rg = _bs.range
            if self._y_range is None:
                self._y_range = list(_rg)
            else:
                # expand range as needed
                self._y_range[0] = min(self._y_range[0], _rg[0])
                self._y_range[1] = max(self._y_range[1], _rg[1])

        # override the output names
        self._output_folder = "_".join([self._basename,
                                   self._channel,
                                   self._jec_correction_string,
                                   self._selection.name])
        self._output_filename = '{}'.format(self._basename)

        # compute total cut weight string
        _total_cut = self._selection
        if self._add_cut_dict:
            _add_cut = self._add_cut_dict.get('cut', None)
            if _add_cut is not None:
                _total_cut = self._selection + _add_cut
                self._output_filename += "_{}".format(_add_cut.name)
                # replace data source label with cut label
                self._data_source_label = self._add_cut_dict.get('label', self._data_source_label)
                # FIXME: what about MC?

        self._basic_weights_string = _total_cut.weights_string

        self._init_basic_dict()


    def _init_basic_dict(self):
        super(_PlotExtrapolation, self)._init_basic_dict()
        self._basic_dict.update({
            'x_bins': self._bin_spec.string,
            'y_label': "Jet Response",
            'weights': [self._basic_weights_string],
            'y_subplot_label': self._y_subplot_label,
            'y_subplot_lims': self._y_subplot_range,
            'y_lims': [0.6, 1.2],

            'line_widths': '1',

            'analysis_modules': [
                "Ratio",
                "FunctionPlot"
            ],
            'plot_modules': [
                "PlotMplZJet",
                "PlotExtrapolationText",
            ],

            'function_parameters': ["1,1,1"],
            'function_ranges': [",".join(map(str, self._function_range))],
            'functions': ["[0]+[1]*x"],

            'lines': [1],
            'legend': "lower left",
            'subplot_fraction': 30,
            'subplot_legend': "lower right",
            "ratio_denominator_no_errors": "false",

            'tree_draw_options': 'prof',

            # -- filled in per sample/response quantity
            'y_expressions': [],
            'extrapolation_text_colors': [],
            'extrapolation_text_nicks': [],
            'function_fit': [],
            'function_nicknames': [],
            "ratio_result_nicks": [],
            "ratio_numerator_nicks": [],
            "ratio_denominator_nicks": [],

            'marker_fill_styles': [],
            'alphas': 0.3    # transparency
        })
        for _prop in ('stacks', 'step', 'y_bins', 'y_errors', 'x_errors'):
            if _prop in self._basic_dict:
                del self._basic_dict[_prop]


    def get_dict(self):
        _d = deepcopy(self._basic_dict)

        for _qy in self._qys:
            _d['y_expressions'].extend(
                [_qy.expression, _qy.expression]
            )
            _d['files'].extend([
                "{}".format(self._sample_data['file']),
                "{}".format(self._sample_mc['file'])
            ])
            _d['corrections'].extend([
                "{}".format(self._jec_correction_string),
                "L1L2L3"  # MC is always L1L2L3
            ])
            _d['nicks'].extend([
                "{}_data".format(_qy.name),
                "{}_mc".format(_qy.name)
            ])
            _d['labels'].extend([
                "{0} {source_type} ({1})".format(_qy.label, self._data_source_label, **self._sample_data._dict),
                "{0} {source_type} ({1})".format(_qy.label, self._mc_source_label, **self._sample_mc._dict),
            ])
            _d['ratio_numerator_nicks'].append("{}_data".format(_qy.name))
            _d['ratio_denominator_nicks'].append("{}_mc".format(_qy.name))
            _d['ratio_result_nicks'].append("{}_ratio".format(_qy.name))

        for _qy in self._qys:
            _d['labels'].append("{}".format(_qy.label))

        #_d['labels'] += [""] * len(self._qys) ???

        _d['markers'] = ["s", "o"] * len(self._qys) + ["o", "o"]
        _d['marker_fill_styles'] = ["none"] * len(self._qys) + ["full"] * len(self._qys) + ["none", "full"]
        _d['line_styles'] = [None]*3*len(self._qys) + ["--"]*3*len(self._qys)

        # fit both quantities and their ratios
        _d['function_fit'] = _d['nicks'] + _d['ratio_result_nicks']
        _d['function_nicknames'] = ["{}_fit".format(_n) for _n in _d['function_fit']]

        _d['extrapolation_text_nicks'] = ['{}_ratio_fit'.format(_qy.name) for _qy in self._qys]

        for _i, _qy in enumerate(self._qys):
            _d['colors'].extend([
                self._LIGHT_COLORS_CYCLE[_i % len(self._LIGHT_COLORS_CYCLE)],
                self._DARK_COLORS_CYCLE[_i % len(self._DARK_COLORS_CYCLE)]
            ])
        for _i, _qy in enumerate(self._qys):
            _col = self._DARK_COLORS_CYCLE[_i % len(self._DARK_COLORS_CYCLE)]
            _d['extrapolation_text_colors'].append(_col)
            _d['colors'].append(_col)

        return _d


"""
API classes (generation of multiple plots)
"""


class _HistoMultiPlotterBase(object):
    _PLOT_CLASS = None

    def __init__(self,
                 basename,
                 iter_specs,
                 plot_class_kwargs):
        self._plots = []
        self._basename = basename

        _keys, _transform_lambdas, _values_lists = [], [], []
        for _key_dict in iter_specs:
            _transform_lambda = _key_dict.get('transform_lambda')
            _values = _key_dict['values']
            if _transform_lambda is not None:
                _values = map(_transform_lambda, _values)
            _values = [_value for _value in _values if _value is not None]
            _values_lists.append(_values)
            _keys.append(_key_dict['key'])

        for _values_list in itertools.product(*_values_lists):
            _kwarg_dict = deepcopy(plot_class_kwargs)
            for _key, _value in zip(_keys, _values_list):
                assert _key not in _kwarg_dict
                _kwarg_dict[_key] = _value

            _plot = self._PLOT_CLASS(
                basename=self._basename,
                **_kwarg_dict
            )

            self._plots.append(_plot)

    @staticmethod
    def _get_quantity(quantity_name):
        _q = QUANTITIES.get(quantity_name, None)
        if _q is None:
            print "UNKONWN quantity '%s': skipping..." % (quantity_name,)
        return _q

    def add_text(self, text, size, xy):
        assert len(xy) == 2
        for _p in self._plots:
            _p._basic_dict['texts'].append(text)
            _p._basic_dict['texts_size'].append(size)
            _p._basic_dict['texts_x'].append(xy[0])
            _p._basic_dict['texts_y'].append(xy[1])

    def make_plots(self, args=None):
        _plot_dicts = [_p.get_dict() for _p in self._plots]
        # harryinterface.harry_interface(_plot_dicts, args)
        harryinterface.harry_interface(_plot_dicts, (args or []) + ['--max-processes', '1'])


class PlotHistograms1D(_HistoMultiPlotterBase):
    _PLOT_CLASS = _Plot1D

    def __init__(self, samples, quantities, selection_cuts,
                 additional_cuts=None,
                 basename='hist_1d',
                 jec_correction_string='L1L2L3Res',
                 show_cut_info_text=True,
                 show_corr_folder_text=True,
                 # -- Plot1D args
                 normalize_to_first_histo=False,  # normalize all histos to first?
                 show_ratio_to_first=False,       # show the ratio to first in lower pad?
                 show_first_in_ratio=False,       # show the reference at 1.0 in ratio pad?
                 stacked=False,                   # stack histograms?
                 **kwargs):

        # run over a cross product of values for the following keys
        _iter_specs = [
            {
                "key": "quantity",
                "transform_lambda": self._get_quantity,
                "values": quantities
            },
            {
                "key": "selection",
                "values": selection_cuts
            },
        ]

        plot_class_kwargs = dict(
            samples=samples,
            cut_sets=additional_cuts,
            jec_correction_string=jec_correction_string,
            show_cut_info_text=show_cut_info_text,
            show_corr_folder_text=show_corr_folder_text,
            # -- Plot1D args
            normalize_to_first_histo=normalize_to_first_histo,
            show_ratio_to_first=show_ratio_to_first,
            show_first_in_ratio=show_first_in_ratio,
            stacked=stacked,
            **kwargs
        )

        super(PlotHistograms1D, self).__init__(
            basename=basename,
            iter_specs=_iter_specs,
            plot_class_kwargs=plot_class_kwargs)


class PlotHistograms1DFractions(_HistoMultiPlotterBase):
    _PLOT_CLASS = _Plot1DFractions

    def __init__(self,
                 sample,
                 quantities, selection_cuts,  # cross-product iteration
                 fraction_cut_sets,           # cut sets for the different fractions
                 # -- PlotBase args           
                 # -- Plot1DFractions         args
                 fraction_colors,              # colors for the different fractions
                 fraction_labels,              # labels for the different fractions
                 reference_cut_set,
                 y_label,
                 basename='hist_1d_fractions',  # base name of the plot
                 jec_correction_string='L1L2L3Res',
                 **kwargs):

        # run over a cross product of values for the following keys
        _iter_specs = [
            {
                "key": "quantity",
                "transform_lambda": self._get_quantity,
                "values": quantities,
            },
            {
                "key": "selection",
                "values": selection_cuts
            },
        ]

        plot_class_kwargs = dict(
            reference_cut_set=reference_cut_set,
            sample=sample,
            cut_sets=fraction_cut_sets,
            cut_set_colors=fraction_colors,
            cut_set_labels=fraction_labels,
            jec_correction_string=jec_correction_string,
            y_label=y_label,
            **kwargs
        )

        super(PlotHistograms1DFractions, self).__init__(
            basename=basename,
            iter_specs=_iter_specs,
            plot_class_kwargs=plot_class_kwargs)


class PlotHistograms2D(_HistoMultiPlotterBase):
    _PLOT_CLASS = _Plot2D

    def __init__(self, sample, quantity_pairs, selection_cuts,
                 basename='hist_2d',
                 jec_correction_string='L1L2L3Res',
                 show_cut_info_text=True,
                 show_corr_folder_text=True,
                 **kwargs):

        # run over a cross product of values for the following keys
        _iter_specs = [
            {
                "key": "quantity_pair",
                "transform_lambda": lambda l: map(self._get_quantity, list(l)),
                "values": quantity_pairs
            },
            {
                "key": "selection",
                "values": selection_cuts
            },
        ]

        plot_class_kwargs = dict(
            sample=sample,
            jec_correction_string=jec_correction_string,
            show_cut_info_text=show_cut_info_text,
            show_corr_folder_text=show_corr_folder_text,
            # -- Plot1D args
            **kwargs
        )

        super(PlotHistograms2D, self).__init__(
            basename=basename,
            iter_specs=_iter_specs,
            plot_class_kwargs=plot_class_kwargs)


class PlotProfiles(_HistoMultiPlotterBase):
    _PLOT_CLASS = _PlotProfile

    def __init__(self, samples, quantity_pairs, selection_cuts,
                 additional_cuts=None,
                 basename='profile',
                 jec_correction_string='L1L2L3Res',
                 show_cut_info_text=True,
                 show_corr_folder_text=True,
                 # -- Plot1D args
                 show_ratio_to_first=False,       # show the ratio to first in lower pad?
                 show_first_in_ratio=False,       # show the reference at 1.0 in ratio pad?
                 **kwargs):

        # run over a cross product of values for the following keys
        _iter_specs = [
            {
                "key": "quantity_pair",
                "transform_lambda": lambda l: map(self._get_quantity, l),
                "values": quantity_pairs
            },
            {
                "key": "selection",
                "values": selection_cuts
            },
        ]

        plot_class_kwargs = dict(
            samples=samples,
            cut_sets=additional_cuts,
            jec_correction_string=jec_correction_string,
            show_cut_info_text=show_cut_info_text,
            show_corr_folder_text=show_corr_folder_text,
            # -- Plot1D args
            show_ratio_to_first=show_ratio_to_first,
            show_first_in_ratio=show_first_in_ratio,
            **kwargs
        )

        super(PlotProfiles, self).__init__(
            basename=basename,
            iter_specs=_iter_specs,
            plot_class_kwargs=plot_class_kwargs)


class PlotStackProfiles(_HistoMultiPlotterBase):
    _PLOT_CLASS = _PlotStackProfile

    def __init__(self, sample_mc, sample_data, quantity_x, quantities_y, selection_cuts,
                 y_label,
                 y_range,
                 basename='stackprofile',
                 jec_correction_string='L1L2L3Res',
                 show_cut_info_text=True,
                 show_corr_folder_text=True,
                 # -- Plot1D args
                 show_data_mc_comparison_as=None,
                 colors_mc=None,
                 markers_data=None,
                 **kwargs):


        # run over a cross product of values for the following keys
        _iter_specs = [
            {
                "key": "selection",
                "values": selection_cuts
            },
        ]

        plot_class_kwargs = dict(
            sample_data=sample_data,
            sample_mc=sample_mc,
            quantity_x=self._get_quantity(quantity_x),
            quantities_y=[self._get_quantity(_qn) for _qn in quantities_y],
            y_label=y_label,
            y_range=y_range,
            jec_correction_string=jec_correction_string,
            show_cut_info_text=show_cut_info_text,
            show_corr_folder_text=show_corr_folder_text,
            # -- Plot1D args
            show_data_mc_comparison_as=show_data_mc_comparison_as,
            colors_mc=colors_mc,
            markers_data=markers_data,
            **kwargs
        )

        super(PlotStackProfiles, self).__init__(
            basename=basename,
            iter_specs=_iter_specs,
            plot_class_kwargs=plot_class_kwargs)


class PlotExtrapolations(_HistoMultiPlotterBase):
    _PLOT_CLASS = _PlotExtrapolation

    def __init__(self, 
                 sample_data, sample_mc, extrapolation_quantity, response_quantities, selection_cuts,
                 fit_function_range,
                 n_extrapolation_bins,
                 basename='extrapolation',
                 jec_correction_string='L1L2L3Res',
                 show_cut_info_text=True,
                 show_corr_folder_text=True,
                 # -- PlotExtrapolation args
                 additional_cut_dicts=None,
                 **kwargs):

        # run over a cross product of values for the following keys
        _iter_specs = [
            {
                "key": "selection",
                "values": selection_cuts
            },
        ]

        if additional_cut_dicts is not None:
            _iter_specs.append({
                    "key": "additional_cut_dict",
                    "values": additional_cut_dicts
                })
        else:
            kwargs['additional_cut_dict'] = None

        plot_class_kwargs = dict(
                 sample_data=sample_data,
                 sample_mc=sample_mc,
                 extrapolation_quantity=self._get_quantity(extrapolation_quantity),
                 response_quantities=[self._get_quantity(_qn) for _qn in response_quantities],
                 fit_function_range=fit_function_range,
                 n_extrapolation_bins=n_extrapolation_bins,
                 jec_correction_string=jec_correction_string,
                 **kwargs)

        super(PlotExtrapolations, self).__init__(
            basename=basename,
            iter_specs=_iter_specs,
            plot_class_kwargs=plot_class_kwargs)


def _test_plots():

    from Excalibur.JEC_Plotter.core import CutSet, QUANTITIES
    from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import SAMPLES, SELECTION_CUTS
    from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import SAMPLES as SAMPLES_2017
    from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import SELECTION_CUTS as SELECTION_CUTS_2017
    
    #from Excalibur.JEC_Plotter.utilities.plot import _flavor_fraction_cuts_miniAOD

    SAMPLES['Data_Zee_BCD_Summer16_JECV6']['color'] = 'darkred'
    SAMPLES['Data_Zee_EF_Summer16_JECV6']['color'] = 'royalblue'
    SAMPLES['Data_Zee_GH_Summer16_JECV6']['color'] = 'orange'

    _common_dict = dict(
        selection = SELECTION_CUTS["finalcuts"],
        plot_label = "Test Plot",
        jec_correction_string = "L1L2L3",
        upload_to_www=False
    )

    _plot1d = _Plot1D(
        basename="test_plot1d",
        quantity=QUANTITIES["jet1pt"],
        samples=[SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'], SAMPLES['Data_Zee_BCD_Summer16_JECV6'], SAMPLES['Data_Zee_EF_Summer16_JECV6'], SAMPLES['Data_Zee_GH_Summer16_JECV6']],
        cut_sets=[None],
        # -- Plot1D args
        normalize_to_first_histo=True,
        show_ratio_to_first=False,
        show_first_in_ratio=False,
        stacked=False,
        **_common_dict)


    _flavor_fraction_cuts_miniAOD = dict(
        u={
            'cut': CutSet(name='u',
                          weights=["abs(jet1flavor)==2"],
                          labels=[]),
            'label': r"u",
            'color': 'pink'
        },
        d={
            'cut': CutSet(name='d',
                          weights=["abs(jet1flavor)==1"],
                          labels=[]),
            'label': r"d",
            'color': 'darkred'
        },
        ud={
            'cut': CutSet(name='ud',
                          weights=["(abs(jet1flavor)==2||abs(jet1flavor)==1)"],
                          labels=[]),
            'label': r"ud",
            'color': 'red'
        },
        s={
            'cut': CutSet(name='s',
                          weights=["abs(jet1flavor)==3"],
                          labels=[]),
            'label': r"s",
            'color': 'green'
        },
        c={
            'cut': CutSet(name='c',
                          weights=["abs(jet1flavor)==4"],
                          labels=[]),
            'label': r"c",
            'color': 'violet'
        },
        b={
            'cut': CutSet(name='b',
                          weights=["abs(jet1flavor)==5"],
                          labels=[]),
            'label': r"b",
            'color': 'cornflowerblue'
        },
        g={
            'cut': CutSet(name='g',
                          weights=["abs(jet1flavor)==21"],
                          labels=[]),
            'label': r"g",
            'color': 'orange'
        },
        undef={
            'cut': CutSet(name='undef',
                          weights=["abs(jet1flavor)==0"],
                          labels=[]),
            'label': r"undef",
            'color': 'lightgray'
        },
    )

    _flavor_cut_sets = []
    _flavor_cut_set_colors = []
    _flavor_cut_set_labels = []
    for _flav in ('ud', 's', 'c', 'b', 'g', 'undef'):
        _flavor_cut_sets.append(_flavor_fraction_cuts_miniAOD[_flav]['cut'])
        _flavor_cut_set_colors.append(_flavor_fraction_cuts_miniAOD[_flav]['color'])
        _flavor_cut_set_labels.append(_flavor_fraction_cuts_miniAOD[_flav]['label'])

    _plot1dfrac = _Plot1DFractions(
        basename="test_plot1dfrac",
        quantity=QUANTITIES["jet1pt"],
        sample=SAMPLES_2017['MC_Zee_DYNJ_Fall17_JECV4'],
        cut_sets=_flavor_cut_sets,
        cut_set_labels=_flavor_cut_set_labels,
        cut_set_colors=_flavor_cut_set_colors,
        # -- Plot1DFraction args
        y_label="Flavor fraction",
        reference_cut_set=[None],
        selection = SELECTION_CUTS_2017["finalcuts"],
        plot_label = "Test Plot",
        jec_correction_string = "L1L2L3",
        upload_to_www=False
    )

    _plot2d = _Plot2D(
        # -- PlotBase args
        basename="test_plot2d",
        quantity_pair=(QUANTITIES["alpha"], QUANTITIES["ptbalance"]),
        sample=SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'],
        **_common_dict)


    _plotprof = _PlotProfile(
        basename="test_profile",
        quantity_pair=(QUANTITIES["zpt"], QUANTITIES["ptbalance"]),
        samples=[SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'], SAMPLES['Data_Zee_BCD_Summer16_JECV6'], SAMPLES['Data_Zee_EF_Summer16_JECV6'], SAMPLES['Data_Zee_GH_Summer16_JECV6']],
        cut_sets=None,
        # -- Plot1D args
        show_ratio_to_first=True,
        show_first_in_ratio=False,
        **_common_dict)

    _plotsp = _PlotStackProfile(
        basename="test_stackprofile",
        quantity_x=QUANTITIES['zpt'],
        quantities_y=[QUANTITIES['jet1chf'], QUANTITIES['jet1nhf']],
        sample_mc=SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'],
        sample_data=SAMPLES['Data_Zee_BCD_Summer16_JECV6'],
        y_label="My Y Label",
        y_range=None,
        # -- Plot1D args
        show_data_mc_comparison_as='percent',
        colors_mc=None,
        markers_data=None,
        **_common_dict)

    _plotex = _PlotExtrapolation(
        basename="test_extrapolation",
        extrapolation_quantity=QUANTITIES['alpha'],
        response_quantities=[QUANTITIES['ptbalance'], QUANTITIES['mpf']],
        sample_mc=SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'],
        sample_data=SAMPLES['Data_Zee_BCDEFGH_Summer16_JECV6'],
        cut_sets=None,
        n_extrapolation_bins=6,
        fit_function_range=(0.0, 0.3),
        # -- Plot1D args
        additional_cut_dict=None,
        **_common_dict)

    for _p in (_plot1d, _plot1dfrac, _plot2d, _plotprof, _plotsp, _plotex):
        _p.make_plot()

def _test_multiplots():

    from Excalibur.JEC_Plotter.core import CutSet, QUANTITIES
    from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import SAMPLES, SELECTION_CUTS
    from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import SAMPLES as SAMPLES_2017
    from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import SELECTION_CUTS as SELECTION_CUTS_2017
    
    #from Excalibur.JEC_Plotter.utilities.plot import _flavor_fraction_cuts_miniAOD

    SAMPLES['Data_Zee_BCD_Summer16_JECV6']['color'] = 'darkred'
    SAMPLES['Data_Zee_EF_Summer16_JECV6']['color'] = 'royalblue'
    SAMPLES['Data_Zee_GH_Summer16_JECV6']['color'] = 'orange'

    _common_dict = dict(
        selection_cuts = [SELECTION_CUTS["finalcuts"], SELECTION_CUTS["basiccuts"]],
        plot_label = "Test Plot",
        jec_correction_string = "L1L2L3",
        upload_to_www=False
    )

    _plot1d = PlotHistograms1D(
        basename="test_multi_plot1d",
        quantities=("jet1pt", "jet2pt"),
        samples=[SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'], SAMPLES['Data_Zee_BCD_Summer16_JECV6'], SAMPLES['Data_Zee_EF_Summer16_JECV6'], SAMPLES['Data_Zee_GH_Summer16_JECV6']],
        additional_cuts=[None],
        # -- Plot1D args
        normalize_to_first_histo=True,
        show_ratio_to_first=False,
        show_first_in_ratio=False,
        stacked=False,
        **_common_dict)


    _flavor_fraction_cuts_miniAOD = dict(
        u={
            'cut': CutSet(name='u',
                          weights=["abs(jet1flavor)==2"],
                          labels=[]),
            'label': r"u",
            'color': 'pink'
        },
        d={
            'cut': CutSet(name='d',
                          weights=["abs(jet1flavor)==1"],
                          labels=[]),
            'label': r"d",
            'color': 'darkred'
        },
        ud={
            'cut': CutSet(name='ud',
                          weights=["(abs(jet1flavor)==2||abs(jet1flavor)==1)"],
                          labels=[]),
            'label': r"ud",
            'color': 'red'
        },
        s={
            'cut': CutSet(name='s',
                          weights=["abs(jet1flavor)==3"],
                          labels=[]),
            'label': r"s",
            'color': 'green'
        },
        c={
            'cut': CutSet(name='c',
                          weights=["abs(jet1flavor)==4"],
                          labels=[]),
            'label': r"c",
            'color': 'violet'
        },
        b={
            'cut': CutSet(name='b',
                          weights=["abs(jet1flavor)==5"],
                          labels=[]),
            'label': r"b",
            'color': 'cornflowerblue'
        },
        g={
            'cut': CutSet(name='g',
                          weights=["abs(jet1flavor)==21"],
                          labels=[]),
            'label': r"g",
            'color': 'orange'
        },
        undef={
            'cut': CutSet(name='undef',
                          weights=["abs(jet1flavor)==0"],
                          labels=[]),
            'label': r"undef",
            'color': 'lightgray'
        },
    )

    _flavor_cut_sets = []
    _flavor_cut_set_colors = []
    _flavor_cut_set_labels = []
    for _flav in ('ud', 's', 'c', 'b', 'g', 'undef'):
        _flavor_cut_sets.append(_flavor_fraction_cuts_miniAOD[_flav]['cut'])
        _flavor_cut_set_colors.append(_flavor_fraction_cuts_miniAOD[_flav]['color'])
        _flavor_cut_set_labels.append(_flavor_fraction_cuts_miniAOD[_flav]['label'])

    _plot1dfrac = PlotHistograms1DFractions(
        basename="test_multi_plot1dfrac",
        quantities=("jet1pt", "jet2pt"),
        sample=SAMPLES_2017['MC_Zee_DYNJ_Fall17_JECV4'],
        fraction_cut_sets=_flavor_cut_sets,
        fraction_labels=_flavor_cut_set_labels,
        fraction_colors=_flavor_cut_set_colors,
        # -- Plot1DFraction args
        y_label="Flavor fraction",
        reference_cut_set=[None],
        selection = SELECTION_CUTS_2017["finalcuts"],
        plot_label = "Test Plot",
        jec_correction_string = "L1L2L3",
        upload_to_www=False
    )

    # _plot2d = PlotHistograms2D(
    #     # -- PlotBase args
    #     basename="test_multi_plot2d",
    #     quantity_pair=(QUANTITIES["alpha"], QUANTITIES["ptbalance"]),
    #     sample=SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'],
    #     **_common_dict)
    # 
    # 
    # _plotprof = PlotProfiles(
    #     basename="test_multi_profile",
    #     quantity_pair=(QUANTITIES["zpt"], QUANTITIES["ptbalance"]),
    #     samples=[SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'], SAMPLES['Data_Zee_BCD_Summer16_JECV6'], SAMPLES['Data_Zee_EF_Summer16_JECV6'], SAMPLES['Data_Zee_GH_Summer16_JECV6']],
    #     cut_sets=None,
    #     # -- Plot1D args
    #     show_ratio_to_first=True,
    #     show_first_in_ratio=False,
    #     **_common_dict)
    # 
    # _plotsp = PlotStackProfiles(
    #     basename="test_multi_stackprofile",
    #     quantity_x=QUANTITIES['zpt'],
    #     quantities_y=[QUANTITIES['jet1chf'], QUANTITIES['jet1nhf']],
    #     sample_mc=SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'],
    #     sample_data=SAMPLES['Data_Zee_BCD_Summer16_JECV6'],
    #     y_label="My Y Label",
    #     y_range=None,
    #     # -- Plot1D args
    #     show_data_mc_comparison_as='percent',
    #     colors_mc=None,
    #     markers_data=None,
    #     **_common_dict)
    # 
    # _plotex = PlotExtrapolations(
    #     basename="test_multi_extrapolation",
    #     extrapolation_quantity=QUANTITIES['alpha'],
    #     response_quantities=[QUANTITIES['ptbalance'], QUANTITIES['mpf']],
    #     sample_mc=SAMPLES['MC_Zee_DYNJ_Summer16_JECV6'],
    #     sample_data=SAMPLES['Data_Zee_BCDEFGH_Summer16_JECV6'],
    #     cut_sets=None,
    #     n_extrapolation_bins=6,
    #     fit_function_range=(0.0, 0.3),
    #     # -- Plot1D args
    #     additional_cut_dict=None,
    #     **_common_dict)

    #for _p in (_plot1d, _plot1dfrac, _plot2d, _plotprof, _plotsp, _plotex):
    for _p in (_plot1d, _plot1dfrac,):
        _p.make_plots()

if __name__ == "__main__":

    #_test_plots()
    _test_multiplots()

