import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Function to load data from SQLite
def load_data():
    db_path = "speed_results.db"  # Ensure this file exists in the same directory
    conn = sqlite3.connect(db_path)
    query = """
    SELECT timestamp, download_speed, upload_speed, ping 
    FROM speed_test_results 
    ORDER BY timestamp DESC 
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# Load Data
df = load_data()

# Streamlit UI
st.set_page_config(page_title="Speed Test Dashboard", layout="wide")
st.title("📊 Internet Speed Test Dashboard")

# Date filter
st.sidebar.header("Filter by Date Range")
date_range = st.sidebar.date_input("Select Date Range", [df["timestamp"].min().date(), df["timestamp"].max().date()])

# Filter data based on selection
filtered_df = df[(df["timestamp"].dt.date >= date_range[0]) & (df["timestamp"].dt.date <= date_range[1])]

# Plot Download Speed
fig1 = px.line(filtered_df, x="timestamp", y="download_speed", markers=True, title="Download Speed Over Time")
fig1.update_layout(xaxis_title="Timestamp", yaxis_title="Download Speed (Mbps)", template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Plot Upload Speed
fig2 = px.line(filtered_df, x="timestamp", y="upload_speed", markers=True, title="Upload Speed Over Time", color_discrete_sequence=["green"])
fig2.update_layout(xaxis_title="Timestamp", yaxis_title="Upload Speed (Mbps)", template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# Plot Ping
fig3 = px.line(filtered_df, x="timestamp", y="ping", markers=True, title="Ping Over Time", color_discrete_sequence=["red"])
fig3.update_layout(xaxis_title="Timestamp", yaxis_title="Ping (ms)", template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

# Summary Statistics
st.sidebar.header("Summary Statistics")
st.sidebar.write("### Download Speed")
st.sidebar.write(f"Max: {filtered_df['download_speed'].max()} Mbps")
st.sidebar.write(f"Min: {filtered_df['download_speed'].min()} Mbps")
st.sidebar.write(f"Average: {filtered_df['download_speed'].mean():.2f} Mbps")

st.sidebar.write("### Upload Speed")
st.sidebar.write(f"Max: {filtered_df['upload_speed'].max()} Mbps")
st.sidebar.write(f"Min: {filtered_df['upload_speed'].min()} Mbps")
st.sidebar.write(f"Average: {filtered_df['upload_speed'].mean():.2f} Mbps")

st.sidebar.write("### Ping")
st.sidebar.write(f"Max: {filtered_df['ping'].max()} ms")
st.sidebar.write(f"Min: {filtered_df['ping'].min()} ms")
st.sidebar.write(f"Average: {filtered_df['ping'].mean():.2f} ms")