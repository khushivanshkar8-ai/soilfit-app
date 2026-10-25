import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Soilfit - Green Mentor App",
    page_icon="🌱",
    layout="centered"
)

# App Header
st.title("🌱 Soilfit: Your Friendly Green Mentor!")
st.markdown("Welcome, young scientist! Let's check how our soil and plants are doing today! 🩵")

# Sidebar for inputs
st.sidebar.header("🌍 Environmental Setup")
city = st.sidebar.text_input("Enter your city name:", "Jabalpur")
plant_choice = st.sidebar.selectbox(
    "What are you growing?",
    [
        "🌳 Shade Trees & Saplings",
        "🌸 Flowering Garden Plants",
        "🍎 Fruit Trees & Orchards"
    ]
)

# Main Engine Function
def soilfit_engine(city_name, plant_type):
    url = f"https://wttr.in/{city_name}?format=j1"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        current = data['current_condition'][0]
        temp_c = float(current['temp_c'])
        humidity = float(current['humidity'])
        weather_desc = current['weatherDesc'][0]['value']
        
        weather_text = f"🌤️ **Live Weather in {city_name}:** {temp_c}°C, Humidity: {humidity}%, Condition: {weather_desc}"
        
        analysis_text = "💡 **Friendly Mentor Advice:**\n"
        
        if "Tree" in plant_type:
            if 20 <= temp_c <= 38:
                analysis_text += "🌳 **Trees:** Perfect weather for young saplings! Make sure to give them a deep watering near the roots."
            else:
                analysis_text += "⚠️ **Trees:** Temperatures are a bit extreme. Protect young saplings with some shade or extra mulch!"
        elif "Flower" in plant_type:
            if 15 <= temp_c <= 30:
                analysis_text += "🌸 **Flowers:** Beautiful blooming weather! Keep the soil moist but not soggy."
            else:
                analysis_text += "⚠️ **Flowers:** Check your flower beds daily—extreme heat or cold means they might need extra attention."
        else:
            if 18 <= temp_c <= 32:
                analysis_text += "🍎 **Fruit Trees:** Great conditions for fruit development! Ensure steady watering."
            else:
                analysis_text += "⚠️ **Fruit Trees:** Keep an eye on soil moisture and protect fruit blossoms from harsh weather."
                
        return weather_text, analysis_text

    except Exception as e:
        return "⚠️ Could not fetch live weather right now.", f"Error: {e}"

# Run Analysis Button
if st.button("🚀 Check Soil & Plant Health"):
    with st.spinner("Consulting the green mentor..."):
        weather_output, advice_output = soilfit_engine(city, plant_choice)
        
        st.success("Analysis Complete!")
        st.markdown(weather_output)
        st.markdown(advice_output)

# Footer
st.markdown("---")
st.markdown("Made with 🩵 for a greener, healthier earth!")
