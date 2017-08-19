Excalibur
=========

[![Build Status](https://travis-ci.org/KIT-CMS/Excalibur.svg)](https://travis-ci.org/KIT-CMS/Excalibur)

**Excalibur** is a high energy physics analysis tool for performing
studies using *Z+Jets* data recorded at the CMS experiment at CERN,
and in particular for deriving part of the residual corrections needed
for calibrating the jet energy scale. It is built on top of the event
data processing framework
[Artus](https://github.com/KIT-CMS/Artus "Artus Analysis").

This repository hosts the source code and configuration files for
*Excalibur* and the associated plotting tool, *Merlin*.

Please also have a look at the documentation for
[Artus](https://github.com/KIT-CMS/Artus/blob/master/README.md "Artus Readme")
and
[HarryPlotter](https://github.com/KIT-CMS/Artus/blob/master/HarryPlotter/README.md "HarryPlotter Readme").

The predecessor of this framework was also named *excalibur* and can be
found [here](https://ekptrac.ekp.kit.edu/trac/excalibur "excalibur")
(protected).


## Input Format

Both **Artus** and **Excalibur** make use of event data stored in
[ROOT](https://root.cern.ch/ "ROOT Data Analysis Framework") files.
These files contain event data extracted from CMS EDM data sets
by the [ĸappa](https://github.com/KIT-CMS/Kappa "Kappa") framework
in a process known as "skimming".

The format of Kappa ROOT files is different from that of the
original EDM formats (RECO, AOD, MINIAOD, etc.).
The interface for accessing the event data stored in these files
is defined in the
[ĸappa](https://github.com/KIT-CMS/Kappa "Kappa") and
[KappaTools](https://github.com/KIT-CMS/KappaTools "KappaTools")
packages.


# Installation Notes

The basic requirements for *Excalibur* are:

- GCC compiler (>= 4.8)
- ROOT (== 5.34)
- boost (>= 1.50)
- Python 2 (>= 2.6)

Although it can be installed as a standalone package, the most
convenient way of satisfying all dependencies is to set up a working
area of the CMS Software Framework
([CMSSW](https://github.com/cms-sw/cmssw "CMS Software Framework")).

Please refer to the 
[Wiki](https://github.com/KIT-CMS/Excalibur/wiki/Installation-notes-(CMSSW))
for a step-by-step guide to this process.


# Running *Excalibur*

Before running *Excalibur* in a new shell session, the file
`scripts/ini_excalibur.sh` must be sourced:
```
cd Excalibur
source scripts/ini_excalibur.sh
```

The main executable for running *Excalibur* is `excalibur.py`.
This is a Python wrapper around the executable generated from the C++
code which provides a flexible way of configuring *Excalibur* by
supplying a configuration file written in Python.

*Excalibur* can be run locally by providing the full path to a
Python configuration file:
```
excalibur.py /path/to/config.py
```

If the configuration file is located in the `cfg/excalibur`
subdirectory, then the filename can be used without providing the
full path, and the extension `.py` can be omitted as well. The following
commands are equivalent:
```
excalibur.py cfg/excalibur/example_config.py
excalibur.py example_config
```

To see a list of command line arguments and their description, run:
```
excalibur.py --help
```

Some useful arguments are:
- `-b`: run in batch mode. This parameter takes an optional argument
  specifying the computing resource use. See `-h`
- `-c`: only create config and exit
- `-f *n*`: only process the first `n` input files

# Further reading

For more information, please consult the
[Excalibur Wiki](https://github.com/KIT-CMS/Excalibur/wiki).
