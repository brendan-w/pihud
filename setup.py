#!/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="pihud",
    version="0.1.0",
    description=("Configurable heads up display for the Raspberry Pi using a car's OBD port"),
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Topic :: System :: Monitoring",
        "Programming Language :: Python :: 2 :: Only",
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Logging",
        "Intended Audience :: Developers",
    ],
    keywords="obd car heads-up display Hud vehicle diagnostic",
    author="Brendan Whitfield",
    author_email="me@brendan-w.com",
    url="http://github.com/brendan-w/piHud",
    license="GNU LGPLv2.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["obd"],
)
