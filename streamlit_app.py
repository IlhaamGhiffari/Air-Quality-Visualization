import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set up page configuration and custom styles
st.set_page_config(layout="wide", page_title="Environmental Insights Dashboard")
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    # Convert to datetime and add a month_year column for easier aggregation
    data['date'] = pd.to_datetime(data[['year', 'month', 'day']])
    data['month_year'] = data['date'].dt.to_period('M')
    # Categorize PM2.5 levels based on a generic standard (customize as needed)
    bins = [0, 12, 35.4, 55.4, 150.4, np.inf]
    labels = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy']
    data['PM2.5_category'] = pd.cut(data['PM2.5'], bins=bins, labels=labels, right=False)
    return data

# Replace 'path/to/your/data.csv' with the actual path to your dataset
data = load_data('clean.csv')


# Sidebar filters for user selection
with st.sidebar:
    st.title("Filters")
    year = st.selectbox('Year', options=sorted(data['year'].unique()), index=0)
    station = st.selectbox('Station', options=sorted(data['station'].unique()), index=0)

# Filter data based on selections
filtered_data = data[(data['year'] == year) & (data['station'] == station)]

    
# Main dashboard layout
st.title(f"Environmental Insights for {station}, {year}")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Fun Facts", "Fun Facts About The Data", "Statistical Insights"])

with tab1:
    st.markdown(
        """
        <p style="font-size:20px; color:grey;">
        Fun Facts:
        </p>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("What is PM2.5?"):
        st.write("PM2.5 refers to atmospheric particulate matter (PM) that have a diameter of less than 2.5 micrometers, which is about 3% the diameter of a human hair. Commonly found in smoke and haze, these particles can be inhaled and cause serious health problems.")

    with st.expander("What is PM10?"):
        st.write("PM10 refers to atmospheric particulate matter (PM) that have a diameter of less than 10 micrometers, which is about 1/7 the diameter of a human hair. Common sources include dust, pollen, and mold.")

    with st.expander("What is AQI?"):
        st.write("The Air Quality Index (AQI) is a measure used to communicate how polluted the air currently is or how polluted it is forecast to become. The AQI scale ranges from 0 to 500. The higher the AQI value, the greater the level of air pollution and the greater the health concern.")

    with st.expander("What is AQI Category?"):
        st.write("The AQI category is a descriptor used to provide a qualitative representation of the AQI value. The categories are based on the health effects associated with different levels of air pollution.")

with tab2:
    st.markdown(
        """
        <p style="font-size:20px; color:grey;">
        Fun Facts About The Data:
        </p>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("PM2.5 Levels"):
        st.write(f"The highest PM2.5 level recorded is {data['PM2.5'].max()} µg/m³.")
        st.write(f"The lowest PM2.5 level recorded is {data['PM2.5'].min()} µg/m³.")

    with st.expander("PM10 Levels"):
        st.write(f"The highest PM10 level recorded is {data['PM10'].max()} µg/m³.")
        st.write(f"The lowest PM10 level recorded is {data['PM10'].min()} µg/m³.")

with tab3:
    st.markdown(
        """
        <p style="font-size:20px; color:grey;">
        Statistical Insights:
        </p>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("PM2.5 Levels"):
        st.write(f"The average PM2.5 level is {data['PM2.5'].mean()} µg/m³.")
        st.write(f"The median PM2.5 level is {data['PM2.5'].median()} µg/m³.")
        st.write(f"The standard deviation of PM2.5 levels is {data['PM2.5'].std()} µg/m³.")

    with st.expander("PM10 Levels"):
        st.write(f"The average PM10 level is {data['PM10'].mean()} µg/m³.")
        st.write(f"The median PM10 level is {data['PM10'].median()} µg/m³.")
        st.write(f"The standard deviation of PM10 levels is {data['PM10'].std()} µg/m³.")

# Display key metrics and aggregated views in columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pollution Overview")
    # Monthly average pollution levels
    monthly_avg = filtered_data.groupby(filtered_data['date'].dt.month)[['PM2.5', 'PM10']].mean()
    fig1 = px.line(monthly_avg, title="Monthly Average PM2.5 and PM10")
    fig1.update_xaxes(title="Month")
    fig1.update_yaxes(title="Concentration (µg/m³)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("PM2.5 Categories Distribution")
    # Distribution of PM2.5 categories
    fig2 = px.pie(filtered_data, names='PM2.5_category', title="PM2.5 Air Quality Categories")
    st.plotly_chart(fig2, use_container_width=True)

# Tabs for detailed visualizations
tab1, tab2, tab3 = st.tabs(["Meteorological Conditions", "Data Overview", "Statistical Insights"])

with tab1:
    st.subheader("Meteorological Conditions Correlations")
    # Correlation between meteorological conditions
    fig3 = px.scatter_matrix(filtered_data,
                             dimensions=['TEMP', 'PRES', 'DEWP', 'RAIN'],
                             title='Correlations Between Meteorological Conditions')
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("Data Table")
    # Display filtered data table
    st.dataframe(filtered_data)
    
with tab3:
    st.subheader("Statistical Summary")
    # Summary statistics for the filtered data
    st.write(filtered_data.describe())
    

# Add copyright and credits
st.markdown(
    """
    <p style="text-align:center; font-size:12px; color:grey;">
    Created by M. Ilhaam Ghiffari
    </p>
    """,
    unsafe_allow_html=True,
)

