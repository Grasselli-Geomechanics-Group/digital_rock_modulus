# /////////////////////////////////////////////////////////////// #
# !python3.6
# -*- coding: utf-8 -*-
# Python Script initially created on 7/7/2020
# Compiled by Aly @ Grasselli's Geomechanics Group, UofT, 2020
# /////////////////////////////////////////////////////////////// #

import time
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

# Load UCS Strength Criterion py file
try:
    from . import rock_variables
except ImportError:
    import rock_variables

# Load Formatting Codes py file
try:
    from . import formatting_codes
except ImportError:
    import formatting_codes

'''
Default MATPLOTLIB Fonts
'''

plt.rcParams["figure.figsize"] = [12, 5]
matplotlib.rcParams['font.family'] = ['arial']
matplotlib.rcParams['font.size'] = 8


def initial_processing():
    """
    Load the UCS Strength Criterion and plot them in a Horizontal Bar Chart with the various criteria

    :return: Matplotlib AxesSubplots
    :rtype: Matplotlib Axis
    """

    # Initialise Figure
    fig, ax = plt.subplots()

    # Load All UCS Strength criteria by passing '' as type
    category_names, category_values, converted_psi = rock_variables.ucs_strength_criteria('')

    print("A total of %s UCS Strength criteria identified." % formatting_codes.bold_text(len(category_names.keys())))

    # Variable to leave gaps between the various criteria on the plot
    initial_gap = 0.5
    bar_width = 0.75
    c_list = []

    ## Prepare for the Category Reference ##
    # List of the Name of the Reference
    # psi to MPa conversion are marked with an *
    for k in category_names.keys():
        if k in converted_psi:
            c_list.append(k + str("*"))
        else:
            c_list.append(k)

    # List of the Y Locations of the Reference
    c_loc = []
    for i in range(0, len(c_list)):
        c_loc.append(initial_gap + (bar_width / 2) + i)

    plt.semilogx()  # Plot in semi-log domain

    # Plot the Horizontal Bar for each Category
    for counter, (k, v) in enumerate(category_values.items()):
        for i in range(0, len(v)-1):
            if i in [0, len(v)-2]:
                # Draw a line at the end of the category to show its continuity
                ax.annotate('', xy=(1000, 1 + counter - (bar_width * 3 / 2)),
                            xycoords='data',
                            xytext=(750, 1 + counter - (bar_width * 3 / 2)),
                            textcoords='data',
                            horizontalalignment='center',
                            verticalalignment='center',
                            arrowprops=dict(arrowstyle='->',
                                            color='k',
                                            lw=0.5,
                                            ls='-')
                            )
            # Plot a Rectangle for each category
            rectangle = plt.Rectangle((v[i], 0 + counter - 0.5), v[i+1] - v[i], bar_width, fc='white', ec="black", lw=1.0, linestyle='-')
            # Add the Rectangle to the plot
            plt.gca().add_patch(rectangle)
            # Insert the category name in the center of hte Rectangle.
            # Center is calculated for a log scale
            ax.text(math.sqrt(v[i + 1] * v[i]), 1 + counter - (bar_width * 3 / 2), category_names[k][i], ha='center', va='center',
                    color='g', fontweight='bold')

    # Format Plot the tick marks for the X axis
    # Changes from the scientific mode to normal number mode
    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.ticklabel_format(style='plain', axis='x', useOffset=False)

    # Format Plot the tick marks for the Y axis
    ax.set_yticks(c_loc)
    ax.set_yticklabels([x for x in c_list])
    # Format Plot the tick marks for the Y axis - Produced UserWarning
    # ax.yaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(c_list))
    # ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(c_loc))

    # Enable the tick marks for the X axis on both the top and bottom with the values.
    ax.tick_params(bottom=True, top=True)
    ax.tick_params(labelbottom=True, labeltop=True)

    # X axis Label
    ax.set_xlabel("Unconfined Compressive Strength (MPa)")

    # Plot Limits and Axis
    plt.grid(which='major', axis='x', linestyle=':', linewidth=0.5)  # Major Axis
    plt.xlim(0.2,1000)
    plt.ylim(0, len(category_names.keys())+1 )
    plt.tight_layout()

    return ax


'''
MAIN MODULE

- Returns total time and Error on user termination.
'''

if __name__ == "__main__":
    try:
        initial_processing()
    except KeyboardInterrupt:
        exit("TERMINATED BY USER")