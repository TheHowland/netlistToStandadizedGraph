from setuptools import find_packages, setup

setup(
    name="generalizeNetlistDrawing",
    version="0.6",
    packages=find_packages(),
    install_requires=[
        "lcapy",
        "networkx",
    ],
)