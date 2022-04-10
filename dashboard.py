import streamlit as st
import pandas as pd

#st.title('This is a title')
#
#st.header("This is a What the fuck om rules")
#
#
#st.write('This is regular test')
#
#
#'''
#
## header
#
### subheader
#
#
#
#'''
#some_dict  = {'symbol': 'BKR',
#  'name': 'Baker Hughes A Ge Co. Cl A',
#  'percent': '1.61',
#  'shares': 'N/A'}
#
#  
#st.write(some_dict)

st.sidebar.title('Options')

option = st.sidebar.selectbox(
     'Select Dashboard',
     ('Wallstreetbets','ETF Holdings','Josh Rules'))

st.header(option)    
df = pd.read_csv('data/2022-04-08/SPYD.csv')

st.dataframe(df)
st.image('https://sporttechie-prod.s3.amazonaws.com/SOTI%202021%20-%20Pro%20Videos/pro_ws-_oracle.png')