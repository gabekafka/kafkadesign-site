import streamlit as st

st.title("Streamlit Structural Terminal")

command = st.text_input("Enter a command (e.g., W12X16)")

if command:
    st.write(f"> {command}")
    st.info("Shape lookup and calculations will appear here in the future.")
else:
    st.write("Type a shape name or command above to begin.") 