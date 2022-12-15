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
    fig1, ax1 = plt.subplots()

    lim_label = '%s%% to %s%% Density' % (str(lim1*100), str(lim2*100))

    # Density Plot with Rug Plot
    # For entire Dataframe
    sns.distplot(ind_df['Ratio'], hist = False, kde = True, rug = True,
                 color = 'green',
                 kde_kws={'linewidth': 3},
                 rug_kws={'color': 'black', 'alpha': 0.5}, label="All Data")

    # Density Plot with Rug Plot
    # For Trimmed Dataframe
    sns.distplot(ind_75['Ratio'], hist = False, kde = True, rug = True,
                 color = 'orange',
                 kde_kws={'linewidth': 3},
                 rug_kws={'color': 'blue', 'alpha': 0.5}, label=lim_label)

    # Plot formatting
    ax1.set_title('Density Rug Plot for %s' % name)
    ax1.set_xlabel('Strength Ratio (UCS:BDS)')
    ax1.set_ylabel('Density')
    ax1.legend()
    plt.savefig('/home/aly/Desktop/IF_rugmap', type='png')
    fig1.show()


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

def initial_processing(x_para, y_para, label):

    df = pd.read_excel("/hdd/home/aly/Desktop/Dropbox/RMRE - Tatone&Grasselli2014 - BD-UCS ratio Technical Note/V1/Data/123.xlsx", sheet_name="Sheet2")

    df.set_index('Type')  # Index file by Rock Type
    # print(df.Type.unique())  # Unique Rock Types
    print(bold_text("Entire Database") + "\n%s" % df.describe())

    # Dictionary to hold Rock Category
    # rocktype = {"Sedimentary": ["\tSL\t", "\tSSh\t", "\tSS\t"], "Metamorphic": ["\tMG\t", "\tMS\t", "\tMQ\t", "\tMM\t"], "Igneous": ["\tIF\t", "\tIG\t", "\tID\t"]}

    rocktype = {"Sedimentary": ["\tSS\t"]}

    # Information for Legends
    leg_info = {"SS": ['r', '^', 'Sandstone'], 'SSh': ['blue', 'o', 'Shale'], "SL": ['black', 's', 'Limestone'],
                "MG": ['r', '^', 'Gnesis'], "MS": ['green', 'D', 'Schist'], "MQ": ['blue', 'o', 'Quartzite'],
                "MM": ['black', 's', 'Marble'], "IF": ['r', '^', 'Flow Rock'], "IG": ['black', 's', 'Intrusive Rock'],
                "ID": ['blue', 'o', 'Diabase']}

    for k, v in rocktype.items():
        print(red_text("\nRock Category %s" % k))  # Rock Category

        # Figure Information
        fig, ax = plt.subplots()
        ax.loglog()  # Log-Log Scale
        plt.xlabel("BDS (MPa)")
        plt.ylabel("UCS (MPa)")
        plt.title(k)

        # Predefined Axis Limits
        xmin, xmax = 0.1, 50
        ymin, ymax = 1, 500
        # plt.ylim(ymin, ymax)
        # plt.xlim(xmin, xmax)

        # Format the x/y axis to numbers
        for axis in [ax.xaxis, ax.yaxis]:
            formatter = FuncFormatter(lambda y, _: '{:.16g}'.format(y))
            axis.set_major_formatter(formatter)

        # Auxiliary Lines
        hzlines = [5, 25, 50, 100, 250]  # Hz Lines for UCS Strength ISRM

        # Draw SLopped line to presents different Areas
        abline(8,0)  # Slope of Strength Ratio Low:Average
        abline(20, 0)  # Slope of Strength Ratio Average:High

        # Draw the Hz Lines
        for i in hzlines:
            plt.axhline(i, color='grey', linestyle='--', alpha = 0.5)

        # Load each Type in Category
        for i in v:
            # Create a Dataframe with the entire data
            df1 = df[df['Type'] == i]
            nn = i.strip('\t')

            # The two independent variables
            m1 = df1['BDS']  # BD
            m2 = df1['UCS']  # UCS

            # Rock Category // Type
            # Print Information
            print(red_text("\t%s - %s" % (nn, leg_info[nn][2])))
            print(bold_text("\tTotal # of Tests\t%s" % df1.shape[0]))
            print("\tTest\tMax\t\tMin")
            print("\tBD:\t\t%s\t%s" % (m1.max(), m1.min()))
            print("\tUCS:\t%s\t%s" % (m2.max(), m2.min()))

            # Describe Entire Dataframe
            print(df1.describe())

            # Trim Data between lim1-lim2
            df2 = df1[(df1.Ratio.quantile(lim1) <= df1.Ratio) &  (df1.Ratio <= df1.Ratio.quantile(lim2))]
            print(df2.describe())

            # Plot the Density-Rug Plots
            # To compare the Original & Trimmed Dataframe
            plot_histo(df1, df2, nn)

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
        plt.savefig('/home/aly/Desktop/IF_Kernel', type='png')
        plt.show()



'''
MAIN MODULE

- Returns total time and Error on user termination.
'''

if __name__ == "__main__":
    try:
        initial_processing()
        print("\nTotal Execution time: \033[1m%s\033[0m\n" % calc_timer_values(time.time() - abs_start))
    except KeyboardInterrupt:
        exit("TERMINATED BY USER")
