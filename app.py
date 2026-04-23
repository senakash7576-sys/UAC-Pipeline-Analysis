import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 UAC Pipeline Dashboard")

df = pd.read_csv("data.csv")
st.write(df.columns)

# Clean column names
df.columns = df.columns.str.strip()

# DEBUG (देखो actual names)
st.write("Columns:", df.columns)

# 🔥 AUTO DETECT COLUMNS
cbp_col = [c for c in df.columns if "CBP custody" in c and "in" in c][0]
transfer_col = [c for c in df.columns if "transferred" in c][0]

# Clean numeric
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
st.line_chart(df['Transfer_Efficiency'])
st.line_chart(df['Backlog'])
