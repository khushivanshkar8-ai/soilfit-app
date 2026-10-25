import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import os

def soilfit_engine(city, plant_choice):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        data = response.json()
        current = data['current_condition'][0]
        temp_c = float(current['temp_C'])
        humidity = float(current['humidity'])
        weather_desc = current['weatherDesc'][0]['value']

        weather_text = f"🌍 **Live Weather in {city}**\n* **Temperature:** {temp_c}°C ({weather_desc})\n* **Air Moisture:** {humidity}%"

        analysis_text = f"💡 **Friendly Mentor Advice for your {plant_choice}**:\n\n"

        if "Tree" in plant_choice:
            if 20 <= temp_c <= 38:
                analysis_text += "🌳 **Tree Happiness**: The weather outside is fantastic! Your tree can stretch its roots and grow big and strong.\n"
            else:
                analysis_text += "⚠️ **Weather Watch**: It's a bit too hot or chilly out there! Wrap a warm blanket of dry leaves (mulch) around the roots to keep them cozy.\n"
        elif any(flower in plant_choice for flower in ["Rose", "Marigold", "Hibiscus", "Jasmine"]):
            if 15 <= temp_c <= 30:
                analysis_text += "🌸 **Flower Power**: Perfect weather for growing bright, colorful petals and happy little buds!\n"
            else:
                analysis_text += "⚠️ **Weather Watch**: The temperature is acting a bit tricky. Give your flowers a nice shaded spot during the super hot afternoon hours so they don't get tired.\n"
        else:
            if 18 <= temp_c <= 28:
                analysis_text += "🌱 **Crop Comfort**: Amazing weather! Your plant is soaking up the sun and getting all the energy it needs.\n"
            else:
                analysis_text += "⚠️ **Weather Watch**: The air feels a bit harsh today. Check the soil often to make sure your plant has enough water to drink!\n"

        if humidity > 70:
            analysis_text += f"\n🌧️ **Super Wet Air ({humidity}%)**: The air feels very heavy and watery. Give your plants extra breathing room, and remember to water them only in the morning sun!"
        elif humidity < 30:
            analysis_text += f"\n🏜️ **Super Dry Air ({humidity}%)**: The air is extra thirsty today and drinking up moisture fast. Give their leaves a gentle splash of water to help them stay fresh!"
        else:
            analysis_text += f"\n✨ **Just Right ({humidity}%)**: The air is nice and balanced, making it super easy for your plant to breathe comfortably."

    except Exception as e:
        weather_text = "⚠️ Oops! We couldn't catch the live weather right now."
        analysis_text = "Please check your internet connection or city spelling."

    image_url = "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=500"
    img_resp = requests.get(image_url)
    ref_img = Image.open(BytesIO(img_resp.content))

    report_filename = "soilfit_care_report.txt"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(f"SOILFIT MENTOR CARE REPORT\n==========================\nTarget: {plant_choice}\nLocation: {city}\n\n{weather_text}\n\n{analysis_text}")

    return weather_text, analysis_text, ref_img, report_filename

def analyze_soil_image(img):
    if img is None:
        return "⚠️ Please take or upload a clear photo of your soil first!", None

    img_arr = np.array(img)
    brightness = np.mean(img_arr)
    red_bias = np.mean(img_arr[:, :, 0])
    green_bias = np.mean(img_arr[:, :, 1])

    result = "### 🔬 Magic Soil Checker & Fun Story Diagnosis\n\n"

    if brightness < 80:
        result += "🟢 **Soil Grade: Super Chocolate Cake Soil (Rich Humus - Grade A+)**\n"
        result += "* **What it looks like:** Dark, rich, spongy, and looks just like yummy chocolate cake crumbs!\n"
        result += "* **Plant Superpower:** Packed with magical plant vitamins and tiny helpful earth helpers (microbes).\n"
        result += "* **Best Friends:** Loves growing colorful flowers, juicy fruits, and big happy trees.\n"
        result += "* **💧 Drink Schedule:** Give it a nice drink every 3 to 4 days, best done right when the sun wakes up in the morning.\n\n"
        result += "🧠 **Why this is awesome:**\n"
        result += "This soil acts like a sponge that holds onto all the best food for your plants. Just remember not to drown it with too much water, and gently fluff the top layer once a month so the roots can breathe fresh air!"

    elif brightness > 160 or red_bias > 140:
        result += "🟡 **Soil Grade: Slip-Slidey Sandy Soil (Needs Our Help!)**\n"
        result += "* **What it looks like:** Light brown, greyish, or reddish, and feels very gritty like a beach.\n"
        result += "* **Plant Superpower:** Water slips right through it like a slide before the plant can catch a drink!\n"
        result += "* **Best Friends:** Tough little plants and roots that don't mind a quick drink.\n"
        result += "* **💧 Drink Schedule:** Needs little sips of water more often (every 1 or 2 days).\n\n"
        result += "🧠 **Why this happens & How to fix it:**\n"
        result += "⚠️ **The trouble:** Sandy soil has big gaps, so water and food fall straight to the bottom and run away!\n"
        + "💡 **Our Fun Fix:** Let's mix in some yummy organic kitchen compost or veggie scraps to turn it into rich garden soil. Put a cozy blanket of leaves on top to stop the sun from stealing its moisture!"

    else:
        result += "🔵 **Soil Grade: The Golden Magic Mix (Balanced Garden Loam)**\n"
        result += "* **What it looks like:** Rich brown, smooth, soft, and easy to shape like play-dough!\n"
        result += "* **Plant Superpower:** It holds just the right amount of water while letting extra water drain away easily.\n"
        result += "* **Best Friends:** Literally EVERY plant, tree, and flower in the world loves this soil!\n"
        result += "* **💧 Drink Schedule:** A balanced drink every 3 to 5 days depending on how warm the sun is.\n\n"
        result += "🧠 **Why this is awesome:**\n"
        result += "You hit the jackpot! This is the ultimate happy home for plants. Just feed it a little bit of natural compost once every season to keep its superpower glowing strong!"

    soil_filename = "soilfit_soil_report.txt"
    with open(soil_filename, "w", encoding="utf-8") as f:
        f.write(f"SOILFIT SOIL SCANNER REPORT\n===========================\n\n{result}")

    return result, soil_filename

custom_css = """
body { background-color: #f4f9f4 !important; }
.gradio-container {
    max-width: 800px !important;
    margin: auto !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(40, 100, 60, 0.1) !important;
    background: #ffffff !important;
    padding: 20px !important;
}
.primary-btn {
    background: linear-gradient(135deg, #2e7d32, #66bb6a) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3) !important;
}
"""

with gr.Blocks(theme=gr.themes.Soft(primary_hue="green", secondary_hue="emerald"), css=custom_css) as demo:

    with gr.Row():
        gr.Markdown(
            """
            # 🌱 Soilfit: Your Friendly Green Mentor
            *“Growing any kind of plant, tree, crop, and flower to heal our planet with fun and simple care!”* ✨
            """
        )

    with gr.Tabs():
        with gr.TabItem("🌍 Live Weather & Plant Friend"):
            gr.Markdown("### 🌤️ Check the Weather & Keep Plants Happy")
            with gr.Row():
                city_input = gr.Textbox(label="Your City", value="Bhopal")
                plant_dropdown = gr.Dropdown(
                    label="Choose Your Plant, Tree, or Flower",
                    choices=[
                        "Tomato", "Wheat", "Rice", "Potato",
                        "Mango Tree 🥭", "Neem Tree 🌳", "Teak Tree (Sagwan) 🪵", "Guava Tree 🍈",
                        "Rose 🌹", "Marigold (Genda) 🌼", "Hibiscus (Gudhal) 🌺", "Jasmine (Mogra) 💮"
                    ],
                    value="Neem Tree 🌳"
                )

            run_btn = gr.Button("✨ Check Weather & Advice", elem_classes="primary-btn")

            with gr.Row():
                out_weather = gr.Markdown(label="Live Weather Info")
                out_analysis = gr.Markdown(label="Friendly Mentor Advice")

            with gr.Row():
                out_image = gr.Image(label="Green Inspiration Snapshot")
                download_file = gr.File(label="📥 Download Care Guide")

            run_btn.click(
                fn=soilfit_engine,
                inputs=[city_input, plant_dropdown],
                outputs=[out_weather, out_analysis, out_image, download_file]
            )

        with gr.TabItem("📸 Magic Soil Scanner"):
            gr.Markdown("### 🔍 Snap a Photo of Your Soil")
            gr.Markdown("Take a picture or upload one of your garden soil. Soilfit will check its color like a detective and explain what kind of soil it is in a super fun, easy way!")

            with gr.Row():
                soil_photo = gr.Image(label="Upload or Snap Soil Photo", type="pil")
                scan_btn = gr.Button("🔬 Check Soil Magic & Get Solutions", elem_classes="primary-btn")

            with gr.Row():
                scan_output = gr.Markdown(label="Fun Soil Detective Report")
                download_soil_file = gr.File(label="📥 Download Soil Report")

            scan_btn.click(
                fn=analyze_soil_image,
                inputs=[soil_photo],
                outputs=[scan_output, download_soil_file]
            )

demo.launch(share=True, auth=("soilfit_friend", "krishi2026"))
    
