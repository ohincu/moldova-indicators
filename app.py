#####################################
# Load libraries
#####################################
import pandas as pd
import streamlit as st
import plotly
import plotly.express as px
print(f"Streamlit version: {st.__version__}")
print(f"Pandas version: {pd.__version__}")
print(f"Plotly version: {plotly.__version__}")

#####################################
# Configure page
#####################################
st.set_page_config('Homepage', page_icon = "🏡")
with st.sidebar:
    st.markdown("# Hello, dear user 👋")
    st.markdown("## Welcome to my interactive app for visualizing key indicators of Moldova based on World Bank data! Explore Moldova's development from birth to death. Have fun 🎉!")


st.title('Moldova\'s Progress From 1960 Till 2022')
st.image('pics/sasha-pleshco-HBtWDEzIe6M-unsplash.jpg')

#####################################
# Get data
#####################################
@st.cache_data
def read_data():
    df = pd.read_csv("data/API_MDA_DS2_en_csv_v2_6302701.csv")
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    df = df[df['kpi'] == True] # only selected KPIs by me
    df.drop(columns = ['country_name', 'country_code', 'kpi'], inplace = True)
    df_melted = pd.melt(df, id_vars = ['indicator_name', 'indicator_code'], var_name = 'year', value_name = 'value')
    df_pivoted = df_melted.pivot_table(index = 'year', columns = 'indicator_name', values = 'value', aggfunc='first').reset_index()
    return df_pivoted

df = read_data()
if read_data() not in st.session_state:
    st.session_state['df'] = df
    
#####################################
# Configure buttons
#####################################
col1, col2 = st.columns(2)
selected_column = col1.selectbox("Select a column:", df.columns[1:])  # Exclude 'year' column

#####################################
# Plot the data
#####################################
def filter_and_plot_data(df, selected_column):
    df_filtered = df[['year', selected_column]].dropna()
    fig = px.line(df_filtered, x='year', y=selected_column, title=f"{selected_column} over the years")
    st.plotly_chart(fig)
    return df_filtered

df_filtered = filter_and_plot_data(df, selected_column)
st.markdown("Source data can be found [here](https://data.worldbank.org/country/MD)")


#####################################
# Download the data into a CSV
#####################################
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_filtered)
file_name = f'World_Bank_MD_{selected_column.replace(" ", "_")}.csv'
st.download_button(
    label = "Download plotted data as CSV",
    data = csv,
    file_name = file_name,
    mime = 'text/csv'
)