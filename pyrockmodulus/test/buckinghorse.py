# /////////////////////////////////////////////////////////////// #
# Python Script initially created on 2022-12-14
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2022
# Created using PyCharm
# /////////////////////////////////////////////////////////////// #

import pandas as pd
import pyrockmodulus
import matplotlib.pyplot as plt
import os
import matplotlib

# plt.rcParams["figure.figsize"] = [12, 6]
plt.rcParams["date.autoformatter.minute"] = "%H:%M:%S"
matplotlib.rcParams["mathtext.fontset"] = 'dejavuserif'
matplotlib.rcParams['font.family'] = ['Times New Roman']
matplotlib.rcParams['font.size'] = 12

# Change to default Dropbox before
os.chdir("../../../..")
my_path = os.path.dirname(
    os.path.abspath(__file__))  # Figures out the absolute path for you in case your working directory moves around.
dir_p = os.path.abspath(os.curdir)

location = {
    'Upper': {'mark': '.', 'color':'k', 'lab':'UBH'},
    'Lower' : {'mark': 'x', 'color':'r', 'lab':'LBH'}
}
test_ori = {
    0 : {'mark': 'x'},
    45: {'mark': '8'},
    90:{'mark': '*'}
}

rock_tests = pd.read_excel(str(dir_p) + r'/20221200_KA_URTEC_BuckingHorse_Characterization/test_results.xlsx', sheet_name='Sample Summary')

pyMR_Plots= pyrockmodulus.modulus_ratio()
plotting_MR_axis = pyMR_Plots.initial_processing(rock_type_to_plot='Sedimentary')

for loc in location.keys():
    for ori in test_ori.keys():
        valid_tests = rock_tests[(rock_tests['Max Stress (MPa) '] > 0) &
                                 (rock_tests['Eavg (GPa)'] > 0) &
                                 (rock_tests['BuckingHorse'] == loc) &
                                 (rock_tests['Orientation'] == ori)]
        plotting_MR_axis.scatter(valid_tests['Max Stress (MPa) '], valid_tests['Eavg (GPa)'], label=location[loc]['lab'] + ' - ' + str(ori) + '$^\circ$', marker=test_ori[ori]['mark'])
        x = valid_tests['Max Stress (MPa) '].tolist()
        y = valid_tests['Eavg (GPa)'].tolist()
        word = valid_tests['Confining Pressure (MPa)'].tolist()
        list_of_strings = [int(item) for item in word]

        for idx, i in enumerate(x):
            plotting_MR_axis.text(x[idx], y[idx], str(list_of_strings[idx]))


plotting_MR_axis.set_ylabel("Eavg (GPa)")
plotting_MR_axis.set_xlabel("Peak Stress (MPa)")
plotting_MR_axis.legend()
plt.tight_layout()
plt.savefig(str(dir_p) + '/20221200_KA_URTEC_BuckingHorse_Characterization/MR.svg')
plotting_MR_axis.set_xlim(10, 500)
plotting_MR_axis.set_ylim(1, 100)
plt.savefig(str(dir_p) + '/20221200_KA_URTEC_BuckingHorse_Characterization/MR_Zoomed.svg')
plt.tight_layout()
plt.show()

rock_tests = pd.read_excel(str(dir_p) + r'/20221200_KA_URTEC_BuckingHorse_Characterization/test_results.xlsx', sheet_name='UCS_E_BD')

pySR_Plots = pyrockmodulus.strength_ratio()
plotting_SR_axis = pySR_Plots.initial_processing(rock_type_to_plot='Sedimentary')

for loc in location.keys():
    for ori in test_ori.keys():
        valid_tests = rock_tests[(rock_tests['Max Stress (MPa) '] > 0) &
                                 (rock_tests['BD (MPa)'] > 0) &
                                 (rock_tests['BuckingHorse'] == loc) &
                                 (rock_tests['Orientation'] == ori) &
                                 (rock_tests['Confining Pressure (MPa)'] == 0)]
        plotting_SR_axis.scatter(valid_tests['BD (MPa)'], valid_tests['Max Stress (MPa) '],
                                 label=location[loc]['lab'] + ' - ' + str(ori) + '$^\circ$', marker=test_ori[ori]['mark'])
plotting_SR_axis.set_ylabel("UCS (MPa)")
plotting_SR_axis.set_xlabel("BD (MPa)")
plotting_SR_axis.legend()
plt.tight_layout()
plt.savefig(str(dir_p) + '/20221200_KA_URTEC_BuckingHorse_Characterization/SR.svg')
plt.show()

plotting_SR_axis = pySR_Plots.initial_processing(rock_type_to_plot='Sedimentary')

for loc in location.keys():
    for ori in test_ori.keys():
        valid_tests = rock_tests[(rock_tests['Max Stress (MPa) '] > 0) &
                                 (rock_tests['BD (MPa)'] > 0) &
                                 (rock_tests['BuckingHorse'] == loc) &
                                 (rock_tests['Orientation'] == ori)]
        plotting_SR_axis.scatter(valid_tests['BD (MPa)'], valid_tests['Max Stress (MPa) '],
                                 label=location[loc]['lab'] + ' - ' + str(ori) + '$^\circ$', marker=test_ori[ori]['mark'])
        x = valid_tests['BD (MPa)'].tolist()
        y = valid_tests['Max Stress (MPa) '].tolist()
        word = valid_tests['Confining Pressure (MPa)'].tolist()
        list_of_strings = [int(item) for item in word]

        for idx, i in enumerate(x):
            plotting_SR_axis.text(x[idx], y[idx], str(list_of_strings[idx]))

plotting_SR_axis.set_ylabel("UCS (MPa)")
plotting_SR_axis.set_xlabel("BD (MPa)")
plotting_SR_axis.legend()
plt.tight_layout()
plt.savefig(str(dir_p) + '/20221200_KA_URTEC_BuckingHorse_Characterization/SR_with_Conf.svg')
plt.show()
