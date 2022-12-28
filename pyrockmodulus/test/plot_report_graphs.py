# /////////////////////////////////////////////////////////////// #
# Python Script initially created on 3/3/22
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2022
# Created using PyCharm
# /////////////////////////////////////////////////////////////// #

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import operator as op
import numpy as np
from scipy.interpolate import interp1d
# import Mohr_Envelope as mohr
import math
import os

# plt.rcParams['figure.constrained_layout.use'] = True
# plt.rcParams["figure.figsize"] = [6, 6]
plt.rcParams["date.autoformatter.minute"] = "%H:%M:%S"
matplotlib.rcParams["mathtext.fontset"] = 'dejavuserif'
matplotlib.rcParams['font.family'] = ['Times New Roman']
matplotlib.rcParams['font.size'] = 12

os.chdir("../..")
dir_p  = os.path.abspath(os.curdir)

def draw_spline_option(x_data, y_data, relation_type='quadratic'):

    # Define interpolators.
    res = [idx for idx, item in enumerate(x_data) if item in x_data[:idx]]

    # Look for duplicates, if any.
    if res:
        print("Found Duplicates")
        dict_to_load = {'X': x_data, 'Y': y_data}
        df = pd.DataFrame(dict_to_load)
        grouped_df_wo_duplicates = df.groupby("X")["Y"].mean()
        y_data = grouped_df_wo_duplicates.to_list()
        x_data = grouped_df_wo_duplicates.index.to_list()

    f_quadratic = interp1d(x_data, y_data, kind=relation_type)
    x_interpol = np.linspace(min(x_data), max(x_data), 1000)
    y_interpol = f_quadratic(x_interpol)

    return  x_interpol, y_interpol

df = pd.read_excel(str(dir_p) + r'/20221200_KA_URTEC_BuckingHorse_Characterization/test_results.xlsx', sheet_name='Sample Summary')
print(df.columns)

grouped_df_ori_bedding = df.groupby(['Orientation', 'Proposed Test'])
grouped_df_conf_bedding = df.groupby(['Confining Pressure (MPa)', 'Proposed Test'])
grouped_df_test = df.groupby(['Proposed Test'])

# ''''
# PROJECT GRAPHS!
# '''

Conf = {0: {'F_Color': 'b'},
        5: {'F_Color': 'r'},
        10: {'F_Color': 'g'},
        15: {'F_Color': 'k'}
        }
### VERTICAL LAYOUT ###

fig_layout = plt.figure(figsize=(6, 18))
gs = fig_layout.add_gridspec(nrows=3, ncols=1, hspace=0)
axs = gs.subplots(sharex=True, sharey=False)

count = int(0)
info_to_plot = ['Max Stress (MPa) ', 'Eavg (GPa)', 'Poisson Ratio (-)']
for plot_info in info_to_plot:
    for key, item in grouped_df_conf_bedding:
        for conf_type in Conf.keys():
            if key == (conf_type, "TRI") or key == (conf_type, "UCS"):
                a_group = grouped_df_conf_bedding.get_group(key)
                upper_group = a_group[a_group['Depth Bottom (m)'].lt(950)].sort_values(by='Orientation')
                lower_group = a_group[a_group['Depth Bottom (m)'].gt(950)].sort_values(by='Orientation')

                axs[count,].scatter(lower_group['Orientation'], lower_group[plot_info], label = "LBH at %s MPa Confinement" % conf_type, marker ='.', linewidths=2.5, color=Conf[conf_type]['F_Color'])
                axs[count,].scatter(upper_group['Orientation'], upper_group[plot_info], label = "UBH at %s MPa Confinement" % conf_type, marker ='x', linewidths=2.5, color=Conf[conf_type]['F_Color'])

                x_interpol, y_interpol = draw_spline_option(np.array(lower_group['Orientation']),
                                                            np.array(lower_group[plot_info]))

                axs[count,].plot(x_interpol, y_interpol, '--', color=Conf[conf_type]['F_Color'])

                x_interpol, y_interpol = draw_spline_option(np.array(upper_group['Orientation']),
                                                            np.array(upper_group[plot_info]))

                axs[count,].plot(x_interpol, y_interpol, ':', color=Conf[conf_type]['F_Color'])

    count += 1

for idx, i in enumerate(info_to_plot):
    axs[idx].set_ylabel(i)
    axs[idx].set_xticks([0, 45, 90])
plt.xlabel('Bedding Orientation ($^\circ$)')
axs[0].legend()
fig_layout.tight_layout()

fig_layout.savefig(dir_p + r"/20221200_KA_URTEC_BuckingHorse_Characterization/VlLayout_3x1.svg")
fig_layout.show()

### HORIZONTAL LAYOUT ###

fig_layout = plt.figure(figsize=(18, 6))
gs = fig_layout.add_gridspec(1, 3)
axs = gs.subplots(sharex=False
                  , sharey=False)

count = int(0)
info_to_plot = ['Max Stress (MPa) ', 'Eavg (GPa)', 'Poisson Ratio (-)']
for plot_info in info_to_plot:
    for key, item in grouped_df_conf_bedding:
        for conf_type in Conf.keys():
            if key == (conf_type, "TRI") or key == (conf_type, "UCS"):
                a_group = grouped_df_conf_bedding.get_group(key)
                upper_group = a_group[a_group['Depth Bottom (m)'].lt(950)].sort_values(by='Orientation')
                lower_group = a_group[a_group['Depth Bottom (m)'].gt(950)].sort_values(by='Orientation')

                axs[count,].scatter(lower_group['Orientation'], lower_group[plot_info], label = "LBH at %s MPa Confinement" % conf_type, marker ='.', linewidths=2.5, color=Conf[conf_type]['F_Color'])
                axs[count,].scatter(upper_group['Orientation'], upper_group[plot_info], label = "UBH at %s MPa Confinement" % conf_type, marker ='x', linewidths=2.5, color=Conf[conf_type]['F_Color'])

                x_interpol, y_interpol = draw_spline_option(np.array(lower_group['Orientation']),
                                                            np.array(lower_group[plot_info]))

                axs[count,].plot(x_interpol, y_interpol, '--', color=Conf[conf_type]['F_Color'])

                x_interpol, y_interpol = draw_spline_option(np.array(upper_group['Orientation']),
                                                            np.array(upper_group[plot_info]))

                axs[count,].plot(x_interpol, y_interpol, ':', color=Conf[conf_type]['F_Color'])

    count += 1

for idx, i in enumerate(info_to_plot):
    axs[idx].set_ylabel(i)
    axs[idx].set_xticks([0, 45, 90])
    axs[idx].set_xlabel('Bedding Orientation ($^\circ$)')
axs[0].legend()
fig_layout.tight_layout()

fig_layout.savefig(dir_p + r"/20221200_KA_URTEC_BuckingHorse_Characterization/HzLayout_1x3.svg")
fig_layout.show()

### INDIVIDUAL PLOTS ###

info_to_plot = ['Max Stress (MPa) ', 'Eavg (GPa)', 'Poisson Ratio (-)']
for plot_info in info_to_plot:
    fig_layout, axs = plt.subplots(figsize=(6, 6))
    for key, item in grouped_df_conf_bedding:
        for conf_type in Conf.keys():
            if key == (conf_type, "TRI") or key == (conf_type, "UCS"):
                a_group = grouped_df_conf_bedding.get_group(key)
                upper_group = a_group[a_group['Depth Bottom (m)'].lt(950)].sort_values(by='Orientation')
                lower_group = a_group[a_group['Depth Bottom (m)'].gt(950)].sort_values(by='Orientation')

                axs.scatter(lower_group['Orientation'], lower_group[plot_info], label = "LBH at %s MPa Confinement" % conf_type, marker ='.', linewidths=2.5, color=Conf[conf_type]['F_Color'])
                axs.scatter(upper_group['Orientation'], upper_group[plot_info], label = "UBH at %s MPa Confinement" % conf_type, marker ='x', linewidths=2.5, color=Conf[conf_type]['F_Color'])

                x_interpol, y_interpol = draw_spline_option(np.array(lower_group['Orientation']),
                                                            np.array(lower_group[plot_info]))

                axs.plot(x_interpol, y_interpol, '--', color=Conf[conf_type]['F_Color'])

                x_interpol, y_interpol = draw_spline_option(np.array(upper_group['Orientation']),
                                                            np.array(upper_group[plot_info]))

                axs.plot(x_interpol, y_interpol, ':', color=Conf[conf_type]['F_Color'])


    axs.set_ylabel(plot_info)
    axs.set_xticks([0, 45, 90])
    plt.xlabel('Bedding Orientation ($^\circ$)')
    plt.legend()
    fig_layout.tight_layout()

    fig_layout.savefig(dir_p + r"/20221200_KA_URTEC_BuckingHorse_Characterization/" + plot_info + '.svg')
    fig_layout.show()

### CCNBD-BD PLOTS ###

other_tests = {'BD (MPa)': {"test_type": "BD",
                            'axis_title': 'Apparent Indirect Tensile Strength (MPa)'},
               'CCNBD (MPa/m^0.5)': {"test_type": "CCNBD",
                                     'axis_title': 'Mode-I Fracture Toughness (MPa $\cdot$ m $^{0.5}$)'},
               }

colors_cycle = {"Lower Buckinghorse": {"leg_color":'orange',
                                       "leg_marker":'.'},
                "Upper Buckinghorse": {"leg_color":'blue',
                                       "leg_marker":'x'},
                }

fig_layout = plt.figure(figsize=(12, 6))
gs = fig_layout.add_gridspec(1, 2)
axs = gs.subplots(sharex=False
                  , sharey=False)
counter = 0
for plot_info in other_tests.keys():
    for key, item in grouped_df_test:
        if key == other_tests[plot_info]["test_type"]:
            a_group = grouped_df_test.get_group(key)
            upper_group = a_group[a_group['Depth Bottom (m)'].lt(950)].sort_values(by='Orientation')
            lower_group = a_group[a_group['Depth Bottom (m)'].gt(950)].sort_values(by='Orientation')

            axs[counter].scatter(lower_group['Orientation'], lower_group[plot_info], label = "LBH",
                    marker =colors_cycle["Lower Buckinghorse"]["leg_marker"],
                    color=colors_cycle["Lower Buckinghorse"]["leg_color"],
                    linewidths=2.5, )
            axs[counter].scatter(upper_group['Orientation'], upper_group[plot_info], label = "UBH",
                    marker =colors_cycle["Upper Buckinghorse"]["leg_marker"],
                    color=colors_cycle["Upper Buckinghorse"]["leg_color"],
                    linewidths=2.5, )

            # print("LOWER", lower_group['Orientation'], lower_group[plot_info])
            # print("UPPER", upper_group['Orientation'], upper_group[plot_info])
            x_interpol, y_interpol = draw_spline_option(np.array(lower_group['Orientation']), np.array(lower_group[plot_info]) )

            axs[counter].plot(x_interpol, y_interpol, '--', color=colors_cycle["Lower Buckinghorse"]["leg_color"])

            x2_interpol, y2_interpol = draw_spline_option(np.array(upper_group['Orientation']), np.array(upper_group[plot_info]) )

            axs[counter].plot(x2_interpol, y2_interpol, ':', color=colors_cycle["Upper Buckinghorse"]["leg_color"])

    counter += 1

for idx, i in enumerate(other_tests.keys()):
    axs[idx].set_ylabel(other_tests[i]['axis_title'])
    axs[idx].set_xticks([0, 45, 90])
    axs[idx].set_xlabel('Bedding Orientation ($^\circ$)')
axs[0].legend()
fig_layout.tight_layout()

fig_layout.savefig(dir_p + r"/20221200_KA_URTEC_BuckingHorse_Characterization/CCNBD_BD_1x2.svg")
fig_layout.show()