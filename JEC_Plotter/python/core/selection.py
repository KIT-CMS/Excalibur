import numpy as np


class CutSet(object):
    def __init__(self, name, weights, labels, zjet_folder=None):
        self._name = name
        self._w = weights
        self._texts = labels
        self._zjet_folder = zjet_folder

    def _get_common_zjf_or_throw(self, other):
        print ("Added cuts '{}' and '{}' together. "
                         "'zjet_folder' : '{}' + "
                         "'{}' = ...".format(self._name, other._name, self._zjet_folder, other._zjet_folder))
        if self._zjet_folder is None:
            return other._zjet_folder
        elif other._zjet_folder is None:
            return self._zjet_folder
        elif self._zjet_folder == other._zjet_folder:
            return self._zjet_folder
        else:
            raise ValueError("Added cuts '{}' and '{}' together, but "
                             "'zjet_folder' differs: '{}' vs "
                             "'{}'".format(self._name, other._name,
                                           self._zjet_folder, other._zjet_folder))


    def __iadd__(self, other):
         self._name += "_" + other._name
         self._w += other._w
         self._texts += other._texts
         self._zjet_folder = self._get_common_zjf_or_throw(other)
         return self

    def __add__(self, other):
        _cs = CutSet('_'.join([self._name, other._name]),
                     self._w + other._w,
                     self._texts + other._texts,
                     self._get_common_zjf_or_throw(other)
        )
        return _cs

    def inverted(self):
        _inv_w = ["(1.0-({}))".format(_w) for _w in self._w]
        _inv_w = ["({})".format("||".join(_inv_w))]

        _inv_t = ["!{}".format(_t) for _t in self._texts]
        _cs = CutSet(name='~' + self._name,
                     weights=_inv_w,
                     labels=_inv_t,
                     zjet_folder=self._zjet_folder
        )
        return _cs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def weights_string(self):
        return "&&".join(self._w)

    @property
    def weights_list(self):
        return self._w

    @property
    def texts(self):
        return self._texts

    @property
    def zjet_folder(self):
        return self._zjet_folder

    @property
    def plot_dict(self):
        _dct = dict(weights=self.weights_string, texts=self._texts)
        if self._zjet_folder is not None:
            _dct['zjetfolders'] = [self._zjet_folder]
        else:
            print "WARNING: no zjetfolder for cut {}".format(self._name)
        return _dct


def btb_cut_factory(cutoff=0.34):
    _name_str = "btb{:03d}".format(int(100*cutoff))
    _label_str =  r"$||\\phi^\\mathrm{Jet1}-\\phi^\\mathrm{Z}|-\\pi| < %f" % (cutoff,)
    _weight_str = "abs(abs({a}phi-{b}phi)-{pi:7.6f})<0.05".format(a='jet1',
                                                                  b='z',
                                                                  pi=np.pi)
    return CutSet(_name_str, weights=[_weight_str], labels=[_label_str])