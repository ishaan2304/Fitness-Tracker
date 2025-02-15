import tkinter as tk
from tkinter import messagebox, filedialog

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

    def load_data(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                date, exercise_type, duration, calories_burned = line.strip().split(',')
                workout = Workout(date, exercise_type, int(duration), int(calories_burned))
                self.workouts.append(workout)

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Tracker")

        self.user = None

        font = ("Helvetica", 14)

        self.name_label = tk.Label(root, text="Name:", font=font)
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(root, font=font)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.age_label = tk.Label(root, text="Age:", font=font)
        self.age_label.grid(row=1, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(root, font=font)
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        self.weight_label = tk.Label(root, text="Weight:", font=font)
        self.weight_label.grid(row=2, column=0, padx=10, pady=5)
        self.weight_entry = tk.Entry(root, font=font)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=5)

        self.create_user_button = tk.Button(root, text="Create User", command=self.create_user, bg="lightblue", font=font)
        self.create_user_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD):", font=font)
        self.date_label.grid(row=4, column=0, padx=10, pady=5)
        self.date_entry = tk.Entry(root, font=font)
        self.date_entry.grid(row=4, column=1, padx=10, pady=5)

        self.exercise_type_label = tk.Label(root, text="Exercise Type:", font=font)
        self.exercise_type_label.grid(row=5, column=0, padx=10, pady=5)
        self.exercise_type_entry = tk.Entry(root, font=font)
        self.exercise_type_entry.grid(row=5, column=1, padx=10, pady=5)

        self.duration_label = tk.Label(root, text="Duration (minutes):", font=font)
        self.duration_label.grid(row=6, column=0, padx=10, pady=5)
        self.duration_entry = tk.Entry(root, font=font)
        self.duration_entry.grid(row=6, column=1, padx=10, pady=5)

        self.calories_burned_label = tk.Label(root, text="Calories Burned:", font=font)
        self.calories_burned_label.grid(row=7, column=0, padx=10, pady=5)
        self.calories_burned_entry = tk.Entry(root, font=font)
        self.calories_burned_entry.grid(row=7, column=1, padx=10, pady=5)

        self.add_workout_button = tk.Button(root, text="Add Workout", command=self.add_workout, bg="lightgreen", font=font)
        self.add_workout_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        self.view_workouts_button = tk.Button(root, text="View Workouts", command=self.view_workouts, bg="lightyellow", font=font)
        self.view_workouts_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.save_data_button = tk.Button(root, text="Save Data", command=self.save_data, bg="lightcoral", font=font)
        self.save_data_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        self.load_data_button = tk.Button(root, text="Load Data", command=self.load_data, bg="lightpink", font=font)
        self.load_data_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    def create_user(self):
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        weight = float(self.weight_entry.get())
        self.user = User(name, age, weight)
        messagebox.showinfo("Success", "User created successfully!")

    def add_workout(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        date = self.date_entry.get()
        exercise_type = self.exercise_type_entry.get()
        duration = int(self.duration_entry.get())
        calories_burned = int(self.calories_burned_entry.get())
        workout = Workout(date, exercise_type, duration, calories_burned)
        self.user.add_workout(workout)
        messagebox.showinfo("Success", "Workout added successfully!")

    def view_workouts(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        workouts = self.user.view_workouts()
        messagebox.showinfo("Workouts", workouts)

    def save_data(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            self.user.save_data(filename)
            messagebox.showinfo("Success", "Data saved successfully!")

    def load_data(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.user.load_data(filename)
            messagebox.showinfo("Success", "Data loaded successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()