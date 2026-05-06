import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="EV Vehicle Database Entry",
    layout="centered"
)

st.title("🚗 EV Vehicle Database Entry Form")

file = "vehicle_database.csv"

# Create file if not exists
if not os.path.exists(file):
    df = pd.DataFrame(columns=[
        "number_plate",
        "owner",
        "model",
        "manufacturer",
        "battery_capacity",
        "vehicle_type",
        "reg_date"
    ])
    df.to_csv(file, index=False)

# Form
with st.form("vehicle_form"):
    number_plate = st.text_input("Vehicle Number Plate").upper()
    owner = st.text_input("Owner Name")
    model = st.text_input("Vehicle Model")
    manufacturer = st.text_input("Manufacturer")
    battery_capacity = st.text_input("Battery Capacity (Example: 40 kWh)")
    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["SUV", "Sedan", "Scooter", "Bike", "Truck", "Bus"]
    )
    reg_date = st.date_input("Registration Date")

    submit = st.form_submit_button("➕ Add Vehicle")

if submit:
    if number_plate == "" or owner == "":
        st.error("Please fill required fields")
    else:
        df = pd.read_csv(file)

        # Check duplicate
        if number_plate in df["number_plate"].astype(str).str.upper().values:
            st.warning("Vehicle already exists in database")
        else:
            new_data = pd.DataFrame([{
                "number_plate": number_plate,
                "owner": owner,
                "model": model,
                "manufacturer": manufacturer,
                "battery_capacity": battery_capacity,
                "vehicle_type": vehicle_type,
                "reg_date": reg_date
            }])

            new_data.to_csv(
                file,
                mode="a",
                header=False,
                index=False
            )

            st.success("✅ Vehicle Added Successfully")

# Show database
st.subheader("📋 Current Vehicle Database")
df = pd.read_csv(file)
st.dataframe(df, use_container_width=True)