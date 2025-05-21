from setuptools import find_packages, setup

from generalizeNetlistDrawing.__version__ import __version__

setup(
    name="generalizeNetlistDrawing",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "lcapyInskale",
        "schemdrawInskale",
        "networkx"
    ],
)