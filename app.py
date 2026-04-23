import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 UAC Pipeline Dashboard")

# Load data
df = pd.read_csv("data.csv")

# Clean data
cols = [
    'Children apprehended and placed in CBP custody*',
    'Children in CBP custody',
    'Children transferred out of CBP custody',
    'Children in HHS Care',
    'Children discharged from HHS Care'
]

for col in cols:
    df[col] = df[col].astype(str).str.replace(',', '')
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.fillna(0)

# KPI
df['Transfer_Efficiency'] = np.where(
    df['Children in CBP custody'] == 0, 0,
    df['Children transferred out of CBP custody'] / df['Children in CBP custody']
)

df['Backlog'] = df['Children in CBP custody'] - df['Children transferred out of CBP custody']

# Show data
st.line_chart(df['Transfer_Efficiency'])
st.line_chart(df['Backlog'])