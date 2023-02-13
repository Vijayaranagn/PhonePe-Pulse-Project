import sqlite3
import folium
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px


st.subheader('Map Transaction Details')

conn = sqlite3.connect('Phonepe_pulse.db')
cursor = conn.cursor()

# Load the data into a DataFrame
df = pd.read_csv(r"C:\Users\ADMIN\Downloads\map_transaction.csv")

# Insert the data from the DataFrame into the database
df.to_sql("map_transaction", conn, if_exists="replace", index=False)	

# Commit the changes
conn.commit()

# Execute the query to create the filter view
cursor.execute("SELECT State, Quarter, Year, District , SUM(Amount) as total_amount FROM map_transaction GROUP BY State, Year, Quarter, District, Amount")

# Fetch the filtered rows
filtered_rows = cursor.fetchall()

# Create a DataFrame from the filtered rows
df = pd.DataFrame(filtered_rows, columns=["State", "Quarter", "Year", "District", "Amount"])

# Create a dropdown menu using Streamlit
#state = st.selectbox("Select State", df["State"].unique())
state_filter = st.selectbox("Select State", ["All", *df['State'].unique()])
year_filter = st.selectbox("Select Year", ["All", *df['Year'].unique()])
district_filter = st.selectbox("Select District", ["All", *df['District'].unique()])
quater_filter = st.selectbox("Select Quarter", ["All", *df['Quarter'].unique()])
#total_amount = st.slider("Amount", 0, 9000000, (0, 9000000))

if state_filter != "All":
    df = df[df['State'] == state_filter]
if year_filter != "All":
    df = df[df['Year'] == int(year_filter)]
if quater_filter != "All":
    df = df[df['Quarter'] == quater_filter]
if district_filter != "All":
    df = df[df['District'] == district_filter]

#df = df[(df['Amount'] >= total_amount[0]) & (df['Amount'] <= total_amount[1])]


# create table
st.write(df)

