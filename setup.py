# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in solubis_brand/__init__.py
from solubis_brand import __version__ as version

setup(
	name='solubis_brand',
	version=version,
	description='For Styling',
	author='bobzz.zone@gmail.com',
	author_email='bobzz.zone@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
