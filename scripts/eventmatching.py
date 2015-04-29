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
	#	print item1, item2
    #for item in com:
    #    print item
    
    print "\nCopy to output trees:"
    fout = ROOT.TFile("output.root", "RECREATE")
    cpTree(com, trees[0], "common1", 0)
    stopWatch()
    cpTree(com, trees[1], "common2", 1)
    stopWatch()
    cpTree(o1, trees[0], "only1", 0)
    stopWatch()
    cpTree(o2, trees[1], "only2", 0)  # treeIndex 0 is correct
    stopWatch()

    fout.Write()
    print "\nTrees written to file", fout.GetName()
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
    branches = list(set([b.GetName() for b in tree.GetListOfBranches()]))
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

    return True

main()
