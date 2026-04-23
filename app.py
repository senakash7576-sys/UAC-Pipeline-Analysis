import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 UAC Pipeline Dashboard")

# FIXED CSV READ
df = pd.read_csv("data.csv", sep=",")

st.write("Columns:", df.columns)  # debug

df.columns = df.columns.str.strip()

# Clean numeric
for col in df.columns:
    if col != 'Date':
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.fillna(0)

# SAFE ACCESS
cbp_col = df.columns[2]
transfer_col = df.columns[3]

df['Transfer_Efficiency'] = np.where(
    df[cbp_col] == 0, 0,
    df[transfer_col] / df[cbp_col]
)

df['Backlog'] = df[cbp_col] - df[transfer_col]

st.line_chart(df['Transfer_Efficiency'])
st.line_chart(df['Backlog'])

st.success("✅ Dashboard running successfully")
