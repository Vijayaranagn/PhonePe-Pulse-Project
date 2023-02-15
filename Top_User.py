import sqlite3
import folium
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px


st.subheader('Top User Details')

conn = sqlite3.connect('Phonepe_pulse.db')
cursor = conn.cursor()

# Load the data into a DataFrame
df = pd.read_csv(r"C:\Users\ADMIN\Downloads\top_user.csv")

# Insert the data from the DataFrame into the database
df.to_sql("top_user", conn, if_exists="replace", index=False)	

# Commit the changes
conn.commit()

# Execute the query to create the filter view
cursor.execute("SELECT State, Year, Quarter, Districts, SUM(Users) as Total_Users FROM top_user GROUP BY State, Year, Quarter, Districts, Users")

# Fetch the filtered rows
filtered_rows = cursor.fetchall()

# Create a DataFrame from the filtered rows
df = pd.DataFrame(filtered_rows, columns=["State", "Year", "Quarter", "Districts", "Users"])

# Create a dropdown menu using Streamlit
#state = st.selectbox("Select State", df["State"].unique())
state_filter = st.selectbox("Select State", ["All", *df['State'].unique()])
year_filter = st.selectbox("Select Year", ["All", *df['Year'].unique()])
quater_filter = st.selectbox("Select Quarter", ["All", *df['Quarter'].unique()])
district_filter = st.selectbox("Select Districts", ["All", *df['Districts'].unique()])


if state_filter != "All":
    df = df[df['State'] == state_filter]
if year_filter != "All":
    df = df[df['Year'] == int(year_filter)]
if quater_filter != "All":
    df = df[df['Quarter'] == quater_filter]
if district_filter != "All":
    df = df[df['Districts'] == district_filter]

#df = df[(df['Users'] >= Total_Users[0]) & (df['Users'] <= Total_Users[1])]


# create table
st.write(df)


fig = px.bar(df, x="State", y="Users", color="Districts", title="Total Users by State")
st.plotly_chart(fig)

