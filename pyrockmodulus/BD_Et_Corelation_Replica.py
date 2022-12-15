import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import time
import math
import bivariant_Kernel

# Load UCS Strength Criterion py file
import ucs_descriptions

# START OF EXECUTION
abs_start = time.time()

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
Default MATPLOTLIB Fonts
'''

# plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams["figure.figsize"] = [8, 8]
matplotlib.rcParams['font.family'] = ['arial']
matplotlib.rcParams['font.size'] = 12

my_path = os.path.dirname(
    os.path.abspath(__file__))  # Figures out the absolute path for you in case your working directory moves around.

# Load markers if needed
type_marker = {}
markers = ['o', 'v', '^', '<', '>', 'P', 'd', '*', '8']

# Dictionary to hold Rock Type
rocktype_deere_miller = {"Diabase": ["Igneous", 'blue', 'ID'],
                         "Granite": ["Igneous", 'black', "IG"],
                         "Basalt": ["Igneous", 'red', "IF"],
                         "Quartzite": ["Metamorphic", 'blue', ],
                         "Gneiss": ["Metamorphic", 'red', "MG"],
                         "Marble": ["Metamorphic", 'black', "MM"],
                         "Schist_Flat": ["Metamorphic", 'darkgreen', "MSpp"],
                         "Schist_Perp": ["Metamorphic", 'olive', "MSpl"],
                         "Limestone": ["Sedimentary", 'black', "SL"],
                         "Mudstone": ["Sedimentary", 'grey', "SSh"],
                         "Sandstone": ["Sedimentary", 'red', "SS"],
                         "Shale": ["Sedimentary", 'blue', 'SSh']}

# Dictionary to hold Rock Category
# Change rock type as needed
rock_type = {"Sedimentary": ["SL", "SSh", "SS"], "Metamorphic": ["MG", "MS", "MQ", "MM"], "Igneous": ["IG", "IF", "ID"]}
replica_type = {'Replica': ['Replica']}

# Information for Legends
leg_info = {"SS": ['r', '^', 'Sandstone'], 'SSh': ['blue', 'o', 'Shale'], "SL": ['black', 's', 'Limestone'],
            "MG": ['r', '^', 'Gneiss'], "MS": ['green', 'D', 'Schist'], "MSpl": ['green', 'D', 'Schist Parallel'],
            "MSpp": ['green', 'D', 'Schist Perpendicular'], "MQ": ['blue', 'o', 'Quartzite'],
            "MM": ['black', 's', 'Marble'], "IF": ['r', '^', 'Flow Rock'], "IG": ['black', 's', 'Intrusive Rock'],
            "ID": ['blue', 'o', 'Diabase'], "Replica": ['r', '^', 'Replica']}

# Predefined Axis Limits
xmin, xmax = 0.1, 50
ymin, ymax = 1, 500

'''
Load Data
- INPUTS
    # Name of file for Deere Miller
    # Name of file for Rock Database entries
-OUTPUTS
    # Loaded data as Global Variables
    # Digitized plots as a dictionary
'''


def load_data(df_deere_miller_data, df_db_data, db_to_load):
    global df_deere_miller, db_deere_miller, df_db
    global rocktype
    # Load deere-miller digitized plots
    # Data digitization courtesy of Rohatgi, Ankit. "WebPlotDigitizer." (2017).
    df_deere_miller = pd.read_csv(os.path.join(my_path, 'Data', df_deere_miller_data), header=None)

    # Load UCS-BD-Et Database
    if db_to_load == "Rock":
        # Load UCS-BD-Et Database
        df_db = pd.read_excel(os.patzdh.join(my_path, 'Data', df_db_data), sheet_name="Database", header=0)
        rocktype = rock_type
    else:
        # Load REPLICA Database
        df_db = pd.read_excel(os.path.join(my_path, 'Data', df_db_data), sheet_name="Replica", header=0)
        rocktype = replica_type

    # Load the deere-miller as a dictionary
    db_deere_miller = {}

    for i in range(0, len(df_deere_miller.columns), 2):
        name = df_deere_miller.iloc[0, i]
        a = pd.Series(df_deere_miller.iloc[:, i].iloc[2:], dtype='float')  # column of data frame
        b = pd.Series(df_deere_miller.iloc[:, i + 1].iloc[2:], dtype='float')  # column of data frame (last_name)
        db_deere_miller[name] = [a, b]


'''
Function to plot by Author
- INPUTS
    # Dataframe
    # X Variable 
    # Y Variable
    # X Label
    # Y Label
    # r_type - Rock Type
    # r_cat - Rock Category
-OUTPUTS
    # Graphs for each Rock Type
    # Grouped by Author
'''


def plot_by_author(db_to_plot, x_para, y_para, x_lab, y_lab, r_type, r_cat, ax, state=''):
    if state:
        n_of_authors = len(db_to_plot['ReplicaType'])
        print(n_of_authors)
        print(db_to_plot['CiteName'])
    else:
        n_of_authors = len(db_to_plot.groupby(['CiteName']))
    # Initialise figure and X/Y Labels
    # fig1, ax = plt.subplots()

    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    # Initialise color spectrum for scatter
    colors = iter(cm.tab20(np.linspace(0, 1, n_of_authors)))

    # Group database by Author/Publications

    # For the replica, division is made by Author and sub-category by Replica Type
    # For any other, division is made by Author
    if state:
        # ReplicaType is for the Marker Type
        for idx, key in enumerate(db_to_plot['ReplicaType'].unique()):
            if key == 'Flowstone':
                type_marker[key] = 's'
            else:
                type_marker[key] = markers[idx]
        counter = 0
        print(type_marker)
        # Plot by Author
        for key, grp in db_to_plot.groupby(['CiteName']):
            if key == 'Tatone, 2014':
                ax.scatter(grp[x_para], grp[y_para], label=grp['CiteName'].values[0], color='k', edgecolors='k', marker='s')
            else:
                ax.scatter(grp[x_para], grp[y_para], color=next(colors), label="%s" % key, marker=type_marker[grp['ReplicaType'].values[0]])
            counter += 1
        # Dummy secondary axis for additional legend
        ax2 = ax.twinx()
        for x, y in type_marker.items():
            ax2.scatter(np.NaN, np.NaN, marker=y, label=x, color='black')
        # Formatting for the secondary axis
        ax2.get_yaxis().set_visible(False)
        # Formatting for the legend
        leg = ax2.legend(loc=4, title=r'$\bf{Replica}$', title_fontsize=12, fontsize=12)
        ax.legend(loc=2, title=r'$\bf{Author}$', title_fontsize=12, fontsize=12)

        plt.draw()  # Draw the figure so you can find the positon of the legend.

        # # Get the bounding box of the original legend
        # # ax.figure.canvas.draw()
        # bb = leg.get_bbox_to_anchor().inverse_transformed(ax.transAxes)
        #
        # # Change to location of the legend.
        # xOffset = 0.05
        # bb.x0 -= xOffset
        # bb.x1 -= xOffset
        # leg.set_bbox_to_anchor(bb, transform=ax.transAxes)


    # # Format primary axis
    for i, axax in enumerate(plt.gcf().get_axes()):
        if i != 0:
            format_axis(axax, 'Secondary')



'''
Function V Lines based on UCS Description Loaded
- INPUTS
    # Locations of V Lines
    # Axis to plot
-OUTPUTS
    # V Lines in the plot
    # Annotations for the UCS Strength Criteria
'''


def plot_v_lines(vlines, ax):
    for i in vlines:
        plt.axhline(i, color='grey', linestyle='--', alpha=0.5)
    # Annotate the UCS Strength Criteria adopted
    for r_type_val in range(0, len(category_values) - 1):
        # Horizontal line at 80% of xmax
        plt.axvline(x=0.8 * xmax, color='grey', linestyle='--')
        # Annotate only the values that lie in the range
        if category_values[r_type_val + 1] > ymin:
            if category_values[r_type_val + 1] > ymax:  # Condition that value > axis limit
                ax.text(math.sqrt(xmax * (0.8 * xmax)), math.sqrt(ymax * category_values[r_type_val]),
                        category_names[r_type_val], ha='center', va='center', color='g', fontweight='bold')
            elif category_values[r_type_val] < ymin:  # Condition that value < axis limit
                ax.text(math.sqrt(xmax * (0.8 * xmax)), math.sqrt(ymin * category_values[r_type_val + 1]),
                        category_names[r_type_val], ha='center', va='center', color='g', fontweight='bold')
            else:  # Values in between
                ax.text(math.sqrt(xmax * (0.8 * xmax)),
                        math.sqrt(category_values[r_type_val + 1] * category_values[r_type_val]),
                        category_names[r_type_val], ha='center', va='center', color='g',
                        fontweight='bold')


'''
Function Sloped Lines
Using mx + c
- INPUTS
    # Slope
    # Intercept
    # State (Line OR Text)
    # Multiplier
    # Text to print on graph
    # Axis to plot
-OUTPUTS
    # V Lines in the plot
    OR
    # Text on plot
'''


def abline(slope, intercept, dr_state, multiplier=1, ratio='', ax=None):
    axes = plt.gca()  # Get axis limits
    x_vals = np.array(axes.get_xlim())  # Array the X as values from xlim
    y_vals = intercept + (slope / multiplier) * x_vals  # Get y values based on mx + c
    x_text_loc = 0.15  # X-Location of text
    txt_slope = np.rad2deg(np.arctan2(np.log(ymax-ymin), np.log(xmax-(xmin))))
    # Plot the mx+c line within axis limits
    # Y-value of text based on mx+c where X is predefined
    if dr_state == "line":
        ax.plot(x_vals, y_vals, color='grey', alpha=0.5, linestyle='--', zorder=-1)
        # Add the text to the sloped line
        ax.text(x_text_loc, intercept + (slope / multiplier) * x_text_loc, '{:d}:1'.format(int(slope)), rotation=txt_slope, bbox=dict(facecolor='white', edgecolor="white"))
    if dr_state == "text":
        # Add the text to category
        ax.text(x_text_loc, intercept + (slope / multiplier) * x_text_loc,  ratio, rotation=txt_slope, alpha=0.5)


'''
Function Plot Deere Miller Clusters

- INPUTS
    # r_type - Rock Type
    # ax - Axis to plot on
    # State - if not empty will plot all clusters the defined key 
    (Sedimentary, Igneous, Metamorphic)
-OUTPUTS
    # Deere Miller Clusters
'''


def deere_miller_clusters(r_type, ax, state=''):
    print("\tPlotting Deere Miller Clusters")
    # If Replica plot all the Rock Type name (k) and cluster area (v)
    if state:
        for k, v in rocktype_deere_miller.items():
            if v[0] == state:
                plot_clusters(k, v, ax)
    # Load k,v pair as Rock Type name (k) and cluster area (v)
    for k, v in rocktype_deere_miller.items():
        if v[0] == r_type:
            plot_clusters(k, v, ax)


def plot_clusters(k, v, ax):
    # For Shale and Sandstone, plot open ended clusters
    if k in ['Sandstone', 'Shale']:
        ax.plot(db_deere_miller[k][0], db_deere_miller[k][1], alpha=0.5, label=k, color=v[1], linewidth=2,
                linestyle='--')
    # Schist has 2 areas
    elif k == 'Schist_Perp':
        ax.fill(db_deere_miller['Schist_Perp'][0], db_deere_miller['Schist_Perp'][1], fill=False, alpha=0.5,
                label='Schist Perpendicular', color=v[1], linewidth=2)
    elif k == 'Schist_Flat':
        ax.fill(db_deere_miller['Schist_Flat'][0], db_deere_miller['Schist_Flat'][1], fill=False, alpha=0.5,
                label='Schist Parallel', color=v[1], linewidth=2)
    else:
        ax.fill(db_deere_miller[k][0], db_deere_miller[k][1], fill=False, alpha=0.5, label=k, color=v[1], linewidth=2)


'''
Function Format log-log Axis
- INPUTS
    # ax - Axis to plot on
    # state to enable to disable slopped lines
-OUTPUTS
    # Formatted Axis
'''


def format_axis(ax, state='', major_axis_vline = False):
    # Draw axis limits
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # Log-Log Scale
    ax.loglog()
    ax.grid(major_axis_vline, alpha=0.25, zorder=-1)
    # Format the Number to XX format for X and Y axis
    for axis in [ax.xaxis, ax.yaxis]:
        formatter = FuncFormatter(lambda ax_lab, _: '{:.16g}'.format(ax_lab))
        axis.set_major_formatter(formatter)

    if not state:
        # Draw SLopped line to presents different Areas
        abline(200 , 0, "line", 1000, '', ax)  # Slope of Strength Ratio Low:Average MPa to GPa
        abline(500 , 0, "line", 1000, '', ax)  # Slope of Strength Ratio Average:High MPa to GPa

        # Text to Classify the MR domains
        abline(800 , 0, "text", 1000, "High MR",ax)  # High MR
        abline(math.sqrt(200*500), 0, "text",1000, 'Average MR', ax)  # Average MR
        abline(100, 0, "text", 1000, 'Low MR',ax)  # Low MR


'''
Function to plot 
# all-plot => 
- INPUTS
    # Dataframe
    # X Variable 
    # Y Variable
    # X Label
    # Y Label
    # ucs_type - UCS Strength Criteria adopted 
    # db_to_load - Load "Rock" or "Replica" database
-OUTPUTS
    # Graphs for each Rock Type
    # Grouped by Author
'''


def initial_processing(x_para, y_para, x_lab, y_lab, ucs_type, db_to_load, all_plot=False):
    # Load the data Deere Miller digitized plots and Rock Database entries
    load_data("Digitized_deere_miller.csv", "rock_database.xlsx", db_to_load)

    # Load information for UCS Strength Criteria adopted
    global category_names, category_values
    category_names, category_values = ucs_descriptions.ucs_strength_criteria(ucs_type)

    fig_all_points, ax_all_points = plt.subplots(figsize=(8, 8))
    format_axis(ax_all_points)
    # plot_v_lines(category_values, ax_all_points)

    print("\tSummary of Individual Points from Database")

    # Loop through Rock Types and their Subcategories
    for r_type, r_sub_cats in rocktype.items():
        df_db['RockMainType1'] = r_type
        df_db[df_db['Type'].isin(r_sub_cats)].dropna(how='all', subset=['Ratio'])
        print(red_text(r_type))

        r_cat = "Replica"
        rocktype_db = df_db[df_db['Type'] == r_cat].dropna(how='any', subset=[x_para, y_para])

        # Plot Points by Author for Individual Rock Type
        # if r_type == 'Replica':
        plot_by_author(rocktype_db, x_para, y_para, x_lab, y_lab, r_cat, r_type, ax_all_points, 'All')

        deere_miller_clusters(r_type, ax_all_points, 'Sedimentary')
        df_db_rock = pd.read_excel(os.path.join(my_path, 'Data', "rock_database.xlsx"), sheet_name="Database", header=0)
        rocktype_rocks = rock_type
        print(rocktype_rocks)

    # Cosmetics to the figure and layouts
    ax_all_points.set_xlabel(x_lab)
    ax_all_points.set_ylabel(y_lab)

    fig_all_points.tight_layout()

    fig_all_points.savefig(os.path.join(my_path, 'Images', "Replica_%s_%s.pdf" % (x_para, y_para)))
    fig_all_points.show()


'''
MAIN MODULE
- Returns total time and Error on user termination.
'''

if __name__ == "__main__":
    try:
        # Names of files are defined in initial_processing - load_data module
        # INPUT x_para, y_para, x_para name, y_para name,  UCS Strength Criteria adopted, "Rock"//"Replica"
        initial_processing('Et', 'UCS', 'Et$_{50}$ (GPa)', 'UCS (MPa)', 'ISRMCAT\n1979', "Replica")
        print("\nTotal Execution time: \033[1m%s\033[0m\n" % calc_timer_values(time.time() - abs_start))
    except KeyboardInterrupt:
        exit("TERMINATED BY USER")