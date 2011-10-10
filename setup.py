### Copied from http://wiki.python.org/moin/Distutils/Tutorial

from distutils.core import setup

# This is a list of files to install, and where
# (relative to the 'root' dir, where setup.py is)
# You could be mroe specific.
files = []

setup(name = "simanneal",
	version = "100",
	description = "Simulated annealing implementation",
	author = "Phillip Knauss",
	author_email = "phillip.knauss@gmail.com",
	url = "DEFAULTURL",
	# Name the folder where your packages live:
	# (If you have other packages or modules, then
	# puth them into the main_package directory - they will be found
	# recursively.)
	packages = ['simanneal','simanneal/samples'],
	# 'main_package' must contain files variable
	# This dict maps the package name=to=> directories
	# Means that the package requires these files.
	package_data = {'package' : files },
	#'runner' is in the root.
	scripts = ["runner"],
	long_description = """An implementation of the Simulated Annealing heuristic for global optimization""",
	classifiers = []
)
