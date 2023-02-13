import sqlite3
import folium
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(page_title = "PhonePe Pulse: 2018 - 2022 Transaction Data")

st.title(":blue[PhonePe Pulse]")
st.title(":green[2018-2022 Transaction Data]")

st.header('Aggregated Transaction Details:smile:')
st.subheader('State')

conn = sqlite3.connect('Phonepe_pulse.db')
cursor = conn.cursor()

# Load the data into a DataFrame
df = pd.read_csv(r"C:\Users\ADMIN\Downloads\agg_transaction.csv")

# Insert the data from the DataFrame into the database
df.to_sql("agg_transaction", conn, if_exists="replace", index=False)

# Commit the changes
conn.commit()

#db_name = r"C:\Users\ADMIN\Downloads\Phonepe_pulse.db"
#table_name = "agg_transaction"
#conn = sqlite3.connect(r"C:\Users\ADMIN\Downloads\Phonepe_pulse.db")
#df = pd.read_sql_query(f"SELECT * from {table_name}", conn)

# Execute the query to create the filter view
cursor.execute("SELECT State, Quarter, Year, SUM(Transaction_amount) as Total_Transaction_amount FROM agg_transaction GROUP BY State, Year, Quarter, Transaction_amount")

# Fetch the filtered rows
filtered_rows = cursor.fetchall()

# Create a DataFrame from the filtered rows
df = pd.DataFrame(filtered_rows, columns=["State", "Quarter", "Year", "Transaction_amount"])

# Create a dropdown menu using Streamlit
#state = st.selectbox("Select State", df["State"].unique())
state_filter = st.selectbox("Select State", ["All", *df['State'].unique()])
year_filter = st.selectbox("Select Year", ["All", *df['Year'].unique()])
quater_filter = st.selectbox("Select Quarter", ["All", *df['Quarter'].unique()])

if state_filter != "All":
    df = df[df['State'] == state_filter]
if year_filter != "All":
    df = df[df['Year'] == int(year_filter)]
if quater_filter != "All":
    df = df[df['Quarter'] == quater_filter]

fig = px.bar(df, x="Year", y="Transaction_amount", facet_col="State", color="State")

# create table
st.write(df)
