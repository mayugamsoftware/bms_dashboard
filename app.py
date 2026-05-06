import streamlit as st
import pandas as pd
import numpy as np
import requests
import joblib
import os
from datetime import datetime
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="⚡ Smart EV BMS Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.block-container {
    padding: 1rem 2rem;
}
.metric-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    border: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 15px;
}
.metric-title {
    font-size: 16px;
    color: #cbd5e1;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}
.good {color:#22c55e; font-weight:bold;}
.warning {color:#f59e0b; font-weight:bold;}
.critical {color:#ef4444; font-weight:bold;}
.stButton>button {
    width: 100%;
    height: 50px;
    border-radius: 14px;
    border: none;
    font-size: 18px;
    font-weight: 600;
    background: linear-gradient(90deg,#06b6d4,#3b82f6);
    color: white;
}
section[data-testid="stSidebar"] {
    background: #020617;
}
.footer {
    text-align:center;
    color:#94a3b8;
    padding:20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================
def login():
    st.markdown("<h1 style='text-align:center;'>🔐 Smart EV BMS Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if user == "admin" and pwd == "admin123":
                st.session_state["login"] = True
            else:
                st.error("Invalid Credentials")

if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    login()
    st.stop()

# =========================
# LOAD MODELS
# =========================
scaler = joblib.load("scaler.pkl")
le = joblib.load("label_encoder.pkl")
clf = joblib.load("condition_classifier.pkl")

# =========================
# LOAD VEHICLE DATABASE
# =========================
vehicle_db = pd.read_csv("vehicle_database.csv")

# =========================
# BLYNK CONFIG
# =========================
TOKEN = "n3gExjNgqmV6yX9O5-Jcc-j048SHxISm"
BASE = "https://blynk.cloud/external/api"

URLS = {
    "v1": f"{BASE}/get?token={TOKEN}&V0",
    "v2": f"{BASE}/get?token={TOKEN}&V1",
    "temp": f"{BASE}/get?token={TOKEN}&V2",
    "uslot": f"{BASE}/get?token={TOKEN}&V3",
    "current": f"{BASE}/get?token={TOKEN}&V6"
}

# =========================
# FETCH SENSOR DATA
# =========================
def fetch_data():
    data = {}
    for key, url in URLS.items():
        try:
            res = requests.get(url, timeout=5)
            data[key] = float(res.text.strip())
        except:
            data[key] = 0
    return data

# =========================
# HISTORY CSV
# =========================
file = "history.csv"

if not os.path.exists(file):
    pd.DataFrame(columns=[
        "time", "number_plate", "v1", "v2",
        "temp", "uslot", "current", "BMS"
    ]).to_csv(file, index=False)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙ Navigation")
menu = st.sidebar.radio("Go to", ["Dashboard", "History", "Analytics"])

st.title("⚡ Smart EV Battery Management System")

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.subheader("🚗 EV Vehicle Search")

    plate = st.text_input("Enter Vehicle Number Plate", placeholder="TN37AB1234").upper()
    search = st.button("📡 Fetch Vehicle & Predict")

    if search:

        if plate == "":
            st.warning("Please enter vehicle number")
            st.stop()

        vehicle = vehicle_db[vehicle_db["number_plate"].str.upper() == plate]

        if vehicle.empty:
            st.error("❌ Vehicle not found")
            st.stop()

        vehicle_data = vehicle.iloc[0]

        st.success("✅ Vehicle Found")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>🚘 Vehicle Details</h3>
                <p><b>Owner:</b> {vehicle_data['owner']}</p>
                <p><b>Model:</b> {vehicle_data['model']}</p>
                <p><b>Manufacturer:</b> {vehicle_data['manufacturer']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>🔋 Battery Details</h3>
                <p><b>Capacity:</b> {vehicle_data['battery_capacity']}</p>
                <p><b>Type:</b> {vehicle_data['vehicle_type']}</p>
                <p><b>Reg Date:</b> {vehicle_data['reg_date']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Fetch sensor data
        sensor = fetch_data()

        X = np.array([[
            sensor["v1"],
            sensor["v2"],
            sensor["temp"],
            sensor["uslot"],
            sensor["current"]
        ]])

        X_scaled = scaler.transform(X)

        bms = le.inverse_transform(clf.predict(X_scaled))[0]

        cols = st.columns(5)

        metrics = {
            "Voltage 1": sensor["v1"],
            "Voltage 2": sensor["v2"],
            "Temperature": sensor["temp"],
            "USlot": sensor["uslot"],
            "Current": sensor["current"]
        }

        for col, (label, value) in zip(cols, metrics.items()):
            col.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>{label}</div>
                <div class='metric-value'>{value:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        status = "good"
        if bms == "Warning":
            status = "warning"
        elif bms == "Critical":
            status = "critical"

        st.markdown(f"""
        <div class='metric-card'>
            <h2>🔋 Battery Status:
                <span class='{status}'>{bms}</span>
            </h2>
        </div>
        """, unsafe_allow_html=True)

        # Save history
        new_row = pd.DataFrame([{
            "time": datetime.now(),
            "number_plate": plate,
            "v1": sensor["v1"],
            "v2": sensor["v2"],
            "temp": sensor["temp"],
            "uslot": sensor["uslot"],
            "current": sensor["current"],
            "BMS": bms
        }])

        new_row.to_csv(file, mode="a", header=False, index=False)

# =========================
# HISTORY
# =========================
if menu == "History":
    st.subheader("📊 Prediction History")

    df = pd.read_csv(file)
    st.dataframe(df, use_container_width=True)

    st.download_button("⬇ Download CSV", df.to_csv(index=False), "history.csv")

# =========================
# ANALYTICS
# =========================
if menu == "Analytics":
    st.subheader("📈 Analytics Dashboard")

    df = pd.read_csv(file)

    if df.empty:
        st.warning("No data available")
    else:
        fig1 = px.histogram(df, x="BMS", title="Battery Status Count")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.scatter(
            df,
            x="temp",
            y="current",
            color="BMS",
            title="Temperature vs Current"
        )
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.histogram(
            df,
            x="number_plate",
            color="BMS",
            title="Vehicle Status Distribution"
        )
        st.plotly_chart(fig3, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown(
    "<div class='footer'>⚡ Smart EV BMS Dashboard | AI Powered EV Monitoring</div>",
    unsafe_allow_html=True
)