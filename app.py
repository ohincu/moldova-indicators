import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config('Homepage', page_icon = "🏡")

with st.sidebar:
    st.markdown("# Hello, dear user 👋")
    st.markdown("## Welcome to my interactive app for visualizing key indicators of Moldova based on World Bank data! Explore Moldova's development from birth to death. Have fun 🎉!")


st.title('Moldovas Progress From 1960 Till Today')
st.markdown("Source data can be found [here](https://data.worldbank.org/country/MD)")

@st.cache_data
def read_data():
    df = pd.read_csv("API_MDA_DS2_en_csv_v2_6302701.csv")
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    df.drop(columns = ['country_name', 'country_code'], inplace = True)
    years_columns = df.columns[4:]  # Assuming the years start from the 4th column onward
    df_melted = pd.melt(df, id_vars = ['indicator_name', 'indicator_code'], var_name = 'Year', value_name = 'Value')
    df_pivoted = df_melted.pivot_table(index = 'Year', columns = 'indicator_name', values='Value', aggfunc='first').reset_index()
    return df_pivoted

df = read_data()
if read_data() not in st.session_state:
    st.session_state['df'] = df
    
col1, col2 = st.columns(2)
selected_column = col1.selectbox("Select a column:", df.columns[1:])  # Exclude 'Year' column
df_filtered = df[['Year', selected_column]].dropna()

fig = px.line(df_filtered, x = 'Year', y = selected_column, title=f"{selected_column} over the years")
st.plotly_chart(fig)

