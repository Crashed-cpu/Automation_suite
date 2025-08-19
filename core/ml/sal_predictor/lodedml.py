import joblib
import streamlit as st
import math
from babel.numbers import format_currency

model = joblib.load("salary_predictor.pkl")
st.title("Salary predictor by Years of Experience")

years = st.number_input("Enter years of experience: ", min_value = 0, max_value = 50)

if st.button("Predict Result"):
    salary = model.predict([[years]])
    salary = math.ceil(salary)
    salary = format_currency(salary, 'INR', locale='en_IN')
    st.success(f"Congrats, Your salary is {salary}")
    