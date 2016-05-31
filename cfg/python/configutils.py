#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
advanced utilities for managing config files and their data
"""
import os
import sys
import hashlib
import cPickle as pickle
import time
import base64
import itertools
import tarfile
import urllib2
import StringIO
import logging
import json
import glob
import subprocess
import socket

# settings used when making a choice
config_logger = logging.getLogger("CONF")
# internals of caching
cache_logger = logging.getLogger("CACHE")
# enviroment
env_logger = logging.getLogger("ENV")


# Environment
no_default=object()


def get_excalibur_env(variable, nofail=False, default=no_default):
	"""
	Get an environment variable defined for Excalibur

	:param variable: name of the variable
	:type variable: str
	:param nofail: do not exit the application if the variable is undefined and no
	               default is given
	:type nofail: bool
	:param default: default to use if the variable is not defined
	:type default: str
	:returns: value variable
	:rtype: str or None

	:raises SystemExit: if the variable is undefined, default is unset and `nofail`
	                    is not `True`
	"""
	try:
		ret_val = os.environ[variable]
		env_logger.debug("Using $%s => %s" % (variable, ret_val))
		return ret_val
	except KeyError:
		if default is not no_default:
			env_logger.debug("Using $%s => %s (default)" % (variable, default))
			return default
		print variable, "is not in shell variables:", os.environ.keys()
		print "Please source ./scripts/ini_excalibur.sh and CMSSW!"
		if nofail:
			return None
		sys.exit(1)


def getPath(variable='EXCALIBURPATH', nofail=False, default=no_default):
	"""Base path to the Excalibur repo/code"""
	return get_excalibur_env(variable, nofail, default)


def get_cachepath(variable='EXCALIBURCACHE', nofail=False, default=None):
	"""Base path to locally cached files"""
	if default is None:
		default = os.path.join(getPath(), "cache")
	return get_excalibur_env(variable, nofail, default)


def download_tarball(url, extract_to='.'):
	"""
	Download and extract an archive
	"""
	# access archive in-memory: content stream opened as file-like string
	archive = tarfile.open(fileobj=StringIO.StringIO(urllib2.urlopen(url).read()))
	archive.extractall(path=extract_to)
	return archive.getnames()


# lazily evaluated objects for dependencies
# objects must provide the `artus_value` attribute/property
class DeferredCall(object):
	"""
	Call that is evaluated lazily

	Instances allow an explicit resolution via the `resolve` method. They also
	serve as proxies for immutable operations, such as `dc + 2` or `len(dc)`.
	Methods that allow mutation may be available, but their effect will be lost.
	"""
	def __init__(self, func, *func_args, **func_kwargs):
		self.func = func
		self.func_args = func_args
		self.func_kwargs = func_kwargs

	def resolve(self):
		"""Resolve and return the call"""
		return self.func(*self.func_args, **self.func_kwargs)

	@property
	def artus_value(self):
		"""Value to store in artus config JSON"""
		return self.resolve()

	# magic must be resolved explicitly
	# self other - resolve in reflected order to allow other to resolve as well
	for so_magic in [("lt", "gt"), ("le", "ge"), ("eq", "eq"), ("ne", "ne"), ("add", "radd"), ("sub", "rsub"), ("mul", "rmul"), ("div", "rdiv"), ("truediv", "rtruediv"), ("floordiv", "rfloordiv"), ("mod", "rmod"), ("divmod", "rdivmod"), ("pow", "rpow"), ("lshift", "rlshift"), ("rshift", "rrshift"), ("and", "rand"), ("xor", "rxor"), ("or", "ror")]:
		for func_name, refl_name in [(so_magic[0], so_magic[1]), (so_magic[1], so_magic[0])]:
			exec("def __%(fname)s__(self, other):\n\ttry:\n\t\tres = other.__%(rname)s__(self.resolve())\n\t\tif res == NotImplemented:\n\t\t\traise AttributeError\n\texcept AttributeError:\n\t\tres = self.resolve().__%(fname)s__(other)\n\treturn res" % {"fname": func_name, "rname": refl_name})

	# regular magic - immutable only
	for magic in ("str", "nonzero", "unicode", "getattr", "call", "len", "getitem", "missing", "iter", "reversed", "contains", "getslice", "neg", "pos", "abs", "invert", "complex", "int", "long", "float", "oct", "hex", "index"):
		exec("def __%(fname)s__(self, *args, **kwargs):\n\treturn self.resolve().__%(fname)s__(*args, **kwargs)" % {"fname": magic})


class DeferredAttribute(DeferredCall):
	"""Attribute/Property that is dereferenced lazily"""
	def __init__(self, owner, attribute_name):
		DeferredCall.__init__(self, lambda: getattr(owner, attribute_name))


class RunJSON(object):
	"""
	Abstraction of CMS run JSONs with joins and run whitelisting

	The CMS run JSONs define which runs contain valid data. This class allows
	joining of JSONs and filtering of runs via whitelisting. It is intended for
	consistent use when multiple sources define runs and multiple consumers
	depend on run selection.

	:param base_jsons: path(s) to one or several CMS run JSONs
	:type base_jsons: str or list[str]
	:param json_store: directory to store dynamic jsons in
	:type json_store: str

	:note: When initialized with an existing instance, the later is returned
	       unchanged.
	"""
	def __new__(cls, *args, **kwargs):
		if isinstance(args[0], cls):
			return args[0]
		else:
			return object.__new__(cls)

	def __init__(self, base_jsons, json_store=None, run_ranges=None):
		if isinstance(base_jsons, self.__class__):
			return
		self._base_jsons = [base_jsons] if isinstance(base_jsons, basestring) else list(base_jsons)
		self._run_ranges = run_ranges or []
		self._store_path = json_store or os.path.join(getPath(), "data", "json")

	def set_base_json(self, *json_paths):
		"""Overwrite the base JSON run selection, discarding all others"""
		self._base_jsons = list(json_paths)

	def add_base_json(self, json_path):
		"""Add a base JSON for run selection"""
		self._base_jsons.append(json_path)

	def set_run_range(self, *run_ranges):
		"""
		Overwrite the run range whitelist, discarding all others

		When called with no argument, the whitelist is cleared, allowing all
		runs to be used.
		"""
		self._run_ranges = list(run_ranges)

	def add_run_range(self, min_run, max_run):
		"""
		Add a run range to the whitelist

		:param min_run: lowest run to include
		:type min_run: int or float
		:param max_run: highest run to include
		:type max_run: int or float
		"""
		self._run_ranges = self._join_ranges(self._run_ranges + [(min_run, max_run)])

	def __str__(self):
		return self.resolve()

	def __repr__(self):
		return "RunJSON(files=%s, runs=%s)" % (self._base_jsons, self._run_ranges)

	def resolve(self):
		"""Path to the JSON file"""
		return cached_query(
			func=self._make_dynamic_json,
			dependency_files=self._base_jsons + [self._get_store_path(self._dynamic_basename())],
			cache_key=os.path.splitext(self._dynamic_basename())[0],
			cache_dir=self._store_path
		)

	@property
	def artus_value(self):
		"""Value to store in artus config JSON"""
		config_logger.info("Using run JSON '%s'", self.resolve())
		return [self.resolve()]

	def _make_dynamic_json(self):
		"""Create a file containing the json content"""
		json_outpath = self._get_store_path(self._dynamic_basename())
		json_data = {}
		for json_path in self._base_jsons:
			with open(json_path) as json_source:
				new_json_data = json.load(json_source)
			if not self._run_ranges:
				json_data.update(new_json_data)
			for run in new_json_data:
				for min_run, max_run in self._run_ranges:
					if min_run <= int(run) <= max_run:
						json_data[run] = self._join_ranges(new_json_data[run] + json_data.get(run, []))
						break
		with open(json_outpath, "w") as output_file:
			# dump compact but pretty-printed to play nice with git
			json.dump(json_data, output_file, separators=(',', ':'), sort_keys=True, indent=1)
		return json_outpath

	def _get_store_path(self, json_name):
		"""Get the path to the json in the local store"""
		return os.path.join(self._store_path, os.path.basename(json_name))

	def _dynamic_basename(self):
		"""Basename of dynamically created file"""
		if len(self._base_jsons) == 1 and not self._run_ranges:
			return os.path.basename(self._base_jsons[0])
		basename = "runjson_"
		basename += "_".join([os.path.splitext(os.path.basename(json_path))[0] for json_path in self._base_jsons])
		basename += "_runs" + "_".join(["%.0f-%.0f" % run_range for run_range in self._run_ranges])
		return basename + ".json"

	@staticmethod
	def _join_ranges(ranges):
		"""Compress `(min, max)` ranges by joining overlapping ones"""
		run_ranges = []
		for min_run, max_run in sorted(ranges):
			if not run_ranges:
				run_ranges = [(min_run, max_run)]
			elif min_run < run_ranges[-1][1] < max_run:
				run_ranges[-1] = (run_ranges[-1][0], max_run)
			else:
				run_ranges.append((min_run, max_run))
		return run_ranges


class PUWeights(object):
	"""
	PileUp weights for tuning MC pileup distribution to match data

	:param npu_data_source: a run JSON specifying the runs used in data
	:type npu_data_source: str or :py:class:`~configutils.RunJSON`
	:param npu_mc_source: input files for MC processing, i.e. the input file glob
	:type npu_mc_source: str
	:param pileup_json: path to json containing pileup information
	:type pileup_json: str
	:param min_bias_xsec: minimum bias cross section to assume
	:type min_bias_xsec: float or int
	:param weight_limits: min and max limits to truncate excessive weights
	:type weight_limits: Tuple[float or int, float or int]
	:param puweight_store: directory to store PU Weight files in
	:type puweight_store: str

	:see: Artus' `puWeightCalc.py` for a functional description of parameters.
	"""
	def __init__(
			self,
			npu_data_source,
			npu_mc_source,
#			pileup_json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt",
			pileup_json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt",
			min_bias_xsec=69.0,
			weight_limits=(0, 4),
			puweight_store=None,
	):
		self.npu_data_source = npu_data_source
		self.npu_mc_source = npu_mc_source
		self.pileup_json = pileup_json
		self.min_bias_xsec = min_bias_xsec
		self.weight_limits = weight_limits
		self._store_path = puweight_store or os.path.join(getPath(), "data", "pileup")

	def __str__(self):
		return self.resolve()

	def __repr__(self):
		return "%s(npu_data_source=%s, npu_mc_source=%s, pileup_json=%s, min_bias_xsec=%.1f, weight_limits=%s)" % (self.__class__.__name__, self.npu_data_source, self.npu_mc_source, self.pileup_json, self.min_bias_xsec, self.weight_limits)

	def resolve(self):
		"""Path to the PU Weight file"""
		return cached_query(
			func=self._make_pu_weights,
			dependency_files=[str(self.npu_data_source), self._output_path()] + glob.glob(str(self.npu_mc_source)),
			cache_key=self._nickname(),
			cache_dir=self._store_path
		)

	@property
	def artus_value(self):
		"""Value to store in artus config JSON"""
		config_logger.info("Using PU Weights '%s'", self.resolve())
		return self.resolve()

	def _make_pu_weights(self):
		npu_data_source = str(self.npu_data_source)
		npu_mc_skim_files = glob.glob(str(self.npu_mc_source))
		output_path = self._output_path()
		subprocess.check_call(["puWeightCalc.py", npu_data_source] + npu_mc_skim_files + ["--inputLumiJSON", self.pileup_json, "--minBiasXsec", str(self.min_bias_xsec), "--weight-limits"] + [str(weight) for weight in self.weight_limits] + ["--output", output_path])
		return output_path

	def _output_path(self):
		"""Path to output file"""
		return os.path.join(self._store_path, self._nickname() + ".root")

	def _nickname(self):
		"""Nickname for the generated PU Weights"""
		def source_nick(source_str):
			nick = os.path.splitext("_".join(source_str.split(os.sep)[-2:]))[0]
			nick = nick.replace("*", "_ST_").replace("?", "_QM_").replace("[", "_SO_").replace("]", "_SE_").replace("!", "_NO_")
			return nick
		return ("pileup_" + source_nick(str(self.npu_data_source)) + "_to_" + source_nick(str(self.npu_mc_source)) + "_xsec_" + ("%.1f" % self.min_bias_xsec) + "_weights_" + "-".join([str(weight) for weight in self.weight_limits])).replace("__", "_")


class InputFiles(object):
	"""
	Domain specific input file resolution

	:param ekppath: glob for files at EKP
	:type ekppath: str
	:param nafpath: glob for files at NAF
	:type nafpath: str

	:note: The interface accepts *any* parameter of the form `domain = glob`,
	       with both `domain` and `glob` being strings. `domain` is truncated
	       to three characters, lower case. The explicit parameters `ekppath`
	       and `nafpath` exist for compatibility; there is no special handling.
	"""
	def __init__(self, **kwargs):
		self.inputs = {}
		self.set_input(**kwargs)
		self.host = socket.gethostname()[:3].lower()

	def set_input(self, **kwargs):
		"""Overwrite the input for specific domains"""
		for domain in kwargs:
			self.inputs[domain[:3].lower()] = kwargs[domain]

	def __str__(self):
		return self.resolve()

	def __repr__(self):
		return "%s(host=%s,inputs=%s)" % (self.__class__.__name__, self.host, self.inputs)

	def resolve(self):
		"""Path to the input files used (i.e. the glob for the local domain)"""
		try:
			if not self.inputs[self.host]:
				raise KeyError
			return self.inputs[self.host]
		except KeyError:
			raise KeyError("Input file for domain '%s' not set" % self.host)

	@property
	def artus_value(self):
		"""Value to store in artus config JSON"""
		config_logger.info("Using Input Files '%s' (Domain: '%s')", self.resolve(), self.host)
		return self.resolve()


class Lumi(object):
	"""
	Lumi information in /fb for the used runs

	:param json_source: a run JSON file specifying the runs used in data
	:type json_source: str or :py:class:`~configutils.RunJSON`
	:param normtag: `brilcalc` normtag file
	:type normtag: str

	:note: Internally uses the `brilcalc` tool, which may currently only be run
	       at CERN. Connects via SSH using the address in $EXCALIBURBRILSSH`.
	"""
	def __init__(self, json_source, normtag="/afs/cern.ch/user/c/cmsbril/public/normtag_json/OfflineNormtagV1.json"):
		self.json_source = json_source
		self.normtag = normtag

	def resolve(self):
		"""Lumi for the given runs in /fb"""
		json_source = getattr(self.json_source, "artus_value", self.json_source)
		if not isinstance(json_source, basestring):
			assert len(json_source) == 1, 'Lumi calculation supports only 1 run JSON'
			json_source = json_source[0]
		# use verbose key for identifying commited lumi results
		cache_key = "lumi_path-" + os.path.splitext(os.path.basename(json_source))[0]
		cache_key += ("_nt-" + os.path.splitext(os.path.basename(self.normtag))[0]) if self.normtag else ""
		cache_dep = [get_relsubpath(path) for path in [json_source] if path is not None]
		lumi = cached_query(
			func=self._get_lumi,
			dependency_files=cache_dep,
			cache_dir=os.path.join(getPath(), "data", "lumi"),
			cache_key=cache_key,
		)
		return lumi

	@property
	def artus_value(self):
		"""Value to store in artus config JSON"""
		lumi = self.resolve()
		config_logger.info("Using lumi %.3f/fb", lumi)
		return lumi

	def _get_lumi(self):
		json_source = getattr(self.json_source, "artus_value", self.json_source)
		if not isinstance(json_source, basestring):
			assert len(json_source) == 1, 'Lumi calculation supports only 1 run JSON'
			json_source = json_source[0]
		bril_ssh = get_excalibur_env("EXCALIBURBRILSSH", default="lxplus.cern.ch")
		# parse jsons so that we can send any file and string input over SSH as run string
		try:
			json_data = json.loads(json_source)
		except ValueError:
			with open(json_source) as json_file:
				json_data = json.load(json_file)
		# remove string quotes - brilssh uses own format...
		json_string = json.dumps(json_data).replace(r'"', r'')
		if json_string == "{}":
			return 0.0
		# execute brilcalc on a remote host
		config_logger.warning("Querying brilcalc for lumi (via %s)", bril_ssh)
		with open(os.path.join(getPath(), "scripts", "get_lumi.py")) as get_lumi_raw:
			lumi_json_raw = subprocess.check_output([
					"ssh", bril_ssh,
					# stream script directly to remote python interpreter via CLI
					'python -c "%(get_lumi)s" "%(json_string)s" '
					'--lumi-unit "/pb" %(normtag)s' % {
						"get_lumi": get_lumi_raw.read().replace(r'"', r'\"'),
						"json_string": json_string,
						"normtag": "" if self.normtag is None else ('--normtag "%s"' % self.normtag),
					}
				])
		lumi_dict = json.loads(lumi_json_raw)
		# query /pb for precision, convert to /fb
		return lumi_dict["totrecorded"]/1000.0


# local caching
def get_relsubpath(path, reference_path=None):
	"""
	Get a relative path for sub-folders/files, else an absolute one

	This works similar to `os.path.relpath` but ensures that the relative path
	is contained within the reference_path. If this is not the case, `path` is
	returned unmodified.

	This function is intended mainly to check whether something is subject to VCS.
	"""
	reference_path = reference_path if reference_path is not None else getPath()
	rel_path = os.path.relpath(
		os.path.abspath(path),
		os.path.abspath(reference_path)
	)
	if not rel_path.startswith(".."):
		return rel_path
	return path


def cached_query(func, func_args=(), func_kwargs={}, dependency_files=(), dependency_folders=(), cache_key=None, cache_dir=None):
	"""
	Get the response to a query, caching it if possible

	:param func: a callable that performs the actual query
	:type func: callable
	:param func_args: `*args` passed to `func` for the query
	:type func_args: tuple, list
	:param func_kwargs: `**kwargs` passed to `func` for the query
	:type func_kwargs: dict
	:param dependency_files: files the response depends on
	:type dependency_files: list[str]
	:param dependency_folders: folders, including their content, the response depends on
	:type dependency_folders: list[str]
	:param cache_key: overwrite the name of the cache data
	:type cache_key: str
	:param cache_dir: directory to store cache data (response and meta info)
	:type cache_dir: str
	:returns: response from the query, possibly from an earlier cached call

	:note: By default, the `cache_key` identifies the function and its
	       arguments. A custom `cache_key` should reflect this as needed.

	:warning: The automatic generation of the `cache_key` does not work
	          deterministically for lambda functions; `cache_key` should be set
	          manually for lambda functions.
	"""
	cache_dir = cache_dir if cache_dir is not None else get_cachepath()
	def stat_file(file_path):
		"""Get a comparable representation of file validity"""
		try:
			file_stat = os.stat(file_path)
			return file_stat.st_size, file_stat.st_mtime
		except OSError:
			return -1, -1
	# key for finding/storing cached responses
	if cache_key is None:
		mangle = lambda data: base64.b32encode(hashlib.sha1(str(data)).digest())
		cache_key = "_".join((
			func.__name__,
			mangle(func_args),
			mangle(sorted(func_kwargs.iteritems())),
			mangle(sorted(dependency_files))
		))
	cache_path = os.path.join(cache_dir, cache_key + ".pkl")
	try:
		# check cache validity - use GeneratorExit to short-circuit
		if not os.path.exists(cache_path):
			raise GeneratorExit("not cached")
		with open(cache_path, "rb") as cache_file:
			cache_data = pickle.load(cache_file)
		cache_meta = cache_data["meta"]
		if not set(cache_meta.get("dependency_files", {}).keys()) >= set(dependency_files):
			raise GeneratorExit("missing dependencies")
		cache_files = cache_meta.get("dependency_files", {})
		cache_folders = cache_meta.get("dependency_folders", {})
		for dep_file in dependency_files:
			if cache_files.get(dep_file, (-1, -1)) != stat_file(dep_file):
				raise GeneratorExit("change in dep file ('%s')" % dep_file)
		for dep_folder in dependency_folders:
			if cache_folders.get(dep_folder, (-1, -1)) != stat_file(dep_folder):
				raise GeneratorExit("change in dep folder ('%s')" % dep_folder)
			dep_files = os.listdir(dep_folder) + [dep_file for dep_file in cache_files if os.path.dirname(dep_file) == dep_folder]
			for dep_file in dep_files:
				if cache_files.get(dep_file, (-1, -1)) != stat_file(dep_file):
					raise GeneratorExit("change in dep folder ('%s')" % dep_file)
		response = cache_data["response"]
		cache_logger.info("Loaded '%s' in '%s'", cache_key, cache_dir)
	except GeneratorExit as err_reason:
		cache_logger.warning('regenerating cache, reason: %s', err_reason)
		# cache is dirty, regenerate it
		response = func(*func_args, **func_kwargs)
		if not os.path.isdir(os.path.dirname(cache_path)):
			os.makedirs(os.path.dirname(cache_path))
		with open(cache_path, "wb") as cache_file:
			dep_files = set(dependency_files).union(itertools.chain(*(os.listdir(pth) for pth in dependency_folders if os.path.exists(pth))))
			pickle.dump(
				{
					# response body
					"response": response,
					# meta header
					"meta": {
						"timestamp": time.time(),
						"dependency_files": dict((dep_file, stat_file(dep_file)) for dep_file in dep_files),
						"dependency_folders": dict((dep_folder, stat_file(dep_folder)) for dep_folder in dependency_folders),
					}
				},
				cache_file,
				# use ASCII protocol for better git integration
				0,
			)
		cache_logger.info("Stored '%s' in '%s'", cache_key, cache_dir)
	return response
