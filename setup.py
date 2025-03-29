"""Setup installation script for the package."""

import os

from setuptools import find_packages, setup

REQUIRED_PACKAGES = open("requirements.txt").readlines()

README = ""
if os.path.exists("README.md"):
    README = open("README.md").read()

setup(
    name="session_manager",
    version="0.1.0",
    description="A session manager for bot automation",
    long_description=README,
    long_description_content_type="text/markdown",
    author="rilckbotslab",
    author_email="rilck.lima@botslab.com.br",
    url="https://github.com/rilckbotslab/session_manager",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platforms="any",
)