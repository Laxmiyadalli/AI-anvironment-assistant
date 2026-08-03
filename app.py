import streamlit as st
import os
import random
import sqlite3
import requests
from dotenv import load_dotenv

# -----------------------------
# Page Config (must be first)
# -----------------------------

st.set_page_config(
    page_title="EcoGuide AI",
    page_icon="🌱",
    layout="wide"
)

# -----------------------------
# Custom UI Styling (Reference UI Theme)
# -----------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Container Background */
    .stApp {
        background: #F4F1EB;
        background-image: 
            radial-gradient(at 10% 10%, rgba(255, 255, 255, 0.8) 0px, transparent 50%),
            radial-gradient(at 90% 90%, rgba(225, 218, 207, 0.5) 0px, transparent 50%);
        color: #2D3136;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #EAE5DC !important;
        border-right: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 4px 0px 20px rgba(0, 0, 0, 0.03);
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #23272A !important;
        font-weight: 700;
    }

    /* Header styling */
    h1 {
        font-weight: 800 !important;
        color: #1A1D20 !important;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        font-weight: 700 !important;
        color: #2C3035 !important;
    }

    /* Buttons - Pill Shape & Soft 3D Shadow */
    .stButton > button {
        background: linear-gradient(135deg, #00875A 0%, #006644 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        box-shadow: 0px 8px 16px rgba(0, 135, 90, 0.25), inset 0px 1px 0px rgba(255, 255, 255, 0.3) !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 12px 20px rgba(0, 135, 90, 0.35), inset 0px 1px 0px rgba(255, 255, 255, 0.4) !important;
        background: linear-gradient(135deg, #009664 0%, #00734D 100%) !important;
    }

    /* Cards / Containers / Expanders */
    [data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        border-radius: 20px;
    }

    .stAlert {
        border-radius: 18px !important;
        border: none !important;
        box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.04), -4px -4px 12px rgba(255, 255, 255, 0.7) !important;
    }

    /* Text Inputs & Selectboxes */
    .stTextInput > div > div > input, .stSelectbox > div > div {
        background-color: #FDFBF7 !important;
        border-radius: 16px !important;
        border: 1px solid #E2DCD2 !important;
        box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.03), 0px 4px 10px rgba(255, 255, 255, 0.8) !important;
        color: #2C3035 !important;
        padding: 10px 16px !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #00875A !important;
        box-shadow: 0 0 0 3px rgba(0, 135, 90, 0.15) !important;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background: #F8F5EF !important;
        padding: 16px 20px !important;
        border-radius: 18px !important;
        box-shadow: 6px 8px 18px rgba(0, 0, 0, 0.05), -4px -4px 12px rgba(255, 255, 255, 0.9) !important;
        border: 1px solid #EAE4D9 !important;
    }

    [data-testid="stMetricValue"] {
        color: #00875A !important;
        font-weight: 800 !important;
    }

    /* Expander Card */
    .streamlit-expanderHeader {
        background: #FAF7F2 !important;
        border-radius: 16px !important;
        font-weight: 600 !important;
    }

    /* Custom Accent Card Highlights */
    .stInfo {
        background: #EBF5F0 !important;
        color: #0F5236 !important;
    }

    .stSuccess {
        background: #E6F7EF !important;
        color: #085232 !important;
    }

    .stWarning {
        background: #FFF4E5 !important;
        color: #8A4B00 !important;
    }

    .stError {
        background: #FDF0ED !important;
        color: #9E1C00 !important;
    }

    /* Radio buttons */
    .stRadio > div {
        background: #FAF8F3;
        padding: 14px 20px;
        border-radius: 18px;
        box-shadow: inset 1px 1px 3px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Load .env
# -----------------------------

load_dotenv()
# Accept either GEMINI_API_KEY or GOOGLE_API_KEY from .env
env_key = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")

# -----------------------------
# Sidebar: Model + Menu
# -----------------------------

st.sidebar.title("⚙️ Settings")

model_choice = st.sidebar.selectbox(
    "🤖 Gemini Model",
    [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
    ],
    help="Select which Gemini model to use"
)

st.sidebar.divider()

menu = st.sidebar.selectbox(
    "📋 Choose Feature",
    [
        "AI Environment Chatbot",
        "Daily Eco Tips",
        "Waste Segregation",
        "Carbon Calculator",
        "Climate Change",
        "Recycling Guide",
        "Water Conservation",
        "Renewable Energy",
        "Environmental Quiz"
    ]
)

# -----------------------------
# Auth — read silently from .env
# -----------------------------

api_key = env_key.strip()
api_key_valid = bool(api_key)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

# -----------------------------
# Database
# -----------------------------

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(
    question TEXT,
    answer TEXT
)
""")
conn.commit()

# -----------------------------
# Page Title
# -----------------------------

st.title("🌱 EcoGuide AI")
st.write("Your intelligent environmental assistant")
st.caption(f"Using model: **{model_choice}**")

# -----------------------------
# Gemini AI Function (REST API)
# -----------------------------

def ask_ai(prompt_text):
    """Send prompt to Gemini REST API and return response text."""
    if not api_key_valid:
        return None, "⚠️ AI is not configured. Please add GEMINI_API_KEY to your .env file."
    try:
        url = f"{GEMINI_API_URL}/{model_choice}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}]
        }
        response = requests.post(url, json=payload, timeout=60)
        data = response.json()

        if response.status_code == 200:
            # Extract text from response
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text, None
        else:
            error_msg = data.get("error", {}).get("message", "Unknown error")
            code = response.status_code
            if code == 429:
                return None, "⚠️ Rate limit reached. Please wait a minute and try again."
            elif code == 404:
                return None, f"❌ Model '{model_choice}' not available. Try a different model from the sidebar."
            elif code == 403:
                return None, "❌ API key rejected. Please check your key in the .env file."
            else:
                return None, f"❌ API Error ({code}): {error_msg}"
    except requests.exceptions.Timeout:
        return None, "⚠️ Request timed out. Please try again."
    except Exception as e:
        return None, f"❌ Unexpected error: {str(e)}"

# -----------------------------
# 1. AI CHATBOT
# -----------------------------

if menu == "AI Environment Chatbot":

    st.subheader("🤖 AI Environment Chatbot")

    question = st.text_input("Ask your environmental question", placeholder="e.g. What is climate change?")

    if st.button("Generate Answer", key="chatbot_btn"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            prompt = f"""
You are EcoGuide AI, an expert environmental assistant.

Answer the following environmental question clearly and helpfully.

Include:
1. Definition
2. Causes
3. Effects
4. Solutions
5. Eco Tip

Question: {question}
"""
            with st.spinner("Thinking..."):
                answer, error = ask_ai(prompt)

            if error:
                st.error(error)
            else:
                st.success("✅ AI Response")
                st.write(answer)
                cursor.execute(
                    "INSERT INTO chat_history VALUES (?, ?)",
                    (question, answer)
                )
                conn.commit()

    # Show chat history
    with st.expander("📜 Chat History"):
        rows = cursor.execute("SELECT question, answer FROM chat_history ORDER BY rowid DESC LIMIT 10").fetchall()
        if rows:
            for q, a in rows:
                st.markdown(f"**Q:** {q}")
                st.markdown(f"**A:** {a[:300]}...")
                st.divider()
        else:
            st.write("No history yet.")

# -----------------------------
# 2. DAILY ECO TIPS
# -----------------------------

elif menu == "Daily Eco Tips":

    st.subheader("🌱 Daily Eco Tips")

    if st.button("Get AI Eco Tips", key="tips_btn"):
        prompt = "Give me 10 practical and creative eco-friendly tips for daily life. Format as a numbered list."
        with st.spinner("Generating tips..."):
            answer, error = ask_ai(prompt)
        if error:
            st.error(error)
        else:
            st.success("✅ Today's Eco Tips")
            st.write(answer)
    else:
        quick_tips = [
            "🛍️ Use reusable bags instead of plastic bags",
            "🌳 Plant more trees in your area",
            "💡 Save electricity — turn off lights when not needed",
            "🚌 Use public transport to reduce emissions",
            "🍽️ Reduce food waste by planning meals",
            "🚰 Fix leaking taps immediately",
            "♻️ Segregate waste for proper recycling",
            "🚿 Take shorter showers to save water",
            "🌿 Compost kitchen waste",
            "☀️ Switch to solar energy where possible"
        ]
        st.info(f"💡 Tip of the moment: **{random.choice(quick_tips)}**")
        st.write("Click **Get AI Eco Tips** for personalized suggestions from AI!")

# -----------------------------
# 3. WASTE SEGREGATION
# -----------------------------

elif menu == "Waste Segregation":

    st.subheader("♻️ Waste Segregation Guide")

    waste = st.text_input("Enter waste item to check", placeholder="e.g. plastic bottle, banana peel, battery")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Quick Check", key="waste_quick"):
            if not waste.strip():
                st.warning("Please enter a waste item.")
            else:
                recyclable = ["paper", "glass", "plastic bottle", "metal", "cardboard", "aluminum", "tin", "newspaper"]
                organic = ["banana peel", "food waste", "vegetable", "fruit", "leaves", "eggshell"]
                hazardous = ["battery", "paint", "chemicals", "medicine", "electronics", "bulb"]

                w = waste.lower().strip()
                if any(r in w for r in recyclable):
                    st.success("♻️ **Recyclable** — Put in the blue/green recycling bin.")
                elif any(o in w for o in organic):
                    st.success("🌱 **Organic/Biodegradable** — Compost it or use the brown bin.")
                elif any(h in w for h in hazardous):
                    st.error("⚠️ **Hazardous Waste** — Take to a special disposal center. Do NOT put in regular bins.")
                else:
                    st.warning("🤔 Unknown item — Use AI Check for detailed guidance.")

    with col2:
        if st.button("🤖 AI Check", key="waste_ai"):
            if not waste.strip():
                st.warning("Please enter a waste item.")
            else:
                prompt = f"""
Explain how to dispose of: {waste}

Include:
- Category (recyclable / organic / hazardous / general)
- Correct bin color
- Disposal method
- Environmental impact if disposed incorrectly
"""
                with st.spinner("Checking with AI..."):
                    answer, error = ask_ai(prompt)
                if error:
                    st.error(error)
                else:
                    st.write(answer)

# -----------------------------
# 4. CARBON CALCULATOR
# -----------------------------

elif menu == "Carbon Calculator":

    st.subheader("🏭 Carbon Footprint Calculator")

    col1, col2 = st.columns(2)
    with col1:
        km = st.number_input("🚗 Vehicle distance per day (km)", min_value=0.0, value=0.0, step=1.0)
        electricity = st.number_input("⚡ Monthly electricity usage (kWh)", min_value=0.0, value=0.0, step=10.0)
    with col2:
        flights = st.number_input("✈️ Short flights per year", min_value=0, value=0, step=1)
        meat_meals = st.number_input("🥩 Meat meals per week", min_value=0, value=0, step=1)

    if st.button("Calculate Carbon Footprint", key="carbon_btn"):
        vehicle_carbon = km * 0.21 * 365
        electricity_carbon = electricity * 0.5 * 12
        flight_carbon = flights * 255
        food_carbon = meat_meals * 3.3 * 52

        total = vehicle_carbon + electricity_carbon + flight_carbon + food_carbon

        st.success(f"🌍 Your estimated annual carbon footprint: **{total:.1f} kg CO₂**")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🚗 Vehicle", f"{vehicle_carbon:.0f} kg")
        col2.metric("⚡ Electricity", f"{electricity_carbon:.0f} kg")
        col3.metric("✈️ Flights", f"{flight_carbon:.0f} kg")
        col4.metric("🥩 Food", f"{food_carbon:.0f} kg")

        if total < 2000:
            st.success("🌟 Great! Your footprint is below average.")
        elif total < 5000:
            st.warning("⚠️ Your footprint is average. Try reducing it!")
        else:
            st.error("🔴 High footprint! Consider making eco-friendly changes.")

# -----------------------------
# 5. CLIMATE CHANGE
# -----------------------------

elif menu == "Climate Change":

    st.subheader("🌡️ Climate Change")

    topic = st.text_input("Ask about climate change", placeholder="e.g. What is global warming?")

    if st.button("Get AI Explanation", key="climate_btn"):
        if not topic.strip():
            prompt = "Explain climate change in simple language — causes, effects, and what we can do to stop it."
        else:
            prompt = f"Explain this climate change topic in simple, clear language: {topic}"

        with st.spinner("Explaining..."):
            answer, error = ask_ai(prompt)
        if error:
            st.error(error)
        else:
            st.write(answer)
    else:
        st.info("""
**🌡️ What is Climate Change?**

Climate change refers to long-term shifts in global temperatures and weather patterns.

**Main Causes:**
- 🏭 Burning fossil fuels (coal, oil, gas)
- 🌲 Deforestation
- 🐄 Agriculture and livestock

**Key Effects:**
- Rising sea levels
- Extreme weather events
- Loss of biodiversity

**Solutions:**
- ☀️ Switch to renewable energy
- 🌳 Plant trees
- 🚲 Use sustainable transport

👆 Type a topic above and click **Get AI Explanation** for detailed info!
""")

# -----------------------------
# 6. RECYCLING GUIDE
# -----------------------------

elif menu == "Recycling Guide":

    st.subheader("♻️ Recycling Guide")

    item = st.text_input("Enter an item to learn how to recycle it", placeholder="e.g. old phone, plastic bag, newspaper")

    if st.button("Get Recycling Guide", key="recycle_btn") and item.strip():
        prompt = f"Provide a clear recycling guide for: {item}\n\nInclude: how to prepare it for recycling, where to recycle, and environmental benefit."
        with st.spinner("Looking up..."):
            answer, error = ask_ai(prompt)
        if error:
            st.error(error)
        else:
            st.write(answer)
    else:
        st.markdown("""
**General Recycling Steps:**

1. 📦 **Collection** — Separate recyclables from regular waste
2. 🔄 **Sorting** — Sort by material (paper, plastic, glass, metal)
3. 🏭 **Processing** — Recyclables are cleaned and processed
4. 🛍️ **Manufacturing** — Made into new products

**Benefits:**
- Reduces landfill waste
- Saves natural resources
- Reduces pollution
- Creates jobs

**What can be recycled?**
- 📄 Paper & Cardboard
- 🍶 Glass bottles & jars
- 🥫 Metal cans & tins
- 🧴 Plastic bottles (check the number)
""")

# -----------------------------
# 7. WATER CONSERVATION
# -----------------------------

elif menu == "Water Conservation":

    st.subheader("💧 Water Conservation")

    if st.button("Get AI Water Tips", key="water_btn"):
        prompt = "Give 10 practical water conservation tips for home use. Include tips for kitchen, bathroom, garden, and daily habits."
        with st.spinner("Generating..."):
            answer, error = ask_ai(prompt)
        if error:
            st.error(error)
        else:
            st.write(answer)
    else:
        st.markdown("""
**💧 Quick Water Saving Tips:**

🚿 **Bathroom**
- Take shorter showers (5 min max)
- Fix leaking taps immediately
- Turn off tap while brushing teeth

🍽️ **Kitchen**
- Wash vegetables in a bowl, not under running water
- Reuse cooking water for plants
- Run dishwasher only when full

🌿 **Garden**
- Water plants in early morning or evening
- Collect rainwater for irrigation
- Use drought-resistant plants

🏠 **General**
- Check for leaks regularly
- Install water-efficient fixtures
- Reuse greywater where possible

👆 Click **Get AI Water Tips** for personalized advice!
""")

# -----------------------------
# 8. RENEWABLE ENERGY
# -----------------------------

elif menu == "Renewable Energy":

    st.subheader("☀️ Renewable Energy")

    topic = st.text_input("Ask about renewable energy", placeholder="e.g. How do solar panels work?")

    if st.button("Get AI Info", key="energy_btn"):
        if not topic.strip():
            prompt = "Give an overview of all major renewable energy types: solar, wind, hydro, biomass, and geothermal. Include advantages and disadvantages of each."
        else:
            prompt = f"Explain this renewable energy topic clearly: {topic}"
        with st.spinner("Loading..."):
            answer, error = ask_ai(prompt)
        if error:
            st.error(error)
        else:
            st.write(answer)
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.info("☀️ **Solar Energy**\nConverts sunlight into electricity using photovoltaic panels.")
            st.info("🌬️ **Wind Energy**\nUses wind turbines to generate electricity.")
            st.info("💧 **Hydropower**\nGenerates electricity from flowing water.")
        with col2:
            st.info("🌱 **Biomass**\nEnergy from organic materials like wood and crop waste.")
            st.info("🌋 **Geothermal**\nHeat energy from inside the Earth.")
            st.info("🌊 **Tidal Energy**\nPower from ocean tides and waves.")

# -----------------------------
# 9. ENVIRONMENTAL QUIZ
# -----------------------------

elif menu == "Environmental Quiz":

    st.subheader("🧠 Environmental Quiz")

    quiz_questions = [
        {
            "q": "Which gas is the primary cause of global warming?",
            "options": ["Oxygen", "Carbon Dioxide (CO₂)", "Nitrogen", "Hydrogen"],
            "answer": "Carbon Dioxide (CO₂)",
            "explanation": "CO₂ from burning fossil fuels traps heat in the atmosphere, causing global warming."
        },
        {
            "q": "What percentage of Earth's surface is covered by water?",
            "options": ["50%", "61%", "71%", "85%"],
            "answer": "71%",
            "explanation": "About 71% of Earth's surface is covered by water, but only 3% is fresh water."
        },
        {
            "q": "Which is NOT a renewable energy source?",
            "options": ["Solar", "Wind", "Natural Gas", "Hydropower"],
            "answer": "Natural Gas",
            "explanation": "Natural gas is a fossil fuel — a non-renewable energy source."
        },
        {
            "q": "What does the 3R principle stand for?",
            "options": ["Run, Rest, Repeat", "Reduce, Reuse, Recycle", "Read, Research, Report", "Renew, Rebuild, Restore"],
            "answer": "Reduce, Reuse, Recycle",
            "explanation": "The 3Rs are the foundation of waste management: Reduce consumption, Reuse items, Recycle materials."
        },
        {
            "q": "Which layer of the atmosphere protects us from UV radiation?",
            "options": ["Troposphere", "Stratosphere (Ozone Layer)", "Mesosphere", "Thermosphere"],
            "answer": "Stratosphere (Ozone Layer)",
            "explanation": "The ozone layer in the stratosphere absorbs most of the Sun's harmful ultraviolet radiation."
        }
    ]

    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.score = 0
        st.session_state.answered = False

    idx = st.session_state.quiz_index

    if idx < len(quiz_questions):
        current = quiz_questions[idx]
        st.write(f"**Question {idx + 1} of {len(quiz_questions)}:**")
        st.write(f"### {current['q']}")

        selected = st.radio("Choose your answer:", current["options"], key=f"quiz_{idx}")

        if st.button("Submit Answer", key=f"submit_{idx}") and not st.session_state.answered:
            st.session_state.answered = True
            if selected == current["answer"]:
                st.success(f"✅ Correct! {current['explanation']}")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! The correct answer is: **{current['answer']}**\n\n{current['explanation']}")

        if st.session_state.answered:
            if st.button("Next Question ➡️", key=f"next_{idx}"):
                st.session_state.quiz_index += 1
                st.session_state.answered = False
                st.rerun()
    else:
        score = st.session_state.score
        total = len(quiz_questions)
        st.balloons()
        st.success(f"🎉 Quiz Complete! Your score: **{score}/{total}**")
        if score == total:
            st.write("🏆 Perfect score! You're an eco champion!")
        elif score >= total // 2:
            st.write("🌱 Good job! Keep learning about the environment.")
        else:
            st.write("📚 Keep studying — our planet needs informed citizens!")

        if st.button("🔄 Restart Quiz"):
            st.session_state.quiz_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.rerun()
