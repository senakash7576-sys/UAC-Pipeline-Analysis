import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 UAC Pipeline Dashboard")

# Load data
df = pd.read_csv("data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# DEBUG (optional)
st.write("Columns:", df.columns)

# 🔥 SAFE COLUMN ACCESS (index based)
cbp_col = df.columns[2]          # Children in CBP custody
transfer_col = df.columns[3]     # Children transferred out

# Clean numeric data
for col in df.columns:
    if col != 'Date':
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.fillna(0)

# KPI
df['Transfer_Efficiency'] = np.where(
    df[cbp_col] == 0,
    0,
    df[transfer_col] / df[cbp_col]
)

df['Backlog'] = df[cbp_col] - df[transfer_col]

# Charts
st.subheader("Transfer Efficiency")
st.line_chart(df['Transfer_Efficiency'])

st.subheader("Backlog")
st.line_chart(df['Backlog'])

st.success("✅ Dashboard running successfully")
