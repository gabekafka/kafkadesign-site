import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Apartment Listing Checker")

URL = st.text_input("Paste apartment URL:", "https://example.com/apartments")

if st.button("Check for Listings"):
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        listings = [item.text.strip() for item in soup.find_all("h2")]
        if listings:
            st.success(f"Found {len(listings)} listing(s):")
            for listing in listings:
                st.write("-", listing)
        else:
            st.warning("No listings found.")
    except Exception as e:
        st.error(f"Error fetching listings: {e}")