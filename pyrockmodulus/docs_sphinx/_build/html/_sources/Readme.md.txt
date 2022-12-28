# About Documentation
Documentation was put together using `Sphinx`, pointing at the .py files in openfdem folder. 

# Where to Find Config Files
All build settings for documentation are controlled in [conf.py](conf.py). The start page and display menu are found under the file [index.rst](index.rst).

# Running Sphinx

## HTML Build
To rerun the HTML build (ex. if a docstring is updated), run
 `make html` 
 in terminal.

To view the `HTML` files locally, navigate to  `_build` -> `html` -> [index.html](_build/html/index.html). From there the sub-modules can be accessed in your browser.
To format the HTML files, refer to `index.rst` and `conf.py`.

## Latex and PDF Build
To rerun the Latex and PDF build (ex. if a docstring is updated), run
 `make latexpdf` 
 in terminal.

To view the PDF file, navigate to  `_build` -> `latex` -> [openfdempost-processing.pdf](_build/latex/openfdempost-processing.pdf). 
