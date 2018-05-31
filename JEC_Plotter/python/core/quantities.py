import numpy as np

from collections import OrderedDict
from copy import deepcopy

from selection import CutSet

__all__ = ['Quantity', "QUANTITIES"]

_N_BINS_DEFAULT = 50

DELTAR_FORMAT = "TMath::Sqrt(({a}eta-{b}eta)^2+TVector2::Phi_mpi_pi({a}phi-{b}phi)^2)"


class BinSpec(object):
    def __init__(self, bin_spec_string):
        self._string = bin_spec_string
        if ',' in self._string:
            self._type = "equidistant"
            _fields = self._string.split(',')
            assert len(_fields) == 3
            self._n_bins = int(_fields[0])
            self._range = float(_fields[1]), float(_fields[2])
            self._bin_edges = list(np.linspace(self._range[0], self._range[1], self._n_bins + 1))
        elif ' ' in self._string:
            self._type = "bin_edges"
            _fields = self._string.split(' ')
            assert len(_fields) > 1
            self._n_bins = len(_fields) - 1
            self._range = float(_fields[0]), float(_fields[-1])
            self._bin_edges = map(float, _fields)
        else:
            self._type = "named_binning"
            # TODO: get from Merlin/HarryPlotter?
            self._n_bins = None
            self._range = None
            self._bin_edges = None

    @classmethod
    def make_from_bin_edges(cls, bin_edges):
        """
        Create a non-equidistant binning from a sequence of bin edges.

        :param bin_edges: bin edges
        :type bin_edges: list/tuple of int/float
        :return: ``BinSpec`` object
        """
        _bin_edges_as_strings = map(str, bin_edges)
        _string = " ".join(_bin_edges_as_strings)
        return cls(bin_spec_string=_string)

    @classmethod
    def make_named(cls, binning_name):
        """
        Create a binning from a quantity name understood by Merlin/HarryPlotter.

        :param binning_name: name of the quantity with a default binning in Merlin/HarryPlotter
        :type binning_name: str
        :return:
        """
        return cls(bin_spec_string=binning_name)

    @classmethod
    def make_equidistant(cls, n_bins, range):
        """
        Create a binning from a number of bins and a numeric range.

        :param n_bins: number of bins
        :type n_bins: int
        :param range: numeric range
        :type range: tuple of 2 floats
        :return:
        """
        assert len(range) == 2
        _string = ",".join((str(int(n_bins)), str(range[0]), str(range[1])))
        return cls(bin_spec_string=_string)

    @property
    def n_bins(self):
        return self._n_bins

    @property
    def bin_edges(self):
        return self._bin_edges

    @property
    def range(self):
        return self._range

    @property
    def string(self):
        return self._string


class Quantity(object):
    def __init__(self, expression, bin_spec,
                 name=None, label=None, source_types=None, log_scale=False, channels=None):
        self.bin_spec = bin_spec
        self.name = name
        self._label = label
        self._expression = expression
        self.source_types = source_types
        self.log_scale = log_scale
        self.channels = channels

    @property
    def expression(self):
        return self._expression or self.name

    @expression.setter
    def expression(self, value):
        self._expression = value

    @property
    def label(self):
        return self._label or self.name

    @label.setter
    def label(self, value):
        self._label = value

    def available_for_source_type(self, source_type):
        if self.source_types is None or source_type in self.source_types:
            return True
        return False

    def available_for_channel(self, channel):
        if self.channels is None or channel in self.channels:
            return True
        return False

    def get_bin_spec_as_string(self):
        if self.bin_spec is None:
            return None
        return self.bin_spec.string

    def make_cutsets_from_binspec(self, bin_spec=None,
                                  include_underflow=False,
                                  include_overflow=False):
        if bin_spec is not None:
            _bs = bin_spec
        else:
            _bs = self.bin_spec

        _be = _bs.bin_edges

        _cs = []

        # underflow
        if include_underflow:
            _name = "{}_-inf_{:.2f}".format(self.name, _be[0])
            _ws = ["({})<{}".format(self.expression, _be[0])]
            _l = "{}$<${:.2f}".format(self.label, _be[0])
            _cs.append(
                CutSet(
                    name=_name,
                    weights=_ws,
                    labels=[_l]
                )
            )

        # regular bins
        for _be_lo, _be_hi in zip(_be[:-1], _be[1:]):
            _name = "{}_{:.2f}_{:.2f}".format(self.name, _be_lo, _be_hi)
            _ws = ["{}<=({})".format(_be_lo, self.expression),
                   "({})<{}".format(self.expression, _be_hi)]
            _l = r"{:.2f}$\\leq${}$<${:.2f}".format(_be_lo, self.label, _be_hi)
            _cs.append(
                CutSet(
                    name=_name,
                    weights=_ws,
                    labels=[_l]
                )
            )

        # overflow
        if include_overflow:
            _name = "{}_{:.2f}_inf".format(self.name, _be[-1])
            _ws = ["{}<=({})".format( _be[-1], self.expression)]
            _l = "{}$\\geq${:.2f}".format(self.label, _be[-1])
            _cs.append(
                CutSet(
                    name=_name,
                    weights=_ws,
                    labels=[_l]
                )
            )

        return _cs

# -- plottable quantities

# special BinSpecs

_binspec_abseta_narrow = BinSpec.make_from_bin_edges(
    [0.000, 0.261, 0.522, 0.783, 1.044, 1.305, 1.479, 1.653, 1.930, 2.172, 2.322, 2.500,
     2.650, 2.853, 2.964, 3.139, 3.489, 3.839, 5.191])
_binspec_eta_narrow = BinSpec.make_from_bin_edges(
    [-5.191, -3.839, -3.489, -3.139, -2.964, -2.853, -2.650, -2.500, -2.322, -2.172,
     -1.930, -1.653, -1.479, -1.305, -1.044, -0.783, -0.522, -0.261, 0.000, 0.261, 0.522,
     0.783, 1.044, 1.305, 1.479, 1.653, 1.930, 2.172, 2.322, 2.500, 2.650, 2.853, 2.964,
     3.139, 3.489, 3.839, 5.191])
_binspec_abseta_wide = BinSpec.make_from_bin_edges(
    [0.000, 1.305, 2.172, 2.500, 3.139, 5.191])
_binspec_eta_wide = BinSpec.make_from_bin_edges(
    [-5.191, -3.139, -2.500, -2.172, -1.305, 0.000, 1.305, 2.172, 2.500, 3.139, 5.191])


QUANTITIES = dict(
    alpha=Quantity(
        name='alpha',
        expression='alpha',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 0.5))
    ),
    e1eta=Quantity(
        name='e1eta',
        expression='e1eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        channels=['Zee']
    ),
    e1iso=Quantity(
        name='e1iso',
        expression='e1iso',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 2)),
        channels=['Zee']
    ),
    e1pt=Quantity(
        name='e1pt',
        expression='e1pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        channels=['Zee']
    ),
    e2pt=Quantity(
        name='e2pt',
        expression='e2pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        channels=['Zee']
    ),
    eminusiso=Quantity(
        name='eminusiso',
        expression='eminusiso',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 2)),
        channels=['Zee']
    ),
    eplusiso=Quantity(
        name='eplusiso',
        expression='eplusiso',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 2)),
        channels=['Zee']
    ),
    eminuspt=Quantity(
        name='eminuspt',
        expression='eminuspt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        channels=['Zee']
    ),
    epluspt=Quantity(
        name='epluspt',
        expression='epluspt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        channels=['Zee']
    ),
    eminuseta=Quantity(
        name='eminuseta',
        expression='eminuseta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-2.5, 2.5)),
        channels=['Zee']
    ),
    epluseta=Quantity(
        name='epluseta',
        expression='epluseta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-2.5, 2.5)),
        channels=['Zee']
    ),
    genjet1eta=Quantity(
        name='genjet1eta',
        expression='genjet1eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        label='$\\\\eta^\\\\mathrm{GenJet1}$',
        source_types=['MC']
    ),
    genjet1pt=Quantity(
        name='genjet1pt',
        expression='genjet1pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 250)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{GenJet1}~/~GeV$',
        source_types=['MC']
    ),
    genjet2eta=Quantity(
        name='genjet2eta',
        expression='genjet2eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        label='$\\\\eta^\\\\mathrm{GenJet2}$',
        source_types=['MC']
    ),
    genjet2pt=Quantity(
        name='genjet2pt',
        expression='genjet2pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 50)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{GenJet2}~/~GeV$',
        source_types=['MC']
    ),
    jet1area=Quantity(
        name='jet1area',
        expression='jet1area',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0.3, 0.7))
    ),
    jet1chf=Quantity(
        name='jet1chf',
        expression='jet1chf',
        bin_spec=BinSpec.make_equidistant(n_bins=30, range=(0, 1)),
        label='PF charged hadron fraction (Jet 1)',
    ),
    jet1ef=Quantity(
        name='jet1ef',
        expression='jet1ef',
        bin_spec=BinSpec.make_equidistant(n_bins=30, range=(0, 1)),
        label='PF electron fraction (Jet 1)',
    ),
    jet1eta=Quantity(
        name='jet1eta',
        expression='jet1eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        label='$\\\\eta^\\\\mathrm{Jet1}$'
    ),
    jet1eta_extended=Quantity(
        name='jet1eta_extended',
        expression='jet1eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-9, 9)),
        label='$\\\\eta^\\\\mathrm{Jet1}$'
    ),
    jet1hfem=Quantity(
        name='jet1hfem',
        expression='jet1hfem',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 1)),
        label='PF HF em fraction (Jet 1)',
    ),
    jet1hfhf=Quantity(
        name='jet1hfhf',
        expression='jet1hfhf',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 1)),
        label='PF HF hadronic fraction (Jet 1)',
    ),
    jet1mf=Quantity(
        name='jet1mf',
        expression='jet1mf',
        bin_spec=BinSpec.make_equidistant(n_bins=30, range=(0, 1)),
        label='PF muon fraction (Jet 1)',
    ),
    jet1nhf=Quantity(
        name='jet1nhf',
        expression='jet1nhf',
        bin_spec=BinSpec.make_equidistant(n_bins=30, range=(0, 1)),
        label='PF neutral hadron fraction (Jet 1)',
    ),
    jet1pf=Quantity(
        name='jet1pf',
        expression='jet1pf',
        bin_spec=BinSpec.make_equidistant(n_bins=30, range=(0, 1)),
        label='PF photon fraction (Jet 1)',
    ),
    jet1phi=Quantity(
        name='jet1phi',
        expression='jet1phi',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-4, 4))
    ),
    jet1pt=Quantity(
        name='jet1pt',
        expression='jet1pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 250)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet1}~/~GeV$'
    ),
    jet1pt_log=Quantity(
        name='jet1pt_log',
        expression='jet1pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 250)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet1}~/~GeV$',
        log_scale=True,
    ),
    jet1pt_extended=Quantity(
        name='jet1pt_extended',
        expression='jet1pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 700)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet1}~/~GeV$'
    ),
    jet1pt_extended_log=Quantity(
        name='jet1pt_extended_log',
        expression='jet1pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 700)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet1}~/~GeV$',
        log_scale=True
    ),
    jet1ptl1=Quantity(
        name='jet1ptl1',
        expression='jet1ptl1',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 250))
    ),
    jet1pt_over_jet1ptraw=Quantity(
        name='jet1pt_over_jet1ptraw',
        expression='jet1pt/jet1ptraw',
        label=r"$p_\\mathrm{T}^\\mathrm{Jet1, corr}/p_\\mathrm{T}^\\mathrm{Jet1, raw}$",
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0.95, 1.25))
    ),
    jet1res=Quantity(
        name='jet1res',
        expression='jet1res',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0., 2.))
    ),
    jet2eta=Quantity(
        name='jet2eta',
        expression='jet2eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        label='$\\\\eta^\\\\mathrm{Jet2}$'
    ),
    jet2eta_extended=Quantity(
        name='jet2eta_extended',
        expression='jet2eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-9, 9)),
        label='$\\\\eta^\\\\mathrm{Jet2}$'
    ),
    jet2phi=Quantity(
        name='jet2phi',
        expression='jet2phi',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-4, 4))
    ),
    jet2pt=Quantity(
        name='jet2pt',
        expression='jet2pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 50)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet2}~/~GeV$'
    ),
    jet2pt_extended=Quantity(
        name='jet2pt_extended',
        expression='jet2pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 150)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet2}~/~GeV$'
    ),
    jet2pt_extended_log=Quantity(
        name='jet2pt_extended_log',
        expression='jet2pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 150)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet2}~/~GeV$',
        log_scale=True
    ),
    jet2pt_over_jet1pt=Quantity(
        name='jet2pt_over_jet1pt',
        expression='jet2pt/jet1pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 1)),
        label='jet1pt/jet2pt'
    ),
    jet3eta=Quantity(
        name='jet3eta',
        expression='jet3eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        label='$\\\\eta^\\\\mathrm{Jet3}$'
    ),
    jet3eta_extended=Quantity(
        name='jet3eta_extended',
        expression='jet3eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-9, 9)),
        label='$\\\\eta^\\\\mathrm{Jet3}$'
    ),
    jet3phi=Quantity(
        name='jet3phi',
        expression='jet3phi',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-4, 4)),
        label='$\\\\phi^\\\\mathrm{Jet3}$'
    ),
    jet3pt=Quantity(
        name='jet3pt',
        expression='jet3pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 50)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet3}~/~GeV$'
    ),
    jet3pt_extended=Quantity(
        name='jet3pt_extended',
        expression='jet3pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet3}~/~GeV$'
    ),
    jet3pt_extended_log=Quantity(
        name='jet3pt_extended_log',
        expression='jet3pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{Jet3}~/~GeV$',
        log_scale=True
    ),
    jetHT=Quantity(
        name='jetHT',
        expression='jetHT',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 0.5))
    ),
    jetrpf=Quantity(
        name='jetrpf',
        expression='jetrpf',
        label="Jet RPF",
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 2))
    ),
    matchedgenjet1eta=Quantity(
        name='matchedgenjet1eta',
        expression='matchedgenjet1eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        label='$\\\\eta^\\\\mathrm{MatchedGenJet1}$',
        source_types=['MC']
    ),
    matchedgenjet1pt=Quantity(
        name='matchedgenjet1pt',
        expression='matchedgenjet1pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 250)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{MatchedGenJet1}~/~GeV$',
        source_types=['MC']
    ),
    matchedgenjet2eta=Quantity(
        name='matchedgenjet2eta',
        expression='matchedgenjet2eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        label='$\\\\eta^\\\\mathrm{MatchedGenJet2}$',
        source_types=['MC']
    ),
    matchedgenjet2pt=Quantity(
        name='matchedgenjet2pt',
        expression='matchedgenjet2pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 50)),
        label='$p_\\\\mathrm{T}^\\\\mathrm{MatchedGenJet2}~/~GeV$',
        source_types=['MC']
    ),
    met=Quantity(
        name='met',
        expression='met',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100))
    ),
    metphi=Quantity(
        name='metphi',
        expression='metphi',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-4, 4))
    ),
    mpf=Quantity(
        name='mpf',
        expression='mpf',
        label="MPF",
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 2))
    ),
    mu1eta=Quantity(
        name='mu1eta',
        expression='mu1eta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        channels=['Zmm']
    ),
    mu1iso=Quantity(
        name='mu1iso',
        expression='mu1iso',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 2)),
        channels=['Zmm']
    ),
    mu1pt=Quantity(
        name='mu1pt',
        expression='mu1pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        channels=['Zmm']
    ),
    mu2pt=Quantity(
        name='mu2pt',
        expression='mu2pt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        channels=['Zmm']
    ),
    muminusiso=Quantity(
        name='muminusiso',
        expression='muminusiso',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 2)),
        channels=['Zmm']
    ),
    muplusiso=Quantity(
        name='muplusiso',
        expression='muplusiso',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 2)),
        channels=['Zmm']
    ),
    muminuspt=Quantity(
        name='muminuspt',
        expression='muminuspt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        channels=['Zmm']
    ),
    mupluspt=Quantity(
        name='mupluspt',
        expression='mupluspt',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 100)),
        channels=['Zmm']
    ),
    muminuseta=Quantity(
        name='muminuseta',
        expression='muminuseta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-2.5, 2.5)),
        channels=['Zmm']
    ),
    mupluseta=Quantity(
        name='mupluseta',
        expression='mupluseta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-2.5, 2.5)),
        channels=['Zmm']
    ),
    njets=Quantity(
        name='njets',
        expression='njets',
        bin_spec=BinSpec.make_equidistant(n_bins=161, range=(-0.5, 160.5)),
        label='# of jets'
    ),
    njets10=Quantity(
        name='njets10',
        expression='njets10',
        bin_spec=BinSpec.make_equidistant(n_bins=31, range=(-0.5, 30.5)),
        label='# of jets with $p_T>10$ GeV'
    ),
    njets10_log=Quantity(
        name='njets10_log',
        expression='njets10',
        bin_spec=BinSpec.make_equidistant(n_bins=31, range=(-0.5, 30.5)),
        label='# of jets with $p_T>10$ GeV',
        log_scale=True
    ),
    njets30=Quantity(
        name='njets30',
        expression='njets30',
        bin_spec=BinSpec.make_equidistant(n_bins=6, range=(-0.5, 5.5)),
        label='# of jets with $p_T>30$ GeV'
    ),
    njets30_log=Quantity(
        name='njets30_log',
        expression='njets30',
        bin_spec=BinSpec.make_equidistant(n_bins=6, range=(-0.5, 5.5)),
        label='# of jets with $p_T>30$ GeV',
        log_scale=True
    ),
    njets_log=Quantity(
        name='njets_log',
        expression='njets',
        bin_spec=BinSpec.make_equidistant(n_bins=161, range=(-0.5, 160.5)),
        label='# of jets'
    ),
    npu=Quantity(
        name='npu',
        expression='npu',
        bin_spec=BinSpec.make_equidistant(n_bins=61, range=(-0.5, 60.5)),
        source_types=['MC']
    ),
    npu_log=Quantity(
        name='npu_log',
        expression='npu',
        bin_spec=BinSpec.make_equidistant(n_bins=61, range=(-0.5, 60.5)),
        source_types=['MC'],
        log_scale=True
    ),
    npumean=Quantity(
        name='npumean',
        expression='npumean',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 60)),
        source_types=['MC']
    ),
    npumean_log=Quantity(
        name='npumean_log',
        expression='npumean',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 60)),
        source_types=['MC'],
        log_scale=True
    ),
    npv=Quantity(
        name='npv',
        expression='npv',
        bin_spec=BinSpec.make_equidistant(n_bins=61, range=(-0.5, 60.5))
    ),
    npv_log=Quantity(
        name='npv_log',
        expression='npv',
        bin_spec=BinSpec.make_equidistant(n_bins=61, range=(-0.5, 60.5)),
        log_scale=True
    ),
    ptbalance=Quantity(
        name='ptbalance',
        expression='ptbalance',
        label='$p_\\\\mathrm{T}$ balance',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 2))
    ),
    rho=Quantity(
        name='rho',
        expression='rho',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(0, 50))
    ),
    run=Quantity(
        name='run',
        expression='run',
        bin_spec=BinSpec.make_equidistant(n_bins=120, range=(272007, 284044))
    ),
    run2017=Quantity(
        name='run2017',
        label='Run number',
        expression='run',
        bin_spec=BinSpec.make_equidistant(n_bins=120, range=(297020, 306462))
    ),
    runBCD=Quantity(
        name='runBCD',
        expression='run',
        bin_spec=BinSpec.make_equidistant(n_bins=48, range=(272007, 276811))
    ),
    zeta=Quantity(
        name='zeta',
        expression='zeta',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-5, 5)),
        label='$\\\\eta^\\\\mathrm{Z}$'
    ),
    zphi=Quantity(
        name='zphi',
        expression='zphi',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(-4, 4))
    ),
    zmass=Quantity(
        name='zmass',
        expression='zmass',
        label='$m_\\\\mathrm{Z}$ / GeV',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(70, 110))
    ),
    zpt=Quantity(
        name='zpt',
        expression='zpt',
        label='$p_\\\\mathrm{T}^\\\\mathrm{Z}$ / GeV',
        bin_spec=BinSpec.make_from_bin_edges(
            bin_edges=(30, 40, 50, 60, 85, 105, 130, 175, 230, 300, 400, 500, 700, 1000, 1500)
        )
    ),
    zpt_log=Quantity(
        name='zpt_log',
        expression='zpt',
        label='$p_\\\\mathrm{T}^\\\\mathrm{Z}$ / GeV',
        bin_spec=BinSpec.make_from_bin_edges(
            bin_edges=(30, 40, 50, 60, 85, 105, 130, 175, 230, 300, 400, 500, 700, 1000, 1500)
        ),
        log_scale=True
    ),
    zpt_low=Quantity(
        name='zpt_low',
        expression='zpt',
        label='$p_\\\\mathrm{T}^\\\\mathrm{Z}$ / GeV',
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT, range=(15, 80))
    ),
    # -- absolute values
    absjet1eta=Quantity(
        name='absjet1eta',
        expression='abs(jet1eta)',
        label=r"$|\\eta^{Jet1}|$",
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT/2, range=(0, 5)),
    ),
    absjet2eta=Quantity(
        name='absjet2eta',
        expression='abs(jet2eta)',
        label=r"$|\\eta^{Jet2}|$",
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT/2, range=(0, 5)),
    ),
    absjet3eta=Quantity(
        name='absjet3eta',
        expression='abs(jet3eta)',
        label=r"$|\\eta^{Jet3}|$",
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT/2, range=(0, 5)),
    ),
    abszeta=Quantity(
        name='abszeta',
        expression='abs(zeta)',
        label=r"$|\\eta^{Z}|$",
        bin_spec=BinSpec.make_equidistant(n_bins=_N_BINS_DEFAULT/2, range=(0, 5)),
    )
)

# narrow eta binnings
for _qn in ('jet1eta', 'zeta', 'absjet1eta', 'abszeta'):
    _q_orig = QUANTITIES[_qn]
    _qn_narrow = "{}_narrow".format(_qn)

    QUANTITIES[_qn_narrow] = deepcopy(_q_orig)
    QUANTITIES[_qn_narrow].name = _qn_narrow

    if _qn.startswith('abs'):
        QUANTITIES[_qn_narrow].bin_spec = _binspec_abseta_narrow
    else:
        QUANTITIES[_qn_narrow].bin_spec = _binspec_eta_narrow

# wide eta binnings
for _qn in ('jet1eta', 'zeta', 'absjet1eta', 'abszeta'):
    _q_orig = QUANTITIES[_qn]
    _qn_wide = "{}_wide".format(_qn)

    QUANTITIES[_qn_wide] = deepcopy(_q_orig)
    QUANTITIES[_qn_wide].name = _qn_wide

    if _qn.startswith('abs'):
        QUANTITIES[_qn_wide].bin_spec = _binspec_abseta_wide
    else:
        QUANTITIES[_qn_wide].bin_spec = _binspec_eta_wide

# --------------------------------------------------------------

_obj_dicts = OrderedDict(
    jet1={
        "label": "Jet1",
    },
    jet2={
        "label": "Jet2",
    },
    jet3={
        "label": "Jet3",
    },
    z={
        "label": "Z",
    },
    mu1={
        "label": r"\\mu_1",
        "channels": ["Zmm"]
    },
    mu2={
        "label": "\\mu_2",
        "channels": ["Zmm"]
    },
    e1={
        "label": "e_1",
        "channels": ["Zee"]
    },
    e2={
        "label": "e_2",
        "channels": ["Zee"]
    },

    #
    genjet1={
        "label": "GenJet1",
        "source_types": ["MC"]
    },
    genjet2={
        "label": "GenJet2",
        "source_types": ["MC"]
    },
    matchedgenjet1={
        "label": "MatchedGenJet1",
        "source_types": ["MC"]
    },
    matchedgenjet2={
        "label": "MatchedGenJet2",
        "source_types": ["MC"]
    },
)


# --

_delta_expr_dicts = {
    "deltaPhi" : {
        "label": r"\\Delta \\phi",
        "expr_lambda": lambda a, b: "TVector2::Phi_mpi_pi({a}phi-{b}phi)".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "-3.14159", "3.14159")
    },
    "absDeltaPhi" : {
        "label": r"|\\Delta \\phi|",
        "expr_lambda": lambda a, b: "abs(TVector2::Phi_mpi_pi({a}phi-{b}phi))".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0", "3.14159")
    },
    "absDeltaPhi_aroundPi" : {
        "label": r"|\\Delta \\phi|",
        "expr_lambda": lambda a, b: "abs(TVector2::Phi_mpi_pi({a}phi-{b}phi))".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "2.74159", "3.14159")
    },
    "absDeltaPhi_fine" : {  # fine binning
        "label": r"|\\Delta \\phi|",
        "expr_lambda": lambda a, b: "abs(TVector2::Phi_mpi_pi({a}phi-{b}phi))".format(a=a, b=b),
        "bins": ("250", "0", "3.14159")
    },
    "absDeltaPhi_aroundPi_fine" : {  # fine binning
        "label": r"|\\Delta \\phi|",
        "expr_lambda": lambda a, b: "abs(TVector2::Phi_mpi_pi({a}phi-{b}phi))".format(a=a, b=b),
        "bins": ("250", "2.74159", "3.14159")
    },
    "deltaEta" : {
        "label": r"\\Delta \\eta",
        "expr_lambda": lambda a, b: "{a}eta-{b}eta".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "-10", "10")
    },
    "absDeltaEta" : {
        "label": r"|\\Delta \\eta|",
        "expr_lambda": lambda a, b: "abs({a}eta-{b}eta)".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0", "10")
    },
    "deltaR" : {
        "label": r"\\Delta R",
        "expr_lambda": lambda a, b: DELTAR_FORMAT.format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0", "10")
    },
    "deltaR_aroundZero" : {
        "label": r"\\Delta R",
        "expr_lambda": lambda a, b: DELTAR_FORMAT.format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0", "0.1")
    },
    "deltaR_upToOne" : {
        "label": r"\\Delta R",
        "expr_lambda": lambda a, b: DELTAR_FORMAT.format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0", "1.0")
    },
    "deltaPtRel" : {
        "label": r"\\Delta p_{\\mathrm{T}}/p_{\\mathrm{T}}",
        "expr_lambda": lambda a, b: "({a}pt-{b}pt)/{a}pt".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0", "1")
    },
    "pTAsymmetry" : {
        "label": r"A_{p,\\mathrm{T}}",
        "expr_lambda": lambda a, b: "({a}pt-{b}pt)/({a}pt+{b}pt)".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0", "1")
    },
    "pTRatio" : {
        "label": r"Ratio_{p,\\mathrm{T}}",
        "expr_lambda": lambda a, b: "{a}pt/{b}pt".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0", "10")
    },
    "pTRatio_aroundOne" : {
        "label": r"Ratio_{p,\\mathrm{T}}",
        "expr_lambda": lambda a, b: "{a}pt/{b}pt".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0.5", "3")
    },
    "sumEta" : {
        "label": r"\\Sigma \\eta",
        "expr_lambda": lambda a, b: "{a}eta+{b}eta".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "-10", "10")
    },
    "absSumEta" : {
        "label": r"|\\Sigma \\eta|",
        "expr_lambda": lambda a, b: "abs({a}eta+{b}eta)".format(a=a, b=b),
        "bins": (_N_BINS_DEFAULT, "0", "10")
    },
}

for _obj1, _obj1_dict in _obj_dicts.iteritems():
    for _obj2, _obj2_dict in _obj_dicts.iteritems():
        if _obj1 == _obj2:
            continue

        _channels_1 = _obj1_dict.get("channels", None)
        _channels_2 = _obj2_dict.get("channels", None)

        if _channels_1 is None and _channels_2 is None:
            _channels = None
        elif _channels_1 is None and _channels_2 is not None:
            _channels =  set(_channels_2)
        elif _channels_1 is not None and _channels_2 is None:
            _channels =  set(_channels_1)
        else:
            _channels =  set(_channels_1).intersection(set(_channels_2))

        _source_types_1 = _obj1_dict.get("source_types", None)
        _source_types_2 = _obj2_dict.get("source_types", None)

        if _source_types_1 is None and _source_types_2 is None:
            _source_types = None
        elif _source_types_1 is None and _source_types_2 is not None:
            _source_types =  set(_source_types_2)
        elif _source_types_1 is not None and _source_types_2 is None:
            _source_types =  set(_source_types_1)
        else:
            _source_types =  set(_source_types_1).intersection(set(_source_types_2))

        for _delta_expr, _delta_expr_dict in _delta_expr_dicts.iteritems():
            _key = r"{}_{}_{}".format(_delta_expr, _obj1, _obj2)
            _label = r"${}({},{})$".format(_delta_expr_dict['label'], _obj1_dict['label'], _obj2_dict['label'])
            _kwargs = {}
            if _channels:
                _kwargs['channels'] = list(_channels)
            if _source_types:
                _kwargs['source_types'] = list(_source_types)
            QUANTITIES[_key] = Quantity(
                expression=_delta_expr_dict['expr_lambda'](_obj1, _obj2),
                label=_label,
                bin_spec=_delta_expr_dict['bins'],
                **_kwargs
            )


# manual tweaks
QUANTITIES['deltaEta_matchedgenjet1_jet1'].bin_spec = (_N_BINS_DEFAULT, "-1", "1")
QUANTITIES['deltaEta_matchedgenjet2_jet2'].bin_spec = (_N_BINS_DEFAULT, "-1", "1")
