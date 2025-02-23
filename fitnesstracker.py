import streamlit as st
import pandas as pd
from io import StringIO
import streamlit.components.v1 as components

# CSS for background animation
background_animation = """
<style>
body {
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}
@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
</style>
"""

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date} - {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"

class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        return "\n".join(str(workout) for workout in self.workouts)

    def save_data(self, filename):
        with open(filename, 'w') as file:
            for workout in self.workouts:
                file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")

    def load_data(self, file):
        if isinstance(file, str):
            file = open(file, 'r')
        for line in file:
            date, exercise_type, duration, calories_burned = line.strip().split(',')
            workout = Workout(date, exercise_type, int(duration), int(calories_burned))
            self.workouts.append(workout)
        if not isinstance(file, StringIO):
            file.close()

def main():
    st.title("Fitness Tracker")

    # Embed the CSS for background animation
    components.html(background_animation, height=0)

    if 'user' not in st.session_state:
        st.session_state.user = None

    with st.sidebar:
        st.header("Create User")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
        if st.button("Create User"):
            st.session_state.user = User(name, age, weight)
            st.success("User created successfully!")

    if st.session_state.user:
        st.header(f"Welcome, {st.session_state.user.name}!")

        st.subheader("Add Workout")
        date = st.date_input("Date")
        exercise_type = st.text_input("Exercise Type")
        duration = st.number_input("Duration (minutes)", min_value=0, step=1)
        calories_burned = st.number_input("Calories Burned", min_value=0, step=1)
        if st.button("Add Workout"):
            workout = Workout(date, exercise_type, duration, calories_burned)
            st.session_state.user.add_workout(workout)
            st.success("Workout added successfully!")

        st.subheader("View Workouts")
        if st.button("Show Workouts"):
            workouts = st.session_state.user.view_workouts()
            st.text(workouts)

        st.subheader("Save Data")
        filename = st.text_input("Filename to save data", value="workouts.txt")
        if st.button("Save Data"):
            st.session_state.user.save_data(filename)
            st.success("Data saved successfully!")

        st.subheader("Load Data")
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            st.session_state.user.load_data(stringio)
            st.success("Data loaded successfully!")

if __name__ == "__main__":
    main()
