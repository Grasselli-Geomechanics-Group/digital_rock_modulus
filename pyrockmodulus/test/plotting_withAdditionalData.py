# /////////////////////////////////////////////////////////////// #
# Python Script initially created on 2022-12-14
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2022
# Created using PyCharm
# /////////////////////////////////////////////////////////////// #


import pyrockmodulus
import matplotlib.pyplot as plt

xx = pyrockmodulus.modulus_ratio()

# xx._rocktype_dictionary = _rocktype_deere_miller_all = {
#                               "Shale": ["Sedimentary", 'black', 'SSh'],
#                               "Chalk": ["Sedimentary", 'fuchsia', 'SC']}

ucs_data = [75.33, 99.03, 111.69, 30.17, 73.76, 41.69, 42.09, 60.99, 39.65, 94.52, 104.6, 102.03]
E_data = [18.31, 21.85, 20.51, 8.62, 25.72, 18.68, 9.2, 14.67, 7.38, 8.48, 8.7, 8.82]

plotting_axis = xx.initial_processing(rock_type_to_plot='Sedimentary')
plotting_axis.scatter(ucs_data, E_data, label='Test Results', marker='.')
plt.ylabel("E (GPa)")
plt.xlabel("UCS (MPa)")
plt.legend()
plt.show()
