import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 UAC Pipeline Dashboard")

# Load data
df = pd.read_csv("data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Clean numeric data
for col in df.columns:
    if col != 'Date':
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.fillna(0)

# KPI calculations
df['Transfer_Efficiency'] = np.where(
    df['Children in CBP custody'] == 0,
    0,
    df['Children transferred out of CBP custody'] / df['Children in CBP custody']
)

df['Backlog'] = df['Children in CBP custody'] - df['Children transferred out of CBP custody']

# Charts
st.subheader("Transfer Efficiency Trend")
st.line_chart(df['Transfer_Efficiency'])

st.subheader("Backlog Trend")
st.line_chart(df['Backlog'])

st.success("✅ Dashboard running successfully")
