import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.title("Weight Loss Estimator from Fitness plan")

# Model

data = pd.read_csv("fitness.csv")

x = data [[
    "initial_weight", 
    "exercise_minutes", 
    "calories", 
    "water", 
    "sleep_hours", 
    "cheat_days"
    ]]

y = data ["weight_loss"]

brain = LinearRegression()
brain.fit(x, y)



# Input from streamlit
st.write("Enter the following details for prediction: ")
initial_weight = st.number_input("Current Weight (kg)")
goal_weight = st.number_input("Goal Weight (kg)")
exercise_minutes = st.number_input("Daily Exercise Minutes")
calories = st.number_input("Daily Calorie Intake")
water = st.number_input("Water Intake (litres/day)")
sleep_hours = st.number_input("Sleep Hours (per day)")
cheat_days = st.number_input("Cheat Days in 30 Days") 



# Get input data
input_data = [[initial_weight, exercise_minutes, calories, water, sleep_hours, cheat_days]]

if st.button("Predict Weight Loss"):
    predicted_weight_loss = brain.predict(input_data)

    st.success(f"Estimated Weight Loss after 30 days: **{predicted_weight_loss[0]:.2f} kg**")
    
    if goal_weight > 0 and predicted_weight_loss > 0:
        total_loss_needed = initial_weight - goal_weight
        if total_loss_needed > 0:
            months_needed = total_loss_needed / predicted_weight_loss
            st.info(f"Estimated time to reach your goal weight: **{months_needed[0]:.1f} months**")
