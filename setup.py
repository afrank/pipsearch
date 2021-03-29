import os
import setuptools
from setuptools import setup, find_packages

setup(
    name="pipsearch",
    version="0.0.1",
    description="A simple tool to scrape search results from pypi.org for pip search like capabilities",
    python_requires=">=3.4",
    author="Adam Frank",
    author_email="adam@antilogo.org",
    packages=find_packages(),
    entry_points={"console_scripts": ["pipsearch=pipsearch.main:main",],},
    install_requires=["beautifulsoup4"],
    extras_require={"test": ["coverage", "pytest", "nose", "simplejson"],},
    project_urls={"Source": "https://github.com/afrank/pipsearch",},
    test_suite="tests.unit",
)

