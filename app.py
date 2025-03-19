# app.py
import streamlit as st
import requests
import os

# Streamlit UI
st.title("News Summarization and TTS App")

# Input company name
company_name = st.text_input("Enter Company Name (e.g., Tesla):")

if st.button("Analyze"):
    if company_name:
        # Call the API
        api_url = f"http://localhost:8000/process/{company_name}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            st.write(f"Company: {data['Company']}")
            
            # Display articles
            for article in data["Articles"]:
                st.subheader(article["Title"])
                st.write(f"Summary: {article['Summary']}")
                st.write(f"Sentiment: {article['Sentiment']}")
                st.write(f"Topics: {', '.join(article['Topics'])}")
                st.write("---")
            
            # Comparative analysis
            st.subheader("Comparative Sentiment Score")
            st.write(data["Comparative Sentiment Score"])
            
            # TTS
            tts_url = f"http://localhost:8000/tts/{company_name}"
            tts_response = requests.get(tts_url)
            if tts_response.status_code == 200:
                audio_file = tts_response.json()["audio_file"]
                st.audio(audio_file)
        else:
            st.error("Error fetching data from API")
    else:
        st.warning("Please enter a company name")

# Instructions
st.sidebar.write("Enter a company name and click 'Analyze' to get started!")