#!/usr/bin/env python

"""Easy looking at rootfiles

This opens root files and starts the TBrowser automatically.
In addition it provides some objects to look at:
- f is the first file
- files is a list of all open files
- t is the Branch called "Events" if it is available (as in our skims)
    or the Branch called "ntuple" if it is available (as in some ntuples)
- l is the Branch called "Lumis" if it is available (as in our skims)

A handy function is t.Draw(quantity, [cuts])
"""

import ROOT
import sys

# open files
ROOT.gSystem.Load('libKappa')
files = [ROOT.TFile(i) for i in sys.argv[1:]]
f = files[0]

print __doc__

# get most common trees if available
l = f.Get("Lumis")
t = f.Get("Events")
if not t: t = f.Get("ntuple")
if not t: t = f.Get("gen/ntuple")
# you can add more here ...
# delete variables that are None
if t:
	print "t is %r (%s)" % (t.GetName(), t.ClassName())
else:
	del t
if l:
	print "l is %r (%s)" % (l.GetName(), l.ClassName())
else:
	del l

tb = ROOT.TBrowser()
