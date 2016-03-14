# CMS Calibration with Excalibur

Performing Z+jet Calibration is a major use case of Excalibur. Aside from *skimming*, all steps are handled by the Excalibur software suite.

## Overview

The Jet Energy Corrections and Resolution [JERC] group uses *combination files* to compare their channels. These ROOT files contain jet responses in various eta and pt bins.

Most of what you need to create a combination file is covered by a standard Excalibur workflow. Simply process an up-to-date skim with a default Excalibur configuration (e.g. via `data15_25ns`). Then use Merlin and its `jec_combination` function to create the combination file.

## Tips and Hints

The Merlin function `jec_combination` has two wrappers which set defaults for Zee/Zmm channels: `jec_combination_zee` and `jec_combination_zmm`.

Always make sure that the following configuration entries are up to date: `JEC`, `JSON`

## Current commands

Process Zmm and Zee skims:

`$ for cfg in data15_25ns mc15_25ns data15_25ns_ee mc15_25ns_ee; do excalibur.py cfg _2015D -b; done`

Create combination files:

`$ merlin.py -i work/data15_25ns_2015D.root work/mc15_25ns_2015D.root --python jec_combination_zmm --www comb_Zmm`
`$ merlin.py -i work/data15_25ns_ee_2015D.root work/mc15_25ns_ee_2015D.root --python jec_combination_zee --www comb_Zmm`