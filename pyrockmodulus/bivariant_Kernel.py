# /////////////////////////////////////////////////////////////// #
# !python3.6
# -*- coding: utf-8 -*-
# Python Script initially created on 8/24/2020
# Compiled by Aly @ Grasselli's Geomechanics Group, UofT, 2020
# Created using PyCharm // Tested on Spyder
# Current Version 06 - Dated August 21, 2018
# /////////////////////////////////////////////////////////////// #

import time
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
from sklearn.neighbors import KernelDensity
import scipy.stats as st
# from sklearn.datasets.samples_generator import make_blobs
import seaborn as sns
import pandas as pd

# START OF EXECUTION
abs_start = time.time()

my_path = os.path.dirname(
    os.path.abspath(__file__))  # Figures out the absolute path for you in case your working directory moves around.


'''
Default MATPLOTLIB Fonts
'''

# plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams["figure.figsize"] = [8, 8]
matplotlib.rcParams['font.family'] = ['arial']
matplotlib.rcParams['font.size'] = 10


'''
Global Parameters 
'''

global lim1, lim2
lim1= 0.25
lim2= 0.75


'''
TIMER FUNCTION
'''


def calc_timer_values(end_time):
    minutes, sec = divmod(end_time, 60)
    if end_time < 60:
        return "\033[1m%.2f seconds\033[0m" % end_time
    else:
        return "\033[1m%d minutes and %d seconds\033[0m." % (minutes, sec)


'''
FORMATTING OPTIONS

- TEXT COLORS
'''


def red_text(val):  # RED Bold text
    tex = "\033[1;31m%s\033[0m" % val
    return tex


def green_text(val):  # GREEN Bold text
    tex = "\033[1;92m%s\033[0m" % val
    return tex


def bold_text(val):  # Bold text
    tex = "\033[1m%s\033[0m" % val
    return tex


'''
Density Rug Plot
Compares the Entire Dataframe vs. Trimmed Dataframe
Trimmed Dataframe is a percentile range
lim1 to lim2 
'''

def plot_histo(ind_df, ind_75, name):
    # print("Here", ind_df)
    fig_rug, ax_rug = plt.subplots()

    lim_label = '%s%% to %s%% Density' % (str(lim1*100), str(lim2*100))

    sns.kdeplot(data=ind_df, x="BDS", y="UCS", cut=0)

    # sns.kdeplot(ind_df["Ratio"], color = 'green', label="All Data", lw=3)
    # sns.rugplot(ind_df["Ratio"], color='black', alpha=0.5)
    # sns.kdeplot(ind_75["Ratio"], color = 'orange', label=lim_label, lw=3)
    # sns.rugplot(ind_75["Ratio"], color='blue', alpha=0.5)

    # Plot formatting
    ax_rug.set_title('Density Rug Plot for %s' % name)
    ax_rug.set_xlabel('BDS')
    ax_rug.set_ylabel('UCS')
    ax_rug.legend()
    ax_rug.set_xlim(0)

    ax_rug.set_ylim(0)
    plt.savefig(os.path.join(my_path, "Images", "Rug_plot_" + name + '.pdf'))
    # plt.savefig('/home/aly/Desktop/IF_rugmap', type='png')
    fig_rug.show()
    # exit('Rug Plot')

'''
Plot a line from slope and intercept
'''


def abline(slope, intercept):
    axes = plt.gca()  # Get axis limits
    x_vals = np.array(axes.get_xlim())  # Array the X as values from xlim
    y_vals = intercept + slope * x_vals  # Get y values based on mx + c
    # Plot the mx+c line within axis limits
    plt.plot(x_vals, y_vals, color='grey', alpha=0.5, linestyle='--')


'''
Process the file
'''

def initial_processing(db, m1, m2, x_para, y_para, x_lab, y_lab, label):
    # # print(db)
    # # fig_box, ax_box = plt.subplots(figsize=(10, 8))
    # # plt.suptitle('')
    # #
    # # db.boxplot(column=['Ratio'])
    # # fig_box.show()
    # # exit()
    #
    # print(x_lab, y_lab, label)
    # print(x_para, y_para,)
    # print(db)
    #
    # print(red_text("\nRock Category %s" % label))  # Rock Category
    #
    # # Figure Information
    # fig_sns, ax_sns = plt.subplots()
    # ax_sns.loglog()  # Log-Log Scale
    # plt.xlabel(x_lab)
    # plt.ylabel(y_lab)
    # plt.title(label)
    #
    #     # Predefined Axis Limits
    # xmin, xmax = 0.1, 50
    # ymin, ymax = 1, 500
    # # plt.ylim(ymin, ymax)
    # # plt.xlim(xmin, xmax)
    #
    # # Format the x/y axis to numbers
    # for axis in [ax.xaxis, ax.yaxis]:
    #     formatter = FuncFormatter(lambda y, _: '{:.16g}'.format(y))
    #     axis.set_major_formatter(formatter)
    #
    # # Auxiliary Lines
    # hzlines = [5, 25, 50, 100, 250]  # Hz Lines for UCS Strength ISRM
    #
    # # Draw SLopped line to presents different Areas
    # abline(8,0)  # Slope of Strength Ratio Low:Average
    # abline(20, 0)  # Slope of Strength Ratio Average:High
    #
    # # Draw the Hz Lines
    # for i in hzlines:
    #     plt.axhline(i, color='grey', linestyle='--', alpha = 0.5)
    #
    # # Describe Entire Dataframe
    # print(db.describe())

    # Trim Data between lim1-lim2
    df2 = db[(db.Ratio.quantile(lim1) <= db.Ratio) &  (db.Ratio <= db.Ratio.quantile(lim2))]
    print(df2.describe())

    # Plot the Density-Rug Plots
    # To compare the Original & Trimmed Dataframe
    plot_histo(db, df2, label)
    # exit()
    return

    mx = df2['BDS']
    my = df2['UCS']


    # print(xmin, xmax, ymin, ymax)
    # Create meshgrid
    # Smoothness of the Kernel
    xx, yy = np.mgrid[xmin:xmax:300j, ymin:ymax:300j]
    d = 1
    n = len(mx)
    bw_rec_value = (n * (d + 2) / 4.)**(-1. / (d + 4))

    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([mx, my])

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html
    # https://towardsdatascience.com/simple-example-of-2d-density-plots-in-python-83b83b934f67
    kernel = st.gaussian_kde(values, bw_method="silverman")
    # kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)

    #
    cfset = ax.contourf(xx, yy, f, cmap='coolwarm')
    # ax.imshow(np.rot90(f), cmap='coolwarm', extent=[xmin, xmax, ymin, ymax])
    cset = ax.contour(xx, yy, f, cmap='coolwarm')
    # ax.clabel(cset, inline=1, fontsize=10)
    # plt.title('2D Gaussian Kernel density estimation')
    #
    # ax.set_xlim(0.1)
    # ax.set_ylim(ymin, ymax)
    # cfset = ax.contourf(xx, yy, f, cmap='coolwarm')
    # ax.imshow(np.rot90(f), cmap='coolwarm', extent=[xmin, xmax, ymin, ymax])
    #
    # cset = ax.contour(xx, yy, f, colors='white')
    # ax.clabel(cset, inline=1, fontsize=10)
    # ax.set_xlabel('BD (MPa)')
    # ax.set_ylabel('UCS (MPa)')
    # plt.title('2D Gaussian Kernel density estimation')
    # plt.show()



    # ax = fig.gca()


    plt.scatter(m1, m2, label=nn, facecolors='none', edgecolors=leg_info[nn][0], marker=leg_info[nn][1])
    # for j in range(len(cset.allsegs)):
    #     for ii, seg in enumerate(cset.allsegs[j]):
    #         # plt.plot(seg[:, 0], seg[:, 1], '-', label=f'Cluster{j}, level{ii}', )
    #         if j == 2:
    #             plt.plot(seg[:, 0], seg[:, 1], '-', color=leg_info[nn][0],label='KDE - %s' % nn)

    plt.legend()
    plt.savefig(os.path.join(my_path, "Images", "Rug_plot" + "1" + '.pdf'))
    plt.show()



'''
MAIN MODULE

- Returns total time and Error on user termination.
'''

if __name__ == "__main__":
    try:
        # initial_processing()
        print("\nTotal Execution time: \033[1m%s\033[0m\n" % calc_timer_values(time.time() - abs_start))
    except KeyboardInterrupt:
        exit("TERMINATED BY USER")
