import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 0. set constants
PATH = '/usr/local/airflow/'


# 1. Load the environmental impact files calculated by the "load_database.py" script
# CBA tables give the consumption-based impacts for each industry in each country
D_cba = pd.read_table(PATH + "impact/D_cba.txt", header=[0, 1], index_col=0)
D_cba_cap = pd.read_table(PATH + "impact/D_cba_cap.txt", header=0, index_col=0)
D_cba_reg = pd.read_table(PATH + "impact/D_cba_reg.txt", header=0, index_col=0)

# the matrix M specifies the impact/EUR for each industry in each country
M = pd.read_table(PATH + "impact/M.txt", header=[0, 1], index_col=0)

# the Y matrix gives the final consumption (in EUR) from each industry in each countries
Y = pd.read_table(PATH + "Y.txt", header=[0, 1], index_col=[0, 1])

# the Z matrix traces the trade flows between each sectors and each countries
Z = pd.read_table(PATH + "Z.txt", header=[0, 1], index_col=[0, 1])


# 2. Compare GHG footprint of each country (with Canada highlighted)
# Select ghg footprint, drop aggregated countries, add integer index, sort by descending ghg footprint
cba = D_cba_reg.loc['global warming (GWP100)']\
    .drop(['WM', 'WA', 'WL', 'WE'])\
    .reset_index()\
    .sort_values('global warming (GWP100)', ascending=False)

# plot results
fig, ax = plt.subplots()
countries = list(cba.loc[:, 'index'].values)
ghg = list(cba.loc[:, 'global warming (GWP100)'].values)

y_pos = np.arange(len(countries))

ax.barh(y_pos, ghg, align='center', color='gray')
ax.set_yticks(y_pos)
ax.set_yticklabels(countries)
ax.invert_yaxis()
ax.set_xlabel('Consumption-based GHG footprint (kg CO2 eq)')

CA_pos = countries.index('CA')
ax.patches[CA_pos].set_facecolor('green')

plt.savefig('fig1.png')

# 3. Compare per-capita GHG footprint of each country
# Select ghg footprint, drop aggregated countries, add integer index, sort by descending ghg footprint
cba_cap = D_cba_cap.loc['global warming (GWP100)']\
    .drop(['WM', 'WA', 'WL', 'WE'])\
    .reset_index()\
    .sort_values('global warming (GWP100)', ascending=False)

# plot results
fig, ax = plt.subplots()
countries = list(cba_cap.loc[:, 'index'].values)
ghg = list(cba_cap.loc[:, 'global warming (GWP100)'].values)

y_pos = np.arange(len(countries))

ax.barh(y_pos, ghg, align='center', color='gray')
ax.set_yticks(y_pos)
ax.set_yticklabels(countries)
ax.invert_yaxis()
ax.set_xlabel('GHG footprint per capita (kg CO2 eq/cap)')

CA_pos = countries.index('CA')
ax.patches[CA_pos].set_facecolor('green')

plt.savefig('fig2.png')


# 4. Calculate the consumption impact/CAD$ in Canada for each industry
# isolate canadian consumption by household
Y_CA = Y['CA']['Final consumption expenditure by households']

# calculate the total environmental impact associated with canadian consumption
M_sum = M.multiply(Y_CA).stack([0, 1]).groupby(['impact', 'sector']).sum().unstack()

# sum the consumption by sector
Y_sum = Y_CA.groupby('sector').sum()

# calculate the impact/Million EURO of canadian consumption for each sector
M_avg = M_sum/Y_sum

# convert to Impact/Million CAD$
M_avg_CAD = M_avg / 1.47


# 5. Compare the impact of selected industries
# select some sectors of interest
sectors = ['Tanning and dressing of leather; manufacture of luggage, handbags, saddlery, harness and footwear',
           'Manufacture of radio, television and communication equipment and apparatus',
           'Recreational, cultural and sporting activities',
           'Hotels and restaurants']

# select some impacts of interest
impacts = ['global warming (GWP100)',
           'Water Consumption Blue - Total',
           'Domestic Extraction',
           'Land use']

# isolate info from selected sector columns
sector_impacts = M_avg_CAD.loc[:, M_avg_CAD.columns & sectors]

# isolate info from selected impact rows
ghg = list(sector_impacts.loc['global warming (GWP100)'].values)
water = list(sector_impacts.loc['Water Consumption Blue - Total'].values)
material = list(sector_impacts.loc['Domestic Extraction'].values)
land = list(sector_impacts.loc['Land use'].values)

# plot impacts
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
sectors = list(sector_impacts.columns.values)
labels = ['Hotel & Restaurant', 'TV Screen', 'Cultural activities', 'Leather bag']
colors = ['black', 'red', 'green', 'blue']
y_pos = np.arange(len(sectors))

ax1.barh(y_pos, ghg, align='center', color=colors)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(labels)
ax1.invert_yaxis()
ax1.set_xlabel('Carbon footprint (kg CO2 eq/M CAD$)')

ax2.barh(y_pos, water, align='center', color=colors)
ax2.set_yticks(y_pos)
ax2.invert_yaxis()
ax2.set_xlabel('Water footprint (M m3/M CAD$)')

ax3.barh(y_pos, material, align='center', color=colors)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(labels)
ax3.invert_yaxis()
ax3.set_xlabel('Material footprint (kT/M CAD$)')

ax4.barh(y_pos, land, align='center', color=colors)
ax4.set_yticks(y_pos)
ax4.invert_yaxis()
ax4.set_xlabel('Land footprint (km2/M CAD$)')

plt.savefig('fig3.png')


# 6. Plot transaction matrix
plt.figure(figsize=(15, 15))
plt.imshow(Z, vmax=1E-3)
plt.xlabel('Countries - sectors')
plt.ylabel('Countries - sectors')

plt.savefig('fig4.png')
