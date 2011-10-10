### Copied from http://wiki.python.org/main/Distutils/Tutorial

from distutils.core import setup
import os

""" find_packages implementation from """
""" http://wiki.python.org/moin/Distutils/Cookbook/AutoPackageDiscovery """

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


files = []

packages = find_packages(".")

setup(name = "simanneal",
	version = "100",
	description = "Simulated annealing implementation",
	author = "Phillip Knauss",
	author_email = "phillip.knauss@gmail.com",
	url = "DEFAULTURL",
        package_dir = packages,
	# Automatically find packages
	packages = packages.keys(),
	package_data = {'package' : files },
	#'runner' is in the root.
	scripts = ["runner"],
	long_description = """An implementation of the Simulated Annealing heuristic for global optimization""",
	classifiers = []
)

