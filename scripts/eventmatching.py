#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ROOT
import time


def main():
    files = []
    trees = []
    stopWatch()
    treeName = ["finalcuts_AK5PFTaggedJetsCHSL1L2L3/ntuple", "finalcuts_AK5PFTaggedJetsCHSL1L2L3/ntuple"]
    if '-t' in sys.argv:
        treeName = [sys.argv.pop(sys.argv.index('-t') + 1), sys.argv.pop(sys.argv.index('-t') + 1)]
        print treeName
        sys.argv.remove('-t')
    if len(sys.argv) < 3:
        print "Usage: %s file1.root file2.root [-t treename1 treename2]" % sys.argv[0]
        exit(0)

    print "Read %d files:" % (len(sys.argv) - 1)
    for i in range(1, len(sys.argv)):
        print "  File%2d: %s (%s)" % (i, sys.argv[i], treeName)
        files.append(ROOT.TFile(sys.argv[i]))
        trees.append(files[-1].Get(treeName[i-1]))
    stopWatch()

    print "\nGet list of runs, lumis, events:"
    lists = []
    for tree in trees:
        lst = getRunLumiEvent(tree, 'e1event' if trees.index(tree) == 0 else 'event', 'lumisec' if trees.index(tree) == 0 else 'lumi')
        lists.append(sorted(lst))
    stopWatch()

    print "\nCompare lists:"
    com, o1, o2 = compareLists(lists[0], lists[1])
    stopWatch()
    #for item1, item2 in zip(o1, o2):
    #    print item1, item2
    #for item in com:
    #    print item
    
    print "\nCopy to output trees:"
    fout = ROOT.TFile("output.root", "RECREATE")
    c1 = cpTree(com, trees[0], "common1", 0)
    stopWatch()
    c2 = cpTree(com, trees[1], "common2", 1)
    stopWatch()
    cpTree(o1, trees[0], "only1", 0)
    stopWatch()
    cpTree(o2, trees[1], "only2", 0)  # treeIndex 0 is correct
    stopWatch()

    fout.Write()
    print "\nTrees written to file", fout.GetName()
    
    print "\nCompare common trees:"
    compareTrees(c1, c2)
    stopWatch(overall=True)
    
    
def stopWatch(n=[], overall=False):
    """print the time needed since last call"""
    n.append(time.time())
    if len(n) > 1:
        print "  -- Last step took: %1.3f s" % (n[-1] - n[-2])
    if overall:
        print "  -- Overall time:   %1.3f s" % (n[-1] - n[0])

def getRunLumiEvent(tree, eventbranch='event', lumibranch='event'):
    """get list of (run, lumi, event, entry index) from a tree"""
    result = []
    nevt = tree.GetEntries()
    for i in xrange(nevt):
        tree.GetEntry(i)
        if eventbranch == 'e1event':
            result.append((int(tree.run), int(getattr(tree, lumibranch)), int(getattr(tree, 'eventnr1') * 1000000 + getattr(tree, 'eventnr2')), i))
        else:
            result.append((int(tree.run), int(getattr(tree, lumibranch)), int(getattr(tree, eventbranch)), i))
        if i % 1000 == 0:
            print "\r  %7d/%d" % (i, nevt),
            sys.stdout.flush() 
    print "\r  %7d/%d" % (i+1, nevt)
    return result

def compareLists(list1, list2):
    """Compare two lists of (run, lumi, evt, index) and sort them into
       three lists: common events, events only in list 1 and events only
       in list 2"""
    n = 0
    m = 0
    only1 = []
    only2 = []
    common = []
    while n < len(list1) and m < len(list2):
        if n % 1000 == 0 or m % 1000 == 0 and m != 0 and n!=0:
            print "\r  tree1:%7d/%d, tree2:%7d/%d -> common:%7d, tree1: %5d, tree2: %5d" % (
                n, len(list1), m, len(list2), len(common), len(only1), len(only2)),
        if list1[n][:3] == list2[m][:3]:
            common.append(list1[n] + (list2[m][3],))  # the common list has two indices
            n += 1
            m += 1
        elif list1[n][:3] < list2[m][:3]:
            only1.append(list1[n])
            n += 1
        elif list1[n][:3] > list2[m][:3]:
            only2.append(list2[m])
            m += 1
        else:
            print "What?"
    print "\r  tree1:%7d/%d, tree2:%7d/%d -> common:%7d, tree1: %5d, tree2: %5d" % (
                n, len(list1), m, len(list2), len(common), len(only1), len(only2))
    return common, only1, only2


def cpTree(eventList, tree, name, treeIndex=0, deactivate=None):
    """Copy the events in eventList[i][3+treeIndex] from tree to a new tree of name 'name'"""
    if deactivate:
        for q in quantities:
            tree.SetBranchStatus(q, 0)
    outputTree = tree.CloneTree(0)
    outputTree.SetName(name)
    outputTree.SetTitle(tree.GetTitle() + "_" + name)
    branches = [b.GetName() for b in tree.GetListOfBranches()]
    print "  tree %r (%d branches, %d entries) to %r (%d branches, %d entries)" % (
        tree.GetName(), len(tree.GetListOfBranches()), tree.GetEntries(),
        name, len(outputTree.GetListOfBranches()), outputTree.GetEntries()),
    assert outputTree.GetEntries() == 0
    sys.stdout.flush()
    
    
    nevt = len(eventList)
    for i, evt in zip(range(nevt), eventList):
        # evt is (run, lumi, event, index in tree1, index in tree2)
        tree.GetEntry(evt[3 + treeIndex])
        if 'TNtuple' in str(type(tree)):
            outputTree.Fill(evt[3 + treeIndex])
        else:
            outputTree.Fill()
        if i % 100 == 0:
            print "\r  %7d/%d" % (i, nevt),
            sys.stdout.flush()

    outputTree.Write(name)
    print "\r  tree %r (%d branches, %d entries) to %r (%d branches, %d entries)" % (
        tree.GetName(), len(tree.GetListOfBranches()), tree.GetEntries(),
        name, len(outputTree.GetListOfBranches()), outputTree.GetEntries())
    
    return outputTree


def compareTrees(tree1, tree2):
    ex1ex2dict = {
        # ex2  :  ex1
        'event': 'eventnr',
        'lumi': 'lumisec',
        'metphi': 'METphi',
        'jet1ef': 'jet1chargedemfraction',
        'jet1chf': 'jet1chargedhadfraction',
        'jet1nhf': 'jet1neutralhadfraction', 
        'jet1mf': 'jet1muonfraction',
        'jet1hfhf': 'jet1HFhadfraction',
        'jet1hfemf': 'jet1HFemfraction',
        'jet1pf': 'jet1photonfraction', 
        'metpt': 'METpt',
        'metphi': 'METphi',
        'rawmetpt': 'rawMETpt',
        'rawmetphi': 'rawMETphi',
        'sumet': 'sumEt', 
    }
    branches1orig = [b.GetName() for b in tree1.GetListOfBranches()] # branches of tree1
    branches2orig = [b.GetName() for b in tree2.GetListOfBranches()] # branches of tree2
    branches1used = [] # branches of tree1 that are in sync with tree2
    branches2used = []
    branches1only = [b for b in branches1orig]
    branches2only = []

    for b2 in branches2orig:
        b1 = ex1ex2dict.get(b2, b2)
        if b1 in branches1orig:
            branches1used.append(b1)
            branches2used.append(b2)
            branches1only.remove(b1)
        else:
            branches2only.append(b1)
    print "  * Branch comparison:"
    print "  %4d branches only in tree1: %s" % (len(branches1only), ", ".join(branches1only))
    print "  %4d branches only in tree1: %s" % (len(branches2only), ", ".join(branches2only))
    print "  %4d common branches" % len(branches1used)
    assert len(branches1used) == len(branches2used)

    tree1.AddFriend(tree2.GetName())
    for i in xrange(tree1.GetEntries()):
        if i % 100 == 0:
            print "\rEntry", i,
        tree1.GetEntry(i)
        tree2.GetEntry(i)
        for b1, b2 in zip(branches1used, branches2used):
            v1 = getattr(tree1, b1)
            v2 = getattr(tree2, b2)
            if b1 == 'eventnr':
                v1 = int(tree1.eventnr1) * 1000000 + tree1.eventnr2
            #if b1 == 'njets':
            #    v1 = tree1.njets + tree1.njetsinv
            #    v2 = tree2.njets + tree2.njetsinv
            #    print "N JET", v1, v2
            if abs(v1 - v2) > 1e-3 and b1 not in ['muplusiso', 'muminusiso', 'rho','njets', 'njetsinv']:
                if abs(tree1.jet1eta - tree2.jet1eta) > 0.001 and b2 in ['jet1pt', 'jet1phi', 'jet1y', 'jet1chf', 'jet1nhf', 'jet1ef', 'jet1pf', 'jet1hfhf', 'jet1hfemf']:
                    continue
                if abs(tree1.jet2eta - tree2.jet2eta) > 0.001 and b2 in ['jet2pt', 'jet2phi', 'jet2y']:
                    continue
                if 'mu2' in b2:
                    continue
                print "\rIn entry %7d, %s differs: %s = %s, %s = %s" % (i, b2, b1, v1, b2, v2)
    print "\rEntry", i
    
            
    
main()
