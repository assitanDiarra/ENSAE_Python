import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader


plt.figure(figsize=(15,15)) #size of figure
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m',
                                        category='cultural', name=shapename)

ax = plt.axes(projection=ccrs.PlateCarree())
countries = shpreader.Reader(countries_shp).records()
     
for country in countries:
    if country.attributes['ISO_A3'] == 'USA':
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='red',
                          label=country.attributes['NAME_LONG'])
    else:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='blue',
                          label=country.attributes['NAME_LONG'])

plt.show()


#see all available attributes for a country
for country in countries:
    #print(country.attributes['ISO_A3'], country.attributes['NAME_LONG'], '\n')
    if country.attributes['NAME_LONG'] == 'France': 
        print(country.attributes)

############################# higlighting specific groups of countries
plt.figure(figsize=(15,15)) #size of figure
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m',
                                        category='cultural', name=shapename)

ax = plt.axes(projection=ccrs.PlateCarree())
countries = shpreader.Reader(countries_shp).records()
for country in countries:
    if country.attributes['ADM0_A3_IS'] in ['USA', 'FRA', 'AUS', 'GBR', 'MLI', 'ROU']:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='red')
   
    elif country.attributes['ADM0_A3_IS'] in ['RUS', 'CAN']:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='yellow') 
    else:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='blue')

plt.show()
###!!!! France doesn't have its iso a3 code => use  ADM0_A3_IS   

############################# higlighting groups of countries, use grouped series
import pandas as pd
df_groups = pd.read_excel(io='CLASS.xls', sheet_name='List of economies'
              ,header = 4)
df_groups = df_groups.loc[1:, df_groups.columns] #remove unwanted rows
  
groupby_inc = df_groups['Code'].groupby(df_groups['Income group']) 
high = [x[-3:] for x in list(groupby_inc)[0][1]] #get country codes in a list for group 0 - High income
low = [x[-3:] for x in list(groupby_inc)[1][1]]
middle_low = [x[-3:] for x in list(groupby_inc)[2][1]]
middle_high = [x[-3:] for x in list(groupby_inc)[2][1]]

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader


plt.figure(figsize=(15,15)) #size of figure
shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m',
                                        category='cultural', name=shapename)

ax = plt.axes(projection=ccrs.PlateCarree())
countries = shpreader.Reader(countries_shp).records()

for country in countries:
    #print(country.attributes['ADM0_A3_IS'])
    if country.attributes['ADM0_A3_IS'] in high:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='green')
        
    elif country.attributes['ADM0_A3_IS'] in low:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='red')
    
    elif country.attributes['ADM0_A3_IS'] in middle_low:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='orange')      

    elif country.attributes['ADM0_A3_IS'] in middle_high:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='yellow')          

    else:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='blue')

plt.show()
#=> KO : countries that remain blue : either unclassified, or codes don't match

