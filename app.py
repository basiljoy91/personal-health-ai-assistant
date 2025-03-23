import streamlit as st
import pandas as pd
import numpy as np

# Load the synthetic dataset
@st.cache_data  # Cache the data for better performance
def load_data():
    return pd.read_csv('healthy_people.csv')

# Title
st.title("AI Personalized Health Tracker 🏃‍♂️💪")

# Sidebar for user input
st.sidebar.header("Enter Your Details")
age = st.sidebar.number_input("Age", min_value=1, max_value=100, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)

# Calculate BMI
def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

bmi = calculate_bmi(weight, height)
st.sidebar.write(f"**Your BMI:** {bmi:.2f}")

# Main input for daily metrics
st.header("Daily Metrics 📊")
col1, col2 = st.columns(2)

with col1:
    steps = st.number_input("Daily Steps", min_value=0, value=5000)
    sleep = st.number_input("Sleep Duration (hours)", min_value=0, max_value=24, value=7)

with col2:
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=70)
    body_temp = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, value=36.5)

# Activity-based calorie burn
st.header("Activity-Based Calorie Burn 🔥")
activity = st.selectbox("Select Activity", ["Walking", "Running", "Swimming"])
activity_duration = st.number_input("Duration (minutes)", min_value=0, value=30)

def activity_calories(activity, duration, weight):
    # Calories burned per minute per kg of body weight
    if activity == "Walking":
        return duration * 0.035 * weight
    elif activity == "Running":
        return duration * 0.07 * weight
    elif activity == "Swimming":
        return duration * 0.06 * weight

activity_calories_burned = activity_calories(activity, activity_duration, weight)
st.write(f"**Calories Burned from {activity}:** {activity_calories_burned:.2f} kcal")

# Display similar healthy people
st.header("Comparison with Healthy People 👥")
healthy_data = load_data()

# Filter similar people based on age, gender, and BMI
similar_people = healthy_data[
    (healthy_data['Age'].between(age - 5, age + 5)) &  # Age within ±5 years
    (healthy_data['Gender'] == gender) &               # Same gender
    (healthy_data['BMI'].between(bmi - 2, bmi + 2))    # BMI within ±2
]

if not similar_people.empty:
    st.write("Here are 4 healthy people with similar profiles:")
    st.dataframe(similar_people.head(4))  # Show only the first 4 rows
else:
    st.write("No similar healthy people found in the dataset.")

# Health Recommendations
st.header("Health Recommendations 🩺")
if bmi < 18.5:
    st.warning("You are underweight. Consider increasing your calorie intake.")
elif 18.5 <= bmi < 24.9:
    st.success("Your weight is normal. Keep up the good work!")
else:
    st.error("You are overweight. Consider exercising more and eating healthier.")

# Tips Section
st.header("Tips for a Healthier Lifestyle 🌱")
if bmi < 18.5:
    st.write("💡 **Tips for Underweight Individuals:**")
    st.write("- Eat calorie-dense foods like nuts, avocados, and whole grains.")
    st.write("- Incorporate strength training to build muscle mass.")
    st.write("- Consider consulting a nutritionist for a personalized diet plan.")
elif 18.5 <= bmi < 24.9:
    st.write("💡 **Tips for Maintaining a Healthy Weight:**")
    st.write("- Maintain a balanced diet with fruits, vegetables, and lean proteins.")
    st.write("- Stay active with regular exercise (e.g., walking, jogging, yoga).")
    st.write("- Monitor your weight and health metrics regularly.")
else:
    st.write("💡 **Tips for Overweight Individuals:**")
    st.write("- Reduce calorie intake by avoiding sugary and processed foods.")
    st.write("- Engage in at least 30 minutes of moderate exercise daily.")
    st.write("- Consider tracking your food intake and physical activity.")

# Footer
st.write("---")
st.write("**Disclaimer:** This app provides general health recommendations and is not a substitute for professional medical advice. Always consult a healthcare provider for personalized guidance.")

# Add a fun progress bar for daily steps
st.header("Daily Steps Progress 🚶‍♀️")
step_goal = 10000  # Daily step goal
step_progress = steps / step_goal
st.progress(step_progress)
st.write(f"You've completed {steps} out of {step_goal} steps today ({step_progress * 100:.1f}%).")

# Add a fun fact about health
st.header("Did You Know? 🤔")
st.write("Regular physical activity can reduce the risk of chronic diseases like heart disease, diabetes, and obesity. Even a 30-minute walk daily can make a big difference!")

# Add a button to refresh the app
if st.button("Refresh App 🔄"):
    st.experimental_rerun()