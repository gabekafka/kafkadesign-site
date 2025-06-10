import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")
st.title("My Dashboard")
st.sidebar.selectbox("Choose column", df.columns)
st.line_chart(df)