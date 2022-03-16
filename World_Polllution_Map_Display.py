# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:49:26 2022

@author: Yang Man, ym236195869@foxmail.com

GWCN AI Models

Subject: Global Plastic Pollution

Type: Display

Data Source: 
 https://www.kaggle.com/sohamgade/plastic-datasets
 https://data.worldbank.org/indicator/EN.ATM.CO2E.PC

Discription: 
 This Code first matches the global plastic waste data set and
 the CO2 emission data set using the national code, and then utilizes a Python
 visualization module to display the worldwide plastic waste volume and CO2 
 emissions of each country and area on a global map in 2010.
"""

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ThemeType

#%% Import data
plastic_data = pd.read_csv('./Global Plastic Pollution/plastic-waste-per-capita.csv')
CO2_data = pd.read_csv('./Global Plastic Pollution/CO2_emissions.csv')
#%% Data matching
plastic_data_nationcode = list(set(list(plastic_data['Code'])))
CO2_data_nationcode = list(CO2_data['Country Code'])
nationcode_matched = [x for x in plastic_data_nationcode if x in CO2_data_nationcode ]

plastic_data_picked = plastic_data.loc[plastic_data['Code'].isin(nationcode_matched)]
CO2_data_picked = CO2_data.loc[CO2_data['Country Code'].isin(nationcode_matched)]

CO2_data_picked.set_axis(['Entity','Country Code','CO2 Emissions (metric tons/person)'],axis='columns',inplace = True)
CO2_data_picked.sort_values(by='Country Code', inplace = True, ascending = True)
CO2_data_picked.reset_index(drop = True, inplace = True)
plastic_data_picked.sort_values(by=['Code'], inplace = True, ascending = True)
plastic_data_picked.reset_index(drop = True, inplace = True)
#%% Merge two picked datasets
data_merged = pd.merge(plastic_data_picked, CO2_data_picked, on = 'Entity')
data_merged.drop(labels = ['Year', 'Country Code'], axis = 1, inplace = True)

#%% Add data to Map
"""
# Abandon from using merged data since there are insufficient countries that exist
# both in CO2 emissions and mismanaged waste data sets.
# country_name = list(data_merged['Entity'])

# mismanaged_waste = list(data_merged['Per capita plastic waste (kg/person/day)'])
# co2_emitted = list(data_merged['CO2 Emissions (metric tons/person)'])

# mismanaged_waste_list = [list(z) for z in zip(country_name, mismanaged_waste)]
# co2_emitted_list = [list(z) for z in zip(country_name, co2_emitted)]
"""

country_name_mismanaged = list(plastic_data['Entity'])
mismanaged_waste = list(plastic_data['Per capita plastic waste (kg/person/day)'])

country_name_co2 = list(CO2_data['Country Name'])
co2_emitted = list(CO2_data['2010'])

mismanaged_waste_list = [list(z) for z in zip(country_name_mismanaged, mismanaged_waste)]
co2_emitted_list = [list(z) for z in zip(country_name_co2, co2_emitted)]

max_mismanaged_waste = max(mismanaged_waste)
min_mismanaged_waste = min(mismanaged_waste)

max_co2_emitted = max(co2_emitted)
min_co2_emitted = min(co2_emitted)


mismanaged_waste_web = (
    Map(init_opts=opts.InitOpts(theme = ThemeType.LIGHT, width="1900px", height="1000px"))  #Initiate Map Size
    
    #Global settings
    .set_global_opts(
        title_opts = opts.TitleOpts(title="Per capita plastic waste (kg/person/day) Year: 2010"),  #Title
        
        #Standard
        visualmap_opts = opts.VisualMapOpts(
            min_ = min_mismanaged_waste,
            max_ = max_mismanaged_waste,
            
            range_text = ['Plastic Waste Colour Range', ''],
            is_piecewise = True, #Define the legend as piecewised, defult is continuous
            pos_top = 'middle',
            pos_left = 'left',
            orient = 'vertical',
            
            split_number = 10,
            #type_ = "scatter"   
        )
    )
    
    #Series settings
    .set_series_opts(
        label_opts = opts.LabelOpts(is_show = False, color = 'blue')
        )
    
    .add("Mismanaged waste", mismanaged_waste_list, maptype = "world", is_map_symbol_show = False)  #Pass the list
    .render("Per capita plastic waste.html")
)


co2_emitted_web = (
    Map(init_opts=opts.InitOpts(theme = ThemeType.LIGHT, width="1900px", height="1000px"))  #Initiate Map Size
    
    #Global settings
    .set_global_opts(
        title_opts = opts.TitleOpts(title="Per capita CO2 emissions (kg/person/day) Year: 2010"),  #Title
        
        #Standard
        visualmap_opts = opts.VisualMapOpts(
            min_ = min_co2_emitted,
            max_ = max_co2_emitted,
            
            range_text = ['CO2 Emisstions Colour Range', ''],
            is_piecewise = True, #Define the legend as piecewised, defult is continuous
            pos_top = 'middle',
            pos_left = 'left',
            orient = 'vertical',
            
            split_number = 10,
            #type_ = "scatter"   
        )
    )
    
    #Series settings
    .set_series_opts(
        label_opts = opts.LabelOpts(is_show = False, color = 'blue')
        )
    
    .add("CO2 emitted", co2_emitted_list, maptype = "world", is_map_symbol_show = False)  #Pass the list
    .render("Per capita CO2 eimtted.html")
)