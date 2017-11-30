JEC_Plotter
===========

The **JEC_Plotter** package is a set of tools designed to streamline
the production of plots for Jet Energy Calibration studies done with
**Excalibur**.

It is a thin layer above **Merlin**, a plotting tool which itself is
derived from the **HarryPlotter** submodule of the **Artus**
analysis framework.

# Directory structure

```
JEC_Plotter/
├── python/     (main package directory containing the Python code)
│   ├── core/           (submodule: core functionality)
│   │   ├── combination.py  (tools for generating combination files)
│   │   ├── plot.py         (tools for generating plots)
│   │   ├── quantities.py   (tools for representing ntuple quantities)
│   │   ├── sample.py       (tools for representing samples (=Excalibur output ROOT files))
│   │   ├── selection.py    (tools for representing the cuts/weights to apply to samples)
│   │   └── tools.py        (general-purpose functions)
│   │
│   ├── definitions/    (submodule: contains definitions of quantities, cuts, etc.)
│   │   └── <campaign_name>/    (e.g. `Summer16`)
│   │       ├── _common.py      (general definitions shared by all samples)
│   │       ├ ...
│   │       └── samples_<sample_name>.py    (sample-specific definitions)
│   │
│   └── utilities/      (submodule: functions which can be called by user scripts)
│       └── plot.py         (functions for common plotting tasks)
│
└── scripts/        (scripts to be called by users)
    ├ ...
    └── <campaign_name>/    (e.g. `Summer16`)
        ├ ...
        └── sample_<sample_name>/   (e.g. `sample_07Aug2017`)
            ├ ...
            └── <script>.py  (e.g. `plot_time_dependence.py`)
```

# Installing *JEC_Plotter*

**Note**: this should be done automatically when running `scram b` for
*Excalibur* in a new SCRAM environment. If `JEC_Plotter` is added to an
old SCRAM environment, SCRAM needs to be run again:

```
scram b python
```

To use `JEC_Plotter`, source the CMSSW/SCRAM environment as usual (`cmsenv`)
and then simply run the scripts in the `scripts/` directory, e.g.:

```
python scripts/Summer16/sample_07Aug2017/plot_time_dependence.py
```

This will create a `websync` subdirectory in your current working directory
containing the generated plots. If *Merlin*/*HarryPlotter* is configured
correctly, the plots will also be uploaded to your ETP webspace.


# Running *JEC_Plotter* plot scripts

To use `JEC_Plotter`, source the CMSSW/SCRAM environment as usual (`cmsenv`)
and then simply run the scripts in the `scripts/` directory, e.g.:

```
python scripts/Summer16/sample_07Aug2017/plot_time_dependence.py
```

This will create a `websync` subdirectory in your current working directory
containing the generated plots. If *Merlin*/*HarryPlotter* is configured
correctly, the plots will also be uploaded to your ETP webspace.

# Creating combination files

There should be a dedicated script for creating combination files for
each sample under `scripts/<campaign_name>/sample_<sample_name>/combination.py`

Running it will create a `plots` subdirectory in your current working directory
containing the combination file.
