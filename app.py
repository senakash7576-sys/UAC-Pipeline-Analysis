import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 UAC Pipeline Dashboard")

df = pd.read_csv("data.csv", engine="python")

st.write("Columns:", df.columns)
st.write("Shape:", df.shape)

df.columns = df.columns.str.strip()

# 🔥 SAFE: name match instead of index
cbp_col = [c for c in df.columns if "CBP custody" in c and "in" in c][0]
transfer_col = [c for c in df.columns if "transferred" in c][0]

# clean
for col in df.columns:
    if col != 'Date':
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.fillna(0)

df['Transfer_Efficiency'] = np.where(
    df[cbp_col] == 0, 0,
    df[transfer_col] / df[cbp_col]
)

df['Backlog'] = df[cbp_col] - df[transfer_col]

st.line_chart(df['Transfer_Efficiency'])
st.line_chart(df['Backlog'])

st.success("✅ Dashboard running successfully")
