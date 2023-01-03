# Setting up Wheel Files
OpenFDEM post-processing is uploaded to testpypi for simpler user download, which includes all dependencies.

The current .whl distribution is found at: 

- [./pyfdempp/README.md] (About.md) has the main description of the wheel file 
- [setup.py] (setup.py) contains package build information, links, dependencies

To recreate the wheel using the setup file, use the following two terminal commands:

- `python3 setup.py bdist_wheel --universal`

To push the wheel to TestPyPi, use `twine`:

- `twine upload -r testpypi dist/*`

To push the wheel to PyPi production, use `twine`:

- `twine upload dist/*`