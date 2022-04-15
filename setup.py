# -*- coding: utf-8 -*-
import os
from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup

with open(join(dirname(__file__), "README.rst")) as readme:
    README = readme.read()

with open(join(dirname(__file__), "VERSION")) as f:
    VERSION = f.read()

tests_require = []
with open(join(dirname(abspath(__file__)), "requirements.txt")) as f:
    for line in f:
        tests_require.append(line.strip())

# allow setup.py to be run from any path
os.chdir(normpath(join(abspath(__file__), os.pardir)))
setup(
    name="edc-pharmacy",
    version=VERSION,
    author="Tshepiso Setsiba",
    maintainer="Erik van Widenfelt",
    author_email="ew2789@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    url="http://github.com/clinicedc/edc-pharmacy",
    license="GPL license, see LICENSE",
    description="Pharmacy module for clinicedc/edc projects",
    long_description_content_type="text/x-rst",
    long_description=README,
    zip_safe=False,
    keywords="django edc edc-pharmacy",
    install_requires=[],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.7",
    tests_require=tests_require,
    test_suite="runtests.main",
)
