'''
EXAMPLE 01
'''
import pyrockmodulus
import matplotlib.pyplot as plt

xx = pyrockmodulus.modulus_ratio()
xx.initial_processing(plot_all_clusters=False, rock_type_to_plot='Sedimentary', ucs_class_type="ISRMCAT\n1979")
plt.ylabel("E (GPa)")
plt.xlabel("UCS (MPa)")
plt.show()

'''
EXAMPLE 02
'''
import pyrockmodulus
import matplotlib.pyplot as plt

xx = pyrockmodulus.modulus_ratio()
xx.initial_processing(plot_all_clusters=True)
plt.ylabel("E (GPa)")
plt.xlabel("UCS (MPa)")
plt.legend()
plt.show()

'''
EXAMPLE 03
'''
import pyrockmodulus.rock_variables as ucs_class
print(ucs_class.ucs_strength_criteria('ISRMCAT\n1979'))

'''
EXAMPLE 06
'''
import pyrockmodulus
import matplotlib.pyplot as plt

xx = pyrockmodulus.strength_ratio()
xx.initial_processing(plot_all_clusters=False, rock_type_to_plot='Sedimentary')
plt.ylabel("UCS (MPa)")
plt.xlabel("BDS (MPa)")
plt.show()

'''
EXAMPLE 04
'''
import pyrockmodulus.ucs_bar_chart_plot as ucs_classification_plot
import matplotlib.pyplot as plt
ucs_class = ucs_classification_plot.initial_processing()
plt.show()


'''
EXAMPLE 05
'''
import matplotlib.pyplot as plt
import matplotlib
import pyrockmodulus

plt.rcParams["figure.figsize"] = [5, 7.5]
matplotlib.rcParams['font.family'] = ['arial']
matplotlib.rcParams['font.size'] = 10

xx = pyrockmodulus.poisson_density()
df_data = xx.initial_processing()
ax1 = xx.plot_span_chart(df_data, ['Min_D', 'Max_D'], 'Density', r'$\rho$ g/cm$^{3}$')
ax1.axvline(2.0, lw=1, ls='--')
plt.tight_layout()
plt.show()