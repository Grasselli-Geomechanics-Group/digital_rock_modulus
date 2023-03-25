import math
import os
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

try:
    from . import formatting_codes
except ImportError:
    import formatting_codes
# Load UCS Strength Criterion py file
try:
    from . import rock_variables
except ImportError:
    import rock_variables

# START OF EXECUTION
abs_start = time.time()

'''
Default MATPLOTLIB Fonts
'''

# plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams["figure.figsize"] = [6, 6]
matplotlib.rcParams['font.family'] = ['arial']
matplotlib.rcParams['font.size'] = 12

my_path = os.path.dirname(
    os.path.abspath(__file__))  # Figures out the absolute path for you in case your working directory moves around.


##TODO:
# Allow to reset the xaxis and yaxis and house all the information (MR and SR)
# Allow to change the colors and have more control over what to plot in terms of sub-category of the rock type (MR and SR)

class modulus_ratio:
    """
    Based on the classification of Deere DU, Miller RP. Engineering Classification and Index Properties for Intact Rocks. Fort Belvoir, VA: Defense Technical Information Center; 1966.
    Data digitization courtesy of Rohatgi, Ankit. "WebPlotDigitizer." (2017).

    # ADVANCED: By assigning the *_rocktype_dictionary* variable, more control over the clusters being plotted is gained.
    """

    # Load default variables
    _rocktype_dictionary = rock_variables._rocktype_dictionary

    def _load_data(self, df_type='MR'):
        """
        Load the file that holds the digital deere_miller cluster points. This information will be used to plot the deere-miller clusters based on the user requirements.

        :param df_type: variable to load. MR = Deere Miller; SR = Tatone et. al. 
        :type df_type: str

        :return: dictionary containing the type of rock and the points that form its cluster.
        :rtype: dict
        
        
        """

        # global df_deere_miller

        # Data digitization courtesy of Rohatgi, Ankit. "WebPlotDigitizer." (2017).
        # Initialise the deere-miller digitized plots as a dictionary
        db_deere_miller = {}
        if df_type == 'MR':
            db_deere_miller_list = rock_variables._rock_deere_miller_points
        elif df_type == 'SR':
            db_deere_miller_list = rock_variables._rock_tatone_et_al_points
        else:
            raise KeyError("Unknown clusters to plot.")

        # Convert the dictionary in rock_variables.py to a panda.series
        for k, v in db_deere_miller_list.items():
            a_panda = pd.Series(list(v[0].values()))
            b_panda = pd.Series(list(v[1].values()))
            db_deere_miller[k] = [a_panda, b_panda]

        return db_deere_miller

    def plot_v_lines(self, vlines, ax):
        """
        Plot lines and annotate the UCS Strength Criteria adopted

        :param vlines: Locations of V Lines
        :type vlines: list[float]
        :param ax: Axis to plot
        :type ax: matplotlib

        :return:
        :rtype:
        """

        for i in vlines:
            plt.axvline(i, color='grey', linestyle='--', alpha=0.5)
        # Annotate the UCS Strength Criteria adopted
        for r_type_val in range(0, len(category_values) - 1):
            # Horizontal line at 80% of ymax
            plt.axhline(y=0.8 * self._ymax, color='grey', linestyle='--', alpha=0.5, zorder=-1)
            # Annotate only the values that lie in the range
            if category_values[r_type_val + 1] > self._xmin and category_values[r_type_val] <= self._xmax:
                if category_values[r_type_val + 1] > self._xmax:  # Condition that value > axis limit
                    ax.text(math.sqrt(self._xmax * category_values[r_type_val]),
                            math.sqrt(self._ymax * (0.8 * self._ymax)),
                            category_names[r_type_val], ha='center', va='center', color='g', fontweight='bold')
                elif category_values[r_type_val] < self._xmin:  # Condition that value < axis limit
                    ax.text(math.sqrt(self._ymin * category_values[r_type_val + 1]),
                            math.sqrt(self._ymax * (0.8 * self._ymax)),
                            category_names[r_type_val], ha='center', va='center', color='g', fontweight='bold')
                else:  # Values in between
                    ax.text(math.sqrt(category_values[r_type_val + 1] * category_values[r_type_val]),
                            math.sqrt(self._ymax * (0.8 * self._ymax)), category_names[r_type_val], ha='center',
                            va='center', color='g',
                            fontweight='bold')

    def abline(self, slope, intercept, dr_state, multiplier=1, ratio='', ax=None, x_text_loc=0.15):
        """
        Function to plot the slopped lines based on a slope and a y-intercept, basically mx+c. It is defined to form the Low/Avg/High MR ratio in the deere-miller classification plot.

        :param slope: the slope of the line
        :type slope: float
        :param intercept: the intercept of the lube
        :type intercept: float
        :param dr_state: draw state to move between the line drawing and the placement/writing of the text. Options [Line, Text]
        :type dr_state: str
        :param multiplier: in case of a need of a multiplier
        :type multiplier: int
        :param ratio: text associated with the MR modulus
        :type ratio: str
        :param ax: Matplotlib Axis
        :type ax: matplotlib
        :param x_text_loc: slope to write text
        :type x_text_loc: float

        :return:
        :rtype:
        """

        # Get axis limits
        axes = plt.gca()

        # Array the X as values from xlim
        x_vals = np.array(axes.get_xlim())

        # Get y values based on mx + c
        y_vals = intercept + (slope / multiplier) * x_vals

        # X-Location of text
        txt_slope = np.rad2deg(np.arctan2(np.log(self._ymax - self._ymin), np.log(self._xmax - (self._xmin))))

        # Plot the mx+c line within axis limits
        # Y-value of text based on mx+c where X is predefined
        if dr_state == "line":
            ax.plot(x_vals, y_vals, color='grey', alpha=0.5, linestyle='--', zorder=-1)
            # Add the text to the sloped line
            ax.text(x_text_loc, intercept + (slope / multiplier) * x_text_loc, '{:d}:1'.format(int(slope)),
                    rotation=txt_slope, bbox=dict(facecolor='white', edgecolor="white"))
        # Add the text to category
        if dr_state == "text":
            ax.text(x_text_loc, intercept + (slope / multiplier) * x_text_loc, ratio, rotation=txt_slope, alpha=0.5)

    def deere_miller_clusters(self, ax, df_of_clusters_deere_miller, r_type=None, plot_all_clusters_bool=False):
        """
        Load information needed to plot

        :param ax: Axis to plot on
        :type ax: matplotlib
        :param df_of_clusters_deere_miller: will plot defined cluster. Options Sedimentary, Igneous, Metamorphic.
        :type df_of_clusters_deere_miller: dict
        :param r_type: Define the rock type to be plotted. plot_all_clusters_bool MUST be false.
        :type r_type: str
        :param plot_all_clusters_bool: Plot all the clusters.
        :type plot_all_clusters_bool: bool

        :return:
        :rtype:
        """

        if not plot_all_clusters_bool and r_type == '':
            raise IndexError(
                "If all clusters is disabled, the cluster to plot must be defined. df_of_clusters_deere_miller option should be Sedimentary, Igneous, Metamorphic")
        elif plot_all_clusters_bool and r_type != None:
            raise IndexError(
                "If all clusters is enabled. r_type should not be specified.")

        # Load dictionary of all the clusters and their default plotting information.
        if plot_all_clusters_bool:
            # Plot all k,v pair as Rock Type name (k) and cluster area (v)
            for k, v in rock_variables._rocktype_dictionary.items():
                modulus_ratio.plot_clusters(self, k, v, ax, df_of_clusters_deere_miller)
        else:
            # Load k,v pair as Rock Type name (k) and cluster area (v)
            for k, v in rock_variables._rocktype_dictionary.items():
                if v[0] == r_type:
                    modulus_ratio.plot_clusters(self, k, v, ax, df_of_clusters_deere_miller)

    def plot_clusters(self, k, v, ax, df_of_clusters_deere_miller):
        """
        Plot the clusters

        :param k: key
        :type k: str
        :param v: value
        :type v: str
        :param ax: Axis to plot on
        :type ax: matplotlib
        :param df_of_clusters_deere_miller: dictionary containing the type of rock and the points that form its cluster.
        :type df_of_clusters_deere_miller: dict

        :return:
        :rtype:
        """

        # For Shale and Sandstone, plot open-ended clusters
        if k not in df_of_clusters_deere_miller.keys():
            return
        else:
            if k in ['Sandstone', 'Shale']:
                ax.plot(df_of_clusters_deere_miller[k][0], df_of_clusters_deere_miller[k][1], label=k, color=v[1],
                        linewidth=1,
                        linestyle='--')
            # Schist has 2 areas
            elif k == 'Schist_Perp':
                ax.fill(df_of_clusters_deere_miller['Schist_Perp'][0], df_of_clusters_deere_miller['Schist_Perp'][1],
                        fill=False,
                        label='Schist Perpendicular', color=v[1], linewidth=1, linestyle='--')
            elif k == 'Schist_Flat':
                ax.fill(df_of_clusters_deere_miller['Schist_Flat'][0], df_of_clusters_deere_miller['Schist_Flat'][1],
                        fill=False,
                        label='Schist Parallel', color=v[1], linewidth=1, linestyle=':')
            else:
                cleanedListx = df_of_clusters_deere_miller[k][0][~np.isnan(df_of_clusters_deere_miller[k][0])]
                cleanedListy = df_of_clusters_deere_miller[k][1][~np.isnan(df_of_clusters_deere_miller[k][1])]
                ax.fill(cleanedListx, cleanedListy, fill=False, label=k, color=v[1], linewidth=1, closed=True)

    def format_axis(self, ax, state='', major_axis_vline=True):
        """
        Format log-log Axis

        :param ax: Axis to plot on
        :type ax: matplotlib
        :param state: state to enable to disable slopped lines
        :type state:
        :param major_axis_vline: Plot the major axis vlines
        :type major_axis_vline: bool
        :return:
        :rtype:
        """
        # Draw axis limits
        ax.set_xlim(self._xmin, self._xmax)
        ax.set_ylim(self._ymin, self._ymax)
        # Log-Log Scale
        ax.loglog()
        if major_axis_vline:
            ax.grid(alpha=0.5, zorder=-1)
        # Format the Number to XX format for X and Y axis
        for axis in [ax.xaxis, ax.yaxis]:
            formatter = FuncFormatter(lambda ax_lab, _: '{:.16g}'.format(ax_lab))
            axis.set_major_formatter(formatter)

        if not state:
            # Draw Slopped line to presents different Areas
            self.abline(200, 0, "line", 1000, '', ax)  # Slope of Modulus Ratio Low:Average MPa to GPa
            self.abline(500, 0, "line", 1000, '', ax)  # Slope of Modulus Ratio Average:High MPa to GPa

            # Text to Classify the MR domains
            self.abline(800, 0, "text", 1000, "High MR", ax)  # High MR
            self.abline(math.sqrt(200 * 500), 0, "text", 1000, 'Average MR', ax)  # Average MR
            self.abline(100, 0, "text", 1000, 'Low MR', ax)  # Low MR

    def initial_processing(self, rock_type_to_plot=None, plot_all_clusters=False, ucs_class_type=None, ax=None):
        """
        Main function to plot the Modulus Ratio underlay

        :param rock_type_to_plot: Rock cluster type to plot.
        :type rock_type_to_plot: UCS Strength Criteria adopted. Options Sedimentary, Igneous, Metamorphic.
        :param ucs_class_type: UCS Strength Criteria adopted. Options 'ISRM\n1977', 'ISRMCAT\n1979', 'Bieniawski\n1974', 'Jennings\n1973', 'Broch & Franklin\n1972', 'Geological Society\n1970', 'Deere & Miller\n1966', 'Coates\n1964', 'Coates & Parsons\n1966', 'ISO 14689\n2017', 'Anon\n1977', 'Anon\n1979', 'Ramamurthy\n2004'
        :type ucs_class_type: str
        :param ax: Axis to plot on
        :type ax: matplotlib

        :return: Axis
        :rtype: Matplotlib Axis
        """

        # Load the data Deere Miller digitized plots
        df_of_clusters_deere_miller = self._load_data("MR")

        # Indicate to user which curve is being plotted.
        if rock_type_to_plot:
            print("\tPlotting Modulus Ratio for %s Clusters" % formatting_codes.bold_text(rock_type_to_plot))
        else:
            print("\tPlotting Modulus Ratio for %s Clusters" % formatting_codes.bold_text("ALL"))

        # Initialise Plotting Axis
        if ax is None:
            ax = plt.gca()
            self._xmin, self._xmax = 0.1, 500
            self._ymin, self._ymax = 0.01, 200

        self.deere_miller_clusters(ax, df_of_clusters_deere_miller, r_type=rock_type_to_plot,
                                   plot_all_clusters_bool=plot_all_clusters)

        # Load information for UCS Strength Criteria adopted
        global category_names, category_values
        if ucs_class_type:
            category_names, category_values = rock_variables.ucs_strength_criteria(ucs_class_type)
            self.format_axis(ax, major_axis_vline=False)
            self.plot_v_lines(category_values, ax)
        else:
            self.format_axis(ax, major_axis_vline=True)

        return ax


class poisson_density():
    """
    Load Poisson Ratio and Density information
    """

    def initial_processing(self):
        """
        Load the variables and initialise the dataframe.

        :return: DataFrame containing the Min/Max Poisson Ratio and the Min/Max Density divided by Rock Name nad ROck Group. The latter two impact the y-axis and the hbars and titles.
        :rtype: pandas.DataFrame

        """

        # Initialise DataFrame
        df = pd.DataFrame()
        # Read the data from the dictionary to a DataFrame
        df = df.from_dict(rock_variables._poisson_density_range)

        # Group the data based on the Major Rock Type
        df = df.sort_values(by=['Group', 'Rock Type'])

        # Get the span of the data which would be the difference between the min and max
        df['Max_D'] = df['Max_D'] - df['Min_D']
        df['Max_P'] = df['Max_P'] - df['Min_P']

        return df

    def check_df_col_validity(self, df_to_plot, var, err_message="['Min_P', 'Max_P'] or ['Min_D', 'Max_D']"):
        """
        Checks if values are within the DataFrame column passed.

        :param df_to_plot: Panda Dataframe to plot
        :type df_to_plot: pandas.DataFrame
        :param var: Valriable name to check
        :type var: str
        :param err_message: Validation message for Options available to user
        :type err_message: str

        :return: True
        :rtype: bool
        :raise KeyError: The value entered is not within the available options.
        """

        if var not in df_to_plot:
            raise KeyError("Available Options %s" % err_message)

        return

    def plot_span_chart(self, df_to_plot, variable_span, variable_label, variable_units, ax=None, **kwargs):
        """
        Plot a chart divided by the rock type and rock group.

        :param df_to_plot: Panda Dataframe to plot
        :type df_to_plot: pandas.DataFrame
        :param variable_span: Span (i.e., min and max values) passed as a list. Must be the Column Header name in the DataFrame!
        :type variable_span: list[str, str]
        :param variable_label: Variable Name. X axis label
        :type variable_label: str
        :param variable_units: Variable Units. X axis label unit
        :type variable_units: str
        :param ax: Matplotlib Axis to plot On
        :type ax: Matplolib
        :param kwargs: Options to pass to matplotlib plotting method
        :type kwargs: keywords

        :return: Matplotlib AxesSubplots
        :rtype: Matplotlib Axis
        """

        # Initialise Plotting Axis
        if ax is None:
            ax = plt.gca()

        # Divide the data into groups
        dfx = df_to_plot.groupby(['Group'])

        # Get the total number of groups
        size = dfx.size()

        # Check data for the Span Chart
        for dat in variable_span:
            self.check_df_col_validity(df_to_plot, dat)
        # Get data for the Span Chart
        # X is the Rock Name and Y is the Parameter to plot
        # Change the grey to the required bar color
        df_to_plot.plot.barh(x='Rock Type', y=variable_span, stacked=True, color=['white', 'grey'], alpha=0.5, ax=ax,
                             **kwargs)

        # Make key, value pairs of the groups and their Cummalitive length to draw the H lines.
        df_dict_groups = dict(zip(list(dfx.groups.keys()), list(np.cumsum(dfx.size()))))
        # initialise variable
        hline_loc = 0
        # Loop over the key value pair and draw H lines and their corresponding key midway.
        for counter, (k, v) in enumerate(df_dict_groups.items()):
            # Skip over and not draw the last line.
            if counter != len(size):
                plt.axhline(v - 0.5, ls='--', color='black', alpha=0.5)  # Plot Division Line
            # Annotate text in the middle of the group with a white background
            plt.text(0.125 + plt.gca().get_xlim()[0], (v + hline_loc - 1) / 2, k, rotation=90,
                     color='green', fontweight='bold', va='center', bbox=dict(boxstyle="square",
                                                                              ec=(1., 1., 1.),
                                                                              fc=(1., 1., 1.),
                                                                              ))
            hline_loc = v  # Update line location

        # Cosmetics to the plotted curve
        # Disable any y-label information as this is determined by the DataFrame being plotted
        plt.ylabel('')
        # Plot the xlabel information based on the variables label and units passed.
        if ' ' not in variable_units:
            plt.xlabel("%s, %s" % (variable_label, variable_units))
        else:
            plt.xlabel("%s, %s (%s)" % (variable_label, variable_units.split(' ')[0], variable_units.split(' ')[1]))
        plt.legend().set_visible(False)

        return ax


class strength_ratio:
    """
    Based on the classification of Tatone, B.S.A., Abdelaziz, A. & Grasselli, G. Novel Mechanical Classification Method of Rock Based on the Uniaxial Compressive Strength and Brazilian Disc Strength. Rock Mech Rock Eng 55, 2503–2507 (2022). https://doi.org/10.1007/s00603-021-02759-7
    Data was built using a bivariant KDE
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html
    # https://towardsdatascience.com/simple-example-of-2d-density-plots-in-python-83b83b934f67

    # ADVANCED: By assigning the *_rocktype_dict* variable, more control over the clusters being plotted is gained.
    """

    # Dictionary to hold Rock Category

    # Load default variables
    _rocktype_dict = rock_variables._rocktype_dictionary

    def initial_processing(self, rock_type_to_plot=None, plot_all_clusters=False, ucs_class_type=None, ax=None):
        """
        Main function to plot the Modulus Ratio underlay

        :param rock_type_to_plot: Rock cluster type to plot.
        :type rock_type_to_plot: UCS Strength Criteria adopted. Options Sedimentary, Igneous, Metamorphic.
        :param ucs_class_type: UCS Strength Criteria adopted. Options 'ISRM\n1977', 'ISRMCAT\n1979', 'Bieniawski\n1974', 'Jennings\n1973', 'Broch & Franklin\n1972', 'Geological Society\n1970', 'Deere & Miller\n1966', 'Coates\n1964', 'Coates & Parsons\n1966', 'ISO 14689\n2017', 'Anon\n1977', 'Anon\n1979', 'Ramamurthy\n2004'
        :type ucs_class_type: str
        :param ax: Axis to plot on
        :type ax: matplotlib

        :return: Axis
        :rtype: Matplotlib Axis

        """

        # Load the data Deere Miller digitized plots
        df_of_clusters_tatone_et_al = modulus_ratio._load_data(self, "SR")

        # Indicate to user which curve is being plotted.
        if rock_type_to_plot:
            print("\tPlotting Strength Ratio for %s Clusters" % formatting_codes.bold_text(rock_type_to_plot))
        else:
            print("\tPlotting Strength Ratio for All Clusters")

        # Initialise Plotting Axis
        if ax is None:
            ax = plt.gca()
            self._xmin, self._xmax = 0.1, 50
            self._ymin, self._ymax = 1, 500

        modulus_ratio.deere_miller_clusters(self, ax, df_of_clusters_tatone_et_al, r_type=rock_type_to_plot,
                                            plot_all_clusters_bool=plot_all_clusters)

        # Load information for UCS Strength Criteria adopted
        global category_names, category_values
        if ucs_class_type:
            category_names, category_values = rock_variables.ucs_strength_criteria(ucs_class_type)
            self.format_axis(ax, major_axis_vline=False)
            modulus_ratio.plot_v_lines(self, category_values, ax)
        else:
            self.format_axis(ax, major_axis_vline=True)

        return ax

    def format_axis(self, ax, state='', major_axis_vline=True):
        """
        Format log-log Axis

        :param ax: Axis to plot on
        :type ax: matplotlib
        :param state: state to enable to disable slopped lines
        :type state:
        :param major_axis_vline: Plot the major axis vlines
        :type major_axis_vline: bool
        :return:
        :rtype:
        """
        # Draw axis limits
        ax.set_xlim(self._xmin, self._xmax)
        ax.set_ylim(self._ymin, self._ymax)
        # Log-Log Scale
        ax.loglog()
        ax.grid(major_axis_vline, alpha=0.5, zorder=-1)
        # Format the Number to XX format for X and Y axis
        for axis in [ax.xaxis, ax.yaxis]:
            formatter = FuncFormatter(lambda ax_lab, _: '{:.16g}'.format(ax_lab))
            axis.set_major_formatter(formatter)

        if not state:
            # Draw Slopped line to presents different Areas
            self.abline(20, 0, "line", 1, '', ax)  # Slope of Strength Ratio Low:Average MPa to GPa
            self.abline(8, 0, "line", 1, '', ax)  # Slope of Strength Ratio Average:High MPa to GPa

            # Text to Classify the MR domains
            self.abline(30, 0, "text", 1, "High UCS:BDS Ratio", ax, )  # High SR
            self.abline(math.sqrt(20 * 8), 0, "text", 1, 'Average UCS:BDS Ratio', ax, )  # Average SR
            self.abline(5, 0, "text", 1, 'Low UCS:BDS Ratio', ax, )  # Low SR

    def abline(self, slope, intercept, dr_state, multiplier=1, ratio='', ax=None):
        """
        Function to plot the slopped lines based on a slope and a y-intercept, basically mx+c. It is defined to form the Low/Avg/High MR ratio in the deere-miller classification plot.

        :param slope: the slope of the line
        :type slope: float
        :param intercept: the intercept of the lube
        :type intercept: float
        :param dr_state: draw state to move between the line drawing and the placement/writing of the text. Options [Line, Text]
        :type dr_state: str
        :param multiplier: in case of a need of a multiplier
        :type multiplier: int
        :param ratio: text associated with the MR modulus
        :type ratio: str
        :param ax: Matplotlib Axis
        :type ax: matplotlib
        :param x_text_loc: slope to write text
        :type x_text_loc: float

        :return:
        :rtype:
        """

        axes = plt.gca()  # Get axis limits
        x_vals = np.array(axes.get_xlim())  # Array the X as values from xlim
        y_vals = intercept + (slope / multiplier) * x_vals  # Get y values based on mx + c
        x_text_loc = 0.2  # X-Location of text
        txt_slope = np.rad2deg(
            np.arctan2(np.log(y_vals[-1]) - np.log(y_vals[0]), np.log(x_vals[-1]) - np.log(x_vals[0])))

        if dr_state == "line":
            ax.plot(x_vals, y_vals, color='grey', alpha=0.5, linestyle='--')
            # Add the text to the sloped line
            plt.text(x_text_loc, intercept + (slope / multiplier) * x_text_loc, '{:d}:1'.format(int(slope)),
                     rotation=txt_slope, bbox=dict(facecolor='white', edgecolor="white"))
        if dr_state == "text":
            # Add the text to category
            ax.text(x_text_loc, intercept + (slope / multiplier) * x_text_loc, ratio, rotation=txt_slope, alpha=0.5)


'''
MAIN MODULE
- Returns total time and Error on user termination.
'''

if __name__ == "__main__":
    try:
        # Names of files are defined in initial_processing - _load_data module
        # INPUT x_para, y_para, x_para name, y_para name,  UCS Strength Criteria adopted, "Rock"//"Replica"
        plx = modulus_ratio().initial_processing(plot_all_clusters=False, rock_type_to_plot='Sedimentary',
                                                 ucs_class_type="ISRMCAT\n1979")
        plx.scatter(10, 10, label="DataPoint")
        # Cosmetics to the figure and layouts
        plt.xlabel("UCS")
        plt.ylabel("Emod")
        plx.legend()
        plt.show()
    except KeyboardInterrupt:
        exit("TERMINATED BY USER")
