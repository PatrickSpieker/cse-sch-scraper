
from setuptools import setup, find_packages
desc = "Python 2 project which visualizes possible degree paths for a given major."
setup(
        name="uw-sch-scraper",
        version="0.1.dev2",
        description=desc,
        url="https://github.com/PatrickSpieker/uw-sch-scraper",
        author="Patrick Spieker",
        author_email="pspieker@uw.edu",
        license="MIT",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2.7",
        ],
        packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
        install_requires=["pygraphviz","graphviz", "requests", "beautifulsoup4"],
        )

