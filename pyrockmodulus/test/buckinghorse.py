# /////////////////////////////////////////////////////////////// #
# Python Script initially created on 2022-12-14
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2022
# Created using PyCharm
# /////////////////////////////////////////////////////////////// #

import pandas as pd
import pyrockmodulus
import matplotlib.pyplot as plt

rock_tests = pd.read_excel(r'/external/ownCloud/2020_PETRONAS/Milling_Updates.xlsx', sheet_name='Sample Summary')

valid_tests_upper = rock_tests[(rock_tests['Max Stress (MPa) '] > 0) & (rock_tests['Eavg (GPa)'] > 0) & (rock_tests['BuckingHorse'] == "Upper")]

valid_tests_lower = rock_tests[(rock_tests['Max Stress (MPa) '] > 0) & (rock_tests['Eavg (GPa)'] > 0) & (rock_tests['BuckingHorse'] == "Lower")]

xx = pyrockmodulus.modulus_ratio()
plotting_axis = xx.initial_processing(rock_type_to_plot='Sedimentary')
plotting_axis.scatter(valid_tests_lower['Max Stress (MPa) '], valid_tests_lower['Eavg (GPa)'], label='Lower BuckingHorse', marker='x')
plotting_axis.scatter(valid_tests_upper['Max Stress (MPa) '], valid_tests_upper['Eavg (GPa)'], label='Upper BuckingHorse', marker='.')
plt.ylabel("E (GPa)")
plt.xlabel("UCS (MPa)")
plt.legend()
plt.show()


