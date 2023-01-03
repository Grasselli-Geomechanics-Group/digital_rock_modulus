import setuptools
import pathlib
import os

HERE = pathlib.Path("pyrockmodulus/README.md")
README = (HERE).read_text()

setuptools.setup(
    name="pyrockmodulus",
    author="Grasselli's Geomechanics Group - University of Toronto",
    author_email="aly.abdelaziz@mail.utoronto.ca",
    description="Module to plot Modulus and Strength ratios for rock.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="Modulus_Ratio Strength_Ratio Deere_Miller Rock_Classification",
    url="https://github.com/alicarlos/digital_modulus_strength_ratio",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    version=0.5,
    install_requires=[
        "pandas>=0.0",
        "numpy>=1.0",
        "scipy~=1.2.1",
        "matplotlib>=3.5",
        "seaborn~=0.11.0",
    ]

)