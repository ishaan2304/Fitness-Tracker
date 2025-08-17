import streamlit as st
import pandas as pd
from io import StringIO
import streamlit.components.v1 as components
page_animation = """
<style>
/* Background Animation */
body {
    background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1);
    background-size: 400% 400%;
    animation: gradient 10s ease infinite;
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}
@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Header Animation */
h1 {
    font-size: 3rem;
    color: #ffffff;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    animation: fadeIn 2s ease-in-out;
}
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Button Styling */
.stButton>button {
    background-color: #6a11cb;
    background-image: linear-gradient(315deg, #6a11cb 0%, #2575fc 74%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.1);
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.4);
}

/* Section Animation */
.section {
    animation: slideIn 1.5s ease-in-out;
}
@keyframes slideIn {
    0% { opacity: 0; transform: translateX(-50px); }
    100% { opacity: 1; transform: translateX(0); }
}

/* Sidebar Styling */
.sidebar .sidebar-content {
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
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

    def save_data(self):
        # Convert workouts to a DataFrame for easier export
        data = {
            "Date": [workout.date for workout in self.workouts],
            "Exercise Type": [workout.exercise_type for workout in self.workouts],
            "Duration (minutes)": [workout.duration for workout in self.workouts],
            "Calories Burned": [workout.calories_burned for workout in self.workouts],
        }
        df = pd.DataFrame(data)
        # Convert DataFrame to CSV
        return df.to_csv(index=False)

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
    # Embed the CSS for animations and styling
    components.html(page_animation, height=0)

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1>🏋️‍♂️ Fitness Tracker</h1>
            <p style="font-size: 18px; color: #ffffff; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);">
                Track your workouts, save your progress, and stay motivated! 💪
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if 'user' not in st.session_state:
        st.session_state.user = None

    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center;">
                <h2>👤 Create User</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
        if st.button("Create User"):
            st.session_state.user = User(name, age, weight)
            st.success("User created successfully!")

    if st.session_state.user:
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 20px;" class="section">
                <h2>Welcome, {st.session_state.user.name}! 🎉</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("➕ Add Workout")
        date = st.date_input("Date")
        exercise_type = st.text_input("Exercise Type")
        duration = st.number_input("Duration (minutes)", min_value=0, step=1)
        calories_burned = st.number_input("Calories Burned", min_value=0, step=1)
        if st.button("Add Workout"):
            workout = Workout(date, exercise_type, duration, calories_burned)
            st.session_state.user.add_workout(workout)
            st.success("Workout added successfully!")

        st.subheader("📋 View Workouts")
        if st.button("Show Workouts"):
            if st.session_state.user.workouts:
                # Convert workouts to a DataFrame for better display
                data = {
                    "Date": [workout.date for workout in st.session_state.user.workouts],
                    "Exercise Type": [workout.exercise_type for workout in st.session_state.user.workouts],
                    "Duration (minutes)": [workout.duration for workout in st.session_state.user.workouts],
                    "Calories Burned": [workout.calories_burned for workout in st.session_state.user.workouts],
                }
                df = pd.DataFrame(data)
                st.markdown(
                    """
                    <div style="text-align: center; margin-top: 20px;" class="section">
                        <h3>Your Workouts</h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.table(df)  # Display the workouts as a table
            else:
                st.warning("No workouts to display. Please add some workouts first.")

        st.subheader("💾 Save Data")
        if st.session_state.user.workouts:
            csv_data = st.session_state.user.save_data()
            st.download_button(
                label="Download Workouts",
                data=csv_data,
                file_name="workouts.csv",
                mime="text/csv",
            )
        else:
            st.warning("No workouts to save. Please add some workouts first.")

        st.subheader("📂 Load Data")
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            st.session_state.user.load_data(stringio)
            st.success("Data loaded successfully!")

if __name__ == "__main__":
    main()


