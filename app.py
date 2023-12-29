#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st # v0.69
import numpy as np
import pandas as pd
import pickle
import gzip
#import utils_functions.py
#from utils_functions import find_postal, find_nearest, dist_from_location, map, map_flats_year, _max_width_
import streamlit.components.v1 as components
import pydeck as pdk
from pathlib import Path
import os
import gdown
import joblib

def load_model():
# Load the model from the file
    with gzip.open('model.pkl', 'rb') as file:
        data = pickle.load(file) 
    return data

data=load_model()
storey_range=data['storey_range']
loaded_model=data['model']
flat_model=data['flatmodel']
flat_type=data['flat_type']
Floor_Area=data['Floor_Area']
town=data['town']
Year_of_sale=np.unique(data['Year_of_sale'])  #data['Year_of_sale']
lease_commence_date= np.unique(data['lease_commence_date'])  #data['lease_commence_date']

#def show_predict_page():
st.set_page_config(layout="wide")
st.title('App for Visualize and Predict Singapore HDB Resale Prices')
st.text(" ")
st.text(" ")
st.text(" ")
    

with st.sidebar.form('User Input HDB Features'):
    
        town1 = st.selectbox('Town', list([ 'TAMPINES', 'YISHUN', 'BEDOK', 'JURONG WEST', 'WOODLANDS', 
                                        'ANG MO KIO', 'HOUGANG', 'BUKIT BATOK', 'CHOA CHU KANG', 'BUKIT MERAH',
                                        'PASIR RIS', 'SENGKANG', 'TOA PAYOH', 'QUEENSTOWN', 'GEYLANG', 'CLEMENTI',
                                        'BUKIT PANJANG', 'KALLANG/WHAMPOA', 'JURONG EAST','SERANGOON', 'BISHAN', 
                                        'PUNGGOL', 'SEMBAWANG', 'MARINE PARADE', 'CENTRAL AREA', 'BUKIT TIMAH', 
                                        'LIM CHU KANG']),index=4)
    
        flat_model1 = st.selectbox('Flat Model', list(['MODEL A','IMPROVED','NEW GENERATION','SIMPLIFIED','PREMIUM APARTMENT','STANDARD','APARTMENT','MAISONETTE','MODEL A2','DBSS',
                                                    'MODEL A-MAISONETTE','ADJOINED FLAT','TERRACE','MULTI GENERATION','TYPE S1','TYPE S2','IMPROVED-MAISONETTE',
                                                    'PREMIUM APARTMENT LOFT','2-ROOM','PREMIUM MAISONETTE','3GEN']), index=2)
    
        flat_type1 = st.selectbox('Flat Type', list(['1 Room', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE']),index=5)
    
        floor_area1 = st.slider("Floor Area (sqm)", 28,307,93) # floor area
    
        storey1 = st.selectbox('Storey', list(['01 TO 03','04 TO 06','07 TO 09','10 TO 12','13 TO 15',
                                                '16 TO 18','19 TO 21','22 TO 24','25 TO 27','28 TO 30',
                                                '31 TO 33','34 TO 36','37 TO 39','40 TO 42','43 TO 45',
                                                '46 TO 48','49 TO 51','01 TO 05','06 TO 10','11 TO 15',
                                                '16 TO 20','21 TO 25', '26 TO 30','31 TO 35','36 TO 40']), index=3)
    
        lease_commence_date1 = st.selectbox('Lease Commencement Date', list(reversed(range(1966, 2022))), index=0)
    
        Year_of_sale1 = st.selectbox('Year_of_sale', list(reversed(range(1990, 2023))), index=0)
        
        submitted1 = st.form_submit_button(label='Submit HDB 🔎')
        
        #                slyear=pd.DataFrame({'Year_of_sale':list(Year_of_sale)})

        selected_Year_of_sale= Year_of_sale1

#                lcd= pd.DataFrame({'lease_commence_date':list(lease_commence_date)})  

        selected_lease_commence_date= lease_commence_date1
                
        selected_town_encoding = town.get(town1, None)
    # print("Encoded Value for", town, ":", selected_town_encoding)

        selected_flat_model_encoding = flat_model.get(flat_model1, None)
    # print("Encoded Value for", flat_model, ":", selected_flat_model_encoding)

        selected_flat_type_encoding = flat_type.get(flat_type1, None)
    # print("Encoded Value for", flat_type, ":", selected_flat_type_encoding)

        selected_floor_area_encoding = Floor_Area.get(floor_area1, None)
    # print("Encoded Value for", floor_area, ":", selected_floor_area_encoding)

        selected_storey_range_encoding = storey_range.get(storey1, None)
    # print("Encoded Value for", storey, ":", selected_storey_range_encoding)

        input_array = [[selected_Year_of_sale, selected_town_encoding, selected_flat_model_encoding, selected_flat_type_encoding,
                                 selected_floor_area_encoding, selected_storey_range_encoding, selected_lease_commence_date]]
        
if submitted1:         
 # input_array
    predict1 = loaded_model.predict(input_array)[0]

    st.header('Predicted HDB Resale Price is **SGD$%s**' % ("{:,}".format(int(predict1))))
#EXPANDER FOR Model INFORMATION


# In[ ]:




