# ⚡ Smart EV Battery Management System (BMS) Dashboard

An AI-powered **Electric Vehicle Battery Monitoring System** built with **Streamlit**, integrated with **Blynk IoT Cloud** for real-time sensor data visualization and battery health prediction.

---

## 🚀 Features

* 🔐 Secure Login System
* 🚗 Vehicle Search using Number Plate
* 🔋 Real-time Battery Monitoring (Voltage, Temperature, Current, etc.)
* 🤖 AI-based Battery Condition Prediction (Good / Warning / Critical)
* 📊 Interactive Analytics Dashboard (Plotly)
* 📁 Data Logging & History Download
* 🌐 Blynk Cloud Integration (Live IoT Data)
* 📱 Responsive UI (Mobile + Desktop)

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Backend:** Python
* **Machine Learning:** Scikit-learn
* **Visualization:** Plotly
* **IoT Platform:** Blynk Cloud
* **Data Handling:** Pandas, NumPy

---

## 📂 Project Structure

```
📁 Smart-EV-BMS/
│
├── app.py                      # Main Streamlit App
├── scaler.pkl                 # Feature Scaler
├── label_encoder.pkl          # Label Encoder
├── condition_classifier.pkl   # ML Model (Battery Condition)
├── vehicle_database.csv       # Vehicle Records
├── history.csv                # Auto-generated Logs
├── requirements.txt           # Dependencies
└── README.md                  # Project Documentation
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/smart-ev-bms.git
cd smart-ev-bms
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 🔑 Login Credentials

```
Username: admin
Password: admin123
```

---

## 🔗 Blynk Configuration

Update your Blynk Token in `app.py`:

```python
TOKEN = "YOUR_BLYNK_TOKEN"
```

### 📡 Virtual Pins Used

| Sensor      | Blynk Pin |
| ----------- | --------- |
| Voltage 1   | V0        |
| Voltage 2   | V1        |
| Temperature | V2        |
| USlot       | V3        |
| Current     | V6        |

---

## 📊 Analytics Included

* Battery Status Distribution
* Temperature vs Current Analysis
* Vehicle-wise Status Overview

---

## 📁 Data Storage

* All predictions are stored in:

  ```
  history.csv
  ```
* Download available from dashboard

---

## 🌐 Deployment (Free)

### 🔹 Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click **New App**
4. Select your repo
5. Deploy 🚀

---

## ⚠️ Notes

* Ensure `.pkl` model files are in the root directory
* Internet required for Blynk API
* If sensors fail → default value = 0

---

## 🔮 Future Enhancements

* 🔴 Real-time auto refresh
* 🌍 GPS Tracking (Map Integration)
* 🚨 Alert System (SMS / Notification)
* 📱 Mobile App Integration
* 🔋 Battery Charging Optimization

---

## 👨‍💻 Author

**LA Tech Team**

---

## 📜 License

This project is for educational and research purposes.

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
