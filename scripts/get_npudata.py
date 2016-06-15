#!/usr/bin/python
# standard library imports
import json
import argparse

# third party imports

# application/library imports

CLI = argparse.ArgumentParser(
	description="Reformats pileup JSON for the Excalibur NPUProducer",
	epilog="""
	Output format is a space separated csv with the columns:
	run lumi_section lumi cross_section_rms cross_section_avg
	"""
)
CLI.add_argument(
	"-j",
	"--pileup_json",
	default="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt",
	help="JSON file containing pileup information",
)
CLI.add_argument(
	"-o",
	"--out-path",
	default="npuproducer_input.txt",
)


if __name__ == "__main__":
	opts = CLI.parse_args()
	print "Reading JSON..."
	with open(opts.pileup_json) as pileup_source:
		raw_data = json.load(pileup_source)
	with open(opts.out_path, "w") as out_file:
		for run_idx, run in enumerate(sorted(raw_data)):
			print "Writing: run %3d/%3d\r" % (run_idx+1, len(raw_data)),
			for lumi_section, lumi, xs_rms, xs_avg in sorted(raw_data[run]):
				out_file.write("%d %d %g %g %g\n" % (int(run), lumi_section, lumi, xs_rms, xs_avg))
	print
