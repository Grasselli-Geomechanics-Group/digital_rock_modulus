# /////////////////////////////////////////////////////////////// #
# Python Script initially created on 2022-12-14
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2022
# Created using PyCharm
# /////////////////////////////////////////////////////////////// #

import platform
import sys

'''
VERIFICATION CODE BLOCK
    - Check Python compatibility
    - Display system information
'''

__version__ = "0.1"
# if platform.architecture()[0] != "64bit":
#     exit("Compatible only on x64")

# Check python compatibility before proceeding
try:
    assert sys.version_info >= (3, 5)
    print("Python Version: %s" % sys.version.split('\n')[0])
except AssertionError:
    print("Python Version: %s" % sys.version.split('\n')[0])

# Load Classes
from .pyrockmodulus import (
    modulus_ratio,
    poisson_density,
    strength_ratio,
)

# Load sub-routine modules py files
from . import (
    formatting_codes,
    rock_variables,
)