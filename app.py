import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 UAC Pipeline Dashboard")

# Load data
df = pd.read_csv("data.csv")

# 🔥 FIX 1: Clean column names
df.columns = df.columns.str.strip()

# 🔍 DEBUG (temporary)
st.write("Columns:", df.columns)

# 🔥 FIX 2: Use dynamic columns (no hardcoding)
for col in df.columns:
    if col != 'Date':
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.fillna(0)

# 🔥 FIX 3: Use correct column names (copy from output if needed)
df['Transfer_Efficiency'] = np.where(
    df['Children in CBP custody'] == 0,
    0,
    df['Children transferred out of CBP custody'] / df['Children in CBP custody']
)

df['Backlog'] = df['Children in CBP custody'] - df['Children transferred out of CBP custody']

# Charts
st.subheader("Transfer Efficiency")
st.line_chart(df['Transfer_Efficiency'])

st.subheader("Backlog")
st.line_chart(df['Backlog'])
