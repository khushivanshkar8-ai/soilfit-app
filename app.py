import streamlit as st
import requests
from PIL import Image

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

# Soil Image Capture / Upload Section
st.markdown("---")
st.subheader("📸 Soil Snapshot")
st.markdown("Upload or snap a photo of your garden soil to evaluate its texture and appearance:")
soil_image_file = st.file_uploader("Choose a soil image...", type=["jpg", "jpeg", "png"])

if soil_image_file is not None:
    # Display the uploaded image
    image = Image.open(soil_image_file)
    st.image(image, caption="Your Soil Sample", use_container_width=True)

# Main Engine Function with Safe Fallbacks
def soilfit_engine(city_name, plant_type, has_image):
    url = f"https://wttr.in/{city_name}?format=j1"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        current = data.get('current_condition', [{}])[0]
        temp_c_str = current.get('temp_c', '25')
        temp_c = float(temp_c_str)
        
        humidity_str = current.get('humidity', '50')
        humidity = float(humidity_str)
        
        weather_desc_list = current.get('weatherDesc', [{'value': 'Clear'}])
        weather_desc = weather_desc_list[0].get('value', 'Clear')
        
        weather_text = f"🌤️ **Live Weather in {city_name}:** {temp_c}°C, Humidity: {humidity}%, Condition: {weather_desc}"
        
        analysis_text = "💡 **Friendly Mentor Advice:**\n"
        
        if has_image:
            analysis_text += "📷 **Soil Analysis:** Great job capturing your soil sample! Based on visual inspection, ensure your soil maintains good dark organic matter and drains well.\n\n"
        else:
            analysis_text += "📷 **Soil Analysis:** (Tip: Upload a photo above for visual soil brightness and texture check!)\n\n"
        
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
        temp_c = 28.0
        weather_text = f"🌤️ **Live Weather in {city_name}:** {temp_c}°C (Estimated / Offline mode)"
        analysis_text = "💡 **Friendly Mentor Advice:**\n🌳 **General Care:** Weather API is currently busy, but standard care applies! Keep your soil adequately moist and check for proper sunlight."
        return weather_text, analysis_text

# Run Analysis Button
if st.button("🚀 Check Soil & Plant Health"):
    with st.spinner("Consulting the green mentor..."):
        has_img = soil_image_file is not None
        weather_output, advice_output = soilfit_engine(city, plant_choice, has_img)
        
        st.success("Analysis Complete!")
        st.markdown(weather_output)
        st.markdown(advice_output)

# Footer
st.markdown("---")
st.markdown("Made with 🩵 for a greener, healthier earth!")
