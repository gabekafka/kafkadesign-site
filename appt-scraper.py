import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

st.title("Apartment Listing Checker")

URL = st.text_input("Paste apartment URL:", "https://example.com/apartments")

if st.button("Check for Listings"):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.get(URL)
        time.sleep(5)  # wait for JavaScript to load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        listings = [a.text.strip() for a in soup.find_all("a") if a.text.strip().startswith("#")]
        if listings:
            st.success(f"Found {len(listings)} listing(s):")
            for listing in listings:
                st.write("-", listing)
        else:
            st.warning("No listings found.")
    except Exception as e:
        st.error(f"Error fetching listings: {e}")