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


# local caching
def get_relsubpath(path, reference_path=getPath()):
	"""
	Get a relative path for sub-folders/files, else an absolute one

	This works similar to `os.path.relpath` but ensures that the relative path
	is contained within the reference_path. If this is not the case, `path` is
	returned unmodified.

	This function is intended mainly to check whether something is subject to VCS.
	"""
	rel_path = os.path.relpath(
		os.path.abspath(path),
		os.path.abspath(reference_path)
	)
	if not rel_path.startswith(".."):
		return rel_path
	return path


def cached_query(func, func_args=(), func_kwargs={}, dependency_files=(), dependency_folders=(), cache_key=None, cache_dir=get_cachepath()):
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
