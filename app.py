def soilfit_engine(city_name, plant_type):
    url = f"https://wttr.in/{city_name}?format=j1"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # Safe extraction with fallback checks
        current = data.get('current_condition', [{}])[0]
        temp_c_str = current.get('temp_c', '25')
        temp_c = float(temp_c_str)
        
        humidity_str = current.get('humidity', '50')
        humidity = float(humidity_str)
        
        weather_desc_list = current.get('weatherDesc', [{'value': 'Clear'}])
        weather_desc = weather_desc_list[0].get('value', 'Clear')
        
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
        # Fallback default values so the app never breaks!
        temp_c = 28.0
        weather_text = f"🌤️ **Live Weather in {city_name}:** {temp_c}°C (Estimated / Offline mode)"
        analysis_text = f"💡 **Friendly Mentor Advice:**\n🌳 **General Care:** Weather API is currently busy, but standard care applies! Keep your soil adequately moist and check for proper sunlight."
        return weather_text, analysis_text
        
