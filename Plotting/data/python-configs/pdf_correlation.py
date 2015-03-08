#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.plotscript as plotscript


def pdf_corr(args=None):
	""" """
	dicts = []
	partons = ["Gluon", "Up", "Down", "Strange"]
	for parton, title in zip(partons, [p.lower() for p in partons]):
		d = {
			"colormap": "seismic", 
			"filename": parton, 
			"files": [
				"/usr/users/dhaitz/home/artus/Excalibur/test_{}.root".format(parton)
			], 
			"folders": [
				"result"
			], 
			"texts": [
				"NNPDF 2.3"
			], 
			"texts_y": [
				0.9
			], 
			"title": title, 
			"x_expressions": [
				"corr"
			], 
			"x_label": "x", 
			"x_lims": [
				0.0001, 
				1.0
			], 
			"x_log": True, 
			"y_label": "|$ y_Z $|", 
			"y_lims": [
				0.0, 
				2.5
			], 
			"z_label": r"Correlation coefficient $ \\rho$ ($ \\sigma_Z$, PDF)", 
			"z_lims": [
				-1.0, 
				1.0
			]
		}
		dicts.append(d)
	plotscript.plotscript(dicts, args)


if __name__ == '__main__':
	pdf_corr()
