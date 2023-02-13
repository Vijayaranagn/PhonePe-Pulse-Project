import sqlite3
import folium
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


st.header('Aggregated User Details')

conn = sqlite3.connect('Phonepe_pulse.db')
cursor = conn.cursor()

# Load the data into a DataFrame
df1 = pd.read_csv(r"C:\Users\ADMIN\Downloads\agg_user.csv")

# Insert the data from the DataFrame into the database
df1.to_sql("agg_user", conn, if_exists="replace", index=False)

# Commit the changes
conn.commit()

# Execute the query to create the filter view
cursor.execute("SELECT State, Year, Quarter, Brand, Count FROM agg_user GROUP BY State, Year, Quarter, Brand, Count")

# Fetch the filtered rows
filtered_rows = cursor.fetchall()

# Load the data into a DataFrame
df1 = pd.read_csv(r"C:\Users\ADMIN\Downloads\agg_user.csv")

# Insert the data from the DataFrame into the database
df1.to_sql("agg_user", conn, if_exists="replace", index=False)


# Load the data from the table into a Pandas DataFrame
#df1 = pd.read_sql_query(f"SELECT * from {table_name}", conn)

df1 = pd.DataFrame(filtered_rows, columns=["State", "Year", "Quarter", "Brand", "Count"])


# Create the filter view
state_filter = st.selectbox("Select State", ["All", *df1['State'].unique()])
year_filter = st.selectbox("Select Year", ["All", *df1['Year'].unique()])
quarter_filter = st.selectbox("Select Quarter", ["All", *df1['Quarter'].unique()])
brand_filter = st.selectbox("Select Brand", ["All", *df1['Brand'].unique()])

# Apply the filters
if state_filter != "All":
    df1 = df1[df1['State'] == state_filter]
if year_filter != "All":
    df1 = df1[df1['Year'] == int(year_filter)]
if quarter_filter != "All":
    df1 = df1[df1['Quarter'] == quarter_filter]
if brand_filter != "All":
    df1 = df1[df1['Brand'] == brand_filter]


# Show the filtered data and the plot in the Streamlit app
st.write(df1)

