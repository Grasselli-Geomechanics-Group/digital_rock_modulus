# /////////////////////////////////////////////////////////////// #
# Python Script initially created on 2022-12-15
# Compiled by Aly @ Grasselli Geomechanics Group, UofT, 2022
# Created using PyCharm
# /////////////////////////////////////////////////////////////// #

# Dictionary to hold Rock Category
_rocktype_dictionary = {
    "Diabase": ["Igneous", 'blue', 'ID'],
    "Intrusive Rock": ["Igneous", 'black', "IG"],
    "Flow Rock": ["Igneous", 'red', "IF"],
    "Granite": ["Igneous", 'black', "IG"],
    "Basalt": ["Igneous", 'red', "IF"],
    "Quartzite": ["Metamorphic", 'orange', "MQ"],
    "Gneiss": ["Metamorphic", 'yellow', "MG"],
    "Marble": ["Metamorphic", 'purple', "MM"],
    "Schist_Flat": ["Metamorphic", 'darkgreen', "MSpp"],
    "Schist": ["Metamorphic", 'darkgreen', "MS"],
    "Schist_Perp": ["Metamorphic", 'olive', "MSpl"],
    "Limestone": ["Sedimentary", 'cyan', "SL"],
    "Mudstone": ["Sedimentary", 'grey', "SSh"],
    "Sandstone": ["Sedimentary", 'brown', "SS"],
    "Shale": ["Sedimentary", 'dodgerblue', 'SSh'],
    "Chalk": ["Sedimentary", 'fuchsia', 'SC']
}

_poisson_density_range = [
    {'Rock Type': 'Andesite', 'Group': 'Igneous', 'Min_P': 0.2, 'Max_P': 0.35, 'Min_D': 2.172, 'Max_D': 3.052},
    {'Rock Type': 'Basalt', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.35, 'Min_D': 0.736, 'Max_D': 3.124},
    {'Rock Type': 'Claystone', 'Group': 'Sedimentary', 'Min_P': 0.25, 'Max_P': 0.4, 'Min_D': 1.8, 'Max_D': 2.2},
    {'Rock Type': 'Conglomerate', 'Group': 'Sedimentary', 'Min_P': 0.1, 'Max_P': 0.4, 'Min_D': 2.47, 'Max_D': 2.76},
    {'Rock Type': 'Diabase/Dolerite', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.35, 'Min_D': 2.296, 'Max_D': 3.19},
    {'Rock Type': 'Diorite', 'Group': 'Igneous', 'Min_P': 0.2, 'Max_P': 0.3, 'Min_D': 2.03, 'Max_D': 3.124},
    {'Rock Type': 'Dolomite', 'Group': 'Sedimentary', 'Min_P': 0.15, 'Max_P': 0.35, 'Min_D': 2.4, 'Max_D': 2.85},
    {'Rock Type': 'Gabbro', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.38, 'Min_D': 2.7, 'Max_D': 3.19},
    {'Rock Type': 'Gneiss', 'Group': 'Metamorphic', 'Min_P': 0.1, 'Max_P': 0.3, 'Min_D': 2.064, 'Max_D': 3.36},
    {'Rock Type': 'Granite', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.33, 'Min_D': 2.4, 'Max_D': 2.785},
    {'Rock Type': 'Granodiorite', 'Group': 'Igneous', 'Min_P': 0.15, 'Max_P': 0.25, 'Min_D': 2.63, 'Max_D': 2.74},
    {'Rock Type': 'Greywacke', 'Group': 'Sedimentary', 'Min_P': 0.08, 'Max_P': 0.23, 'Min_D': 2.41, 'Max_D': 2.77},
    {'Rock Type': 'Limestone', 'Group': 'Sedimentary', 'Min_P': 0.1, 'Max_P': 0.33, 'Min_D': 1.31, 'Max_D': 2.92},
    {'Rock Type': 'Marble', 'Group': 'Metamorphic', 'Min_P': 0.15, 'Max_P': 0.3, 'Min_D': 2.64, 'Max_D': 3.02},
    {'Rock Type': 'Marl', 'Group': 'Sedimentary', 'Min_P': 0.13, 'Max_P': 0.33, 'Min_D': 1.86, 'Max_D': 2.69},
    {'Rock Type': 'Norite', 'Group': 'Igneous', 'Min_P': 0.2, 'Max_P': 0.25, 'Min_D': 2.72, 'Max_D': 3.02},
    {'Rock Type': 'Quartzite', 'Group': 'Metamorphic', 'Min_P': 0.1, 'Max_P': 0.33, 'Min_D': 2.55, 'Max_D': 3.05},
    {'Rock Type': 'Rock Salt', 'Group': 'Sedimentary', 'Min_P': 0.05, 'Max_P': 0.3, 'Min_D': 2.1, 'Max_D': 2.9},
    {'Rock Type': 'Sandstone', 'Group': 'Sedimentary', 'Min_P': 0.05, 'Max_P': 0.4, 'Min_D': 1.44, 'Max_D': 2.8},
    {'Rock Type': 'Shale', 'Group': 'Sedimentary', 'Min_P': 0.05, 'Max_P': 0.32, 'Min_D': 1.6, 'Max_D': 2.92},
    {'Rock Type': 'Siltstone', 'Group': 'Sedimentary', 'Min_P': 0.13, 'Max_P': 0.35, 'Min_D': 1.11, 'Max_D': 2.87},
    {'Rock Type': 'Tuff', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.28, 'Min_D': 1.6, 'Max_D': 2.78}
]