import streamlit as st

st.title("My First Streamlit App")
st.write("Hello, world!")

# A simple slider widget
value = st.slider("Pick a number", 0, 100, 50)
st.write("You picked:", value)