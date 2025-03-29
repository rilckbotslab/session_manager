"""Setup installation script for the package."""

import os

from setuptools import find_packages, setup

REQUIRED_PACKAGES = open("requirements.txt").readlines()

README = ""
if os.path.exists("README.md"):
    README = open("README.md").read()

setup(
    name="botslab",
    version="0.1.0",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Rilck",
    author_email="rilck.lima@botslab.com.br",
    url="https://github.com/rilckbotslab/session_manager",
    install_requires=REQUIRED_PACKAGES,    
    packages=find_packages(
        include=[
            "botslab",
            "botslab.*",
        ]
    ),
    platforms="any",
)