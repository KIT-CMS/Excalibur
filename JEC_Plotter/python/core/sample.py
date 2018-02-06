import os
import re

__all__ = ['Sample', 'SAMPLE_FILENAME_CONVENTIONS']

SAMPLE_SOURCE_COLOR_MAP = {
        'BCD': 'red',
        'EF': 'blue',
        'G': 'green',
        'H': 'orange',
        'amc': 'magenta',
        'madgraph': 'k',
        'madgraph_1J': 'k',
        'madgraph_2J': 'k',
        'madgraph_3J': 'k',
        'madgraph_4J': 'k',
        'madgraph_NJ': 'k',
        'DYJets_Madgraph': 'k',
    }

SAMPLE_FILENAME_CONVENTIONS = {
        "data([0-9]+)_([^_]+)_([^_]+)_([^.]+).root": {
                'source_type': 'Data',
                'channel': lambda e, s: 'Z'+e.match(s).groups()[1],
                'source_label': lambda e, s: e.match(s).groups()[2],
                'color': lambda e, s: SAMPLE_SOURCE_COLOR_MAP.get(e.match(s).groups()[2], None),
                'marker': '_',
                'step_flag': True
        },
        "mc([0-9]+)_([^_]+)_[BCDEFGH]+_([^.]+).root": {
                'source_type': 'MC',
                'channel': lambda e, s: 'Z'+e.match(s).groups()[1],
                'source_label': lambda e, s: e.match(s).groups()[2],
                'color': lambda e, s: SAMPLE_SOURCE_COLOR_MAP.get(e.match(s).groups()[2], None),
                'marker': '_',
                'step_flag': True
        },
    }

class Sample(object):
    """one sample = one Excalibur output root file"""
    def __init__(self, name, source_file_path):
        self._name = name

        self._filepath = source_file_path
        if not os.path.exists(self._filepath):
            raise IOError("File not found: '%s'" % (self._filepath,))
        self._filepath = os.path.realpath(self._filepath)

        self._dict = {}

    @classmethod
    def load_using_convention(cls, sample_dir, sample_file, convention=None):
        _dirname = sample_dir
        _filename = sample_file

        _basename = ".".join(sample_file.split('.')[0])
        _fullname = "__".join([sample_dir, _basename])

        _filepath = os.path.join(_dirname, _filename)
        self = cls(name=_fullname, source_file_path=_filepath)

        _conventions = [convention]
        if convention is None:
            _conventions = SAMPLE_FILENAME_CONVENTIONS

        for _fc_name, _fc in _conventions.iteritems():
            _regex = re.compile(_fc_name)
            _m = _regex.match(_filename)
            if _m is None:
                # print "No match for convention '{}'".format(_fc_name)
                continue
            self['file'] = self._filepath
            self['channel'] = _fc['channel'](_regex, _filename)
            self['source_label'] = _fc['source_label'](_regex, _filename)
            self['source_type'] = _fc['source_type']
            self['color'] = _fc['color'](_regex, _filename)
            self['marker'] = _fc['marker']
            self['step_flag'] = _fc['step_flag']

        if not self._dict:
            raise Exception("Cannot parse source file name ('%s') using any convention!" % (_filename,))

        return self

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

if __name__ == "__main__":
    _SAMPLE_DIR = "_mock/sample_root/Summer16_07Aug2017_V1_2017-11-13"

    _s1 = Sample.load_using_convention('Summer16_07Aug2017_V1_2017-11-13_Data',
                                       os.path.join(_SAMPLE_DIR, "data16_mm_BCDEFGH_DoMuLegacy.root"))

    for k, v in _s1._dict.iteritems():
        print "{}: {}".format(k, v)

    print '\n'

    _s2 = Sample.load_using_convention('Summer16_07Aug2017_V1_2017-11-13_MC',
                                       os.path.join(_SAMPLE_DIR, "mc16_mm_BCDEFGH_DYJets_Madgraph.root"))

    for k, v in _s2._dict.iteritems():
        print "{}: {}".format(k, v)
