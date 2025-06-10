import streamlit as st

# Set the title of the app
st.title("Hello, Streamlit!")

# Display a subtitle
st.subheader("A simple Hello World example")

# Display some text
st.write("This is a basic Streamlit app for demonstration purposes.")

# Create a text input widget
name = st.text_input("Enter your name:", "")

# When the user enters a name, greet them
if name:
    st.write(f"Hello, {name}! 👋")

# Add a slider as an additional example widget
number = st.slider("Pick a number", 0, 10, 5)
st.write(f"You selected the number: {number}")