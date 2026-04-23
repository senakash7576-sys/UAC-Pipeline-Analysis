import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 UAC Pipeline Dashboard")

df = pd.read_csv("clean_data.csv", sep=",", engine="python", quotechar='"')

st.write("Shape:", df.shape)

df.columns = df.columns.str.strip()

# SAFE COLUMN FIND
cbp_col = None
transfer_col = None

for col in df.columns:
    if "CBP custody" in col and "in" in col:
        cbp_col = col
    if "transferred" in col:
        transfer_col = col

st.write("Using:", cbp_col, transfer_col)

# Clean numeric
for col in df.columns:
    if col != 'Date':
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.fillna(0)

# KPI
df['Transfer_Efficiency'] = np.where(
    df[cbp_col] == 0, 0,
    df[transfer_col] / df[cbp_col]
)

df['Backlog'] = df[cbp_col] - df[transfer_col]

st.line_chart(df['Transfer_Efficiency'])
st.line_chart(df['Backlog'])

st.success("✅ Dashboard running successfully")
