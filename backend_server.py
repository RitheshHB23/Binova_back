import streamlit as st
import pandas as pd
import random
import pydeck as pdk

# --- PAGE SETUP ---
st.set_page_config(
    page_title="BINOVA – Smart Dustbin Monitor",
    layout="wide",
)

# --- STYLE (COLOURFUL UI) ---
st.markdown("""
    <style>
        .title {
            text-align: center;
            color: #4A90E2;
            font-size: 45px;
            font-weight: 700;
        }
        .sub {
            color: #F39C12;
            font-size: 25px;
            font-weight: 600;
        }
        body {
            background-color: #F0F4F8;
        }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<div class='title'>🚮 BINOVA – Smart Dustbin Worker App</div>", unsafe_allow_html=True)
st.write("### A colourful prototype dashboard for workers. (No IoT required)")

# ---- PROTOTYPE DATA ----
dustbins = [
    {"id": "BIN-101", "location": "Main Road", "lat": 12.9716, "lon": 77.5946, "fill": random.randint(20, 100)},
    {"id": "BIN-102", "location": "Bus Stand", "lat": 12.9725, "lon": 77.5952, "fill": random.randint(20, 100)},
    {"id": "BIN-103", "location": "Market Street", "lat": 12.9730, "lon": 77.5938, "fill": random.randint(20, 100)},
    {"id": "BIN-104", "location": "Temple Road", "lat": 12.9705, "lon": 77.5960, "fill": random.randint(20, 100)},
]

df = pd.DataFrame(dustbins)

# --- COLOUR LOGIC ---
def get_color(fill):
    if fill >= 80:
        return [255, 0, 0]   # Red = Full
    elif fill >= 50:
        return [255, 165, 0] # Orange = Half
    else:
        return [0, 200, 0]   # Green = Low

df["color"] = df["fill"].apply(get_color)

# --- ROW 1: TABLE ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='sub'>📊 Dustbin Status</div>", unsafe_allow_html=True)
    st.dataframe(df[["id", "location", "fill"]])

# --- MAP VIEW ---
with col2:
    st.markdown("<div class='sub'>🗺️ Live Map View (Prototype)</div>", unsafe_allow_html=True)

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=12.9716,
            longitude=77.5946,
            zoom=14,
            pitch=45,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[lon, lat]',
                get_color="color",
                get_radius=40,
            )
        ],
    ))

# --- CLEANING SYSTEM ---
st.markdown("<div class='sub'>✔ Mark Dustbin as Cleaned</div>", unsafe_allow_html=True)

bin_ids = [d["id"] for d in dustbins]
selected_bin = st.selectbox("Select Dustbin:", bin_ids)

if st.button("Mark as Cleaned"):
    st.success(f"✔ {selected_bin} was marked as cleaned!")
    st.info("Fill level reset to 0% (Prototype only).")

st.write("---")
st.write("🌱 **Prototype version of BINOVA. Add IoT sensors later.**")

