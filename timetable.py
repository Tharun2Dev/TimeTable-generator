import tkinter as tk
from tkinter import ttk, messagebox
import random
import pandas as pd

# Constants
CLASSES = [f"Class {i}" for i in range(1, 11)]
SUBJECTS = ["Math", "Science", "English", "History", "Social", "Computer", "PT"]
PERIODS_PER_DAY = 7
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TEACHERS = [f"Teacher {i}" for i in range(1, 21)]

# Core Logic
class TimetableGenerator:
    def __init__(self):
        self.timetable = {cls: {day: [""] * PERIODS_PER_DAY for day in DAYS} for cls in CLASSES}
        self.subject_teacher_map = self.assign_teachers_to_subjects()

    def assign_teachers_to_subjects(self):
        """
        Assigns each subject to a random teacher.
        Ensures no teacher is overburdened.
        """
        random.shuffle(TEACHERS)
        subject_teacher_map = {}
        for i, subject in enumerate(SUBJECTS):
            subject_teacher_map[subject] = TEACHERS[i % len(TEACHERS)]
        return subject_teacher_map

    def generate_timetable(self):
        """
        Generates a timetable for each class ensuring no teacher overlaps.
        """
        for cls in CLASSES:
            for day in DAYS:
                subjects_for_day = random.sample(SUBJECTS, PERIODS_PER_DAY)
                for period, subject in enumerate(subjects_for_day):
                    teacher = self.subject_teacher_map[subject]
                    self.timetable[cls][day][period] = f"{subject} ({teacher})"

    def get_timetable_for_class(self, cls):
        """
        Returns the timetable for a specific class.
        """
        return self.timetable[cls]

# GUI Implementation
class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic Timetable Generator")
        self.root.geometry("800x600")

        # Initialize Timetable Generator
        self.generator = TimetableGenerator()
        self.generator.generate_timetable()

        # UI Components
        self.setup_ui()

    def setup_ui(self):
        # Dropdown to select class
        self.class_label = tk.Label(self.root, text="Select Class:", font=("Arial", 14))
        self.class_label.pack(pady=10)

        self.class_var = tk.StringVar(value=CLASSES[0])
        self.class_dropdown = ttk.Combobox(self.root, textvariable=self.class_var, values=CLASSES, font=("Arial", 12), state="readonly")
        self.class_dropdown.pack(pady=10)

        # Button to generate timetable
        self.generate_button = tk.Button(self.root, text="Show Timetable", command=self.display_timetable, font=("Arial", 14))
        self.generate_button.pack(pady=20)

        # Treeview to display timetable
        self.timetable_tree = ttk.Treeview(self.root, columns=DAYS, show="headings", height=10)
        self.timetable_tree.pack(pady=10, fill="both", expand=True)

        for day in DAYS:
            self.timetable_tree.heading(day, text=day)
            self.timetable_tree.column(day, width=100, anchor="center")

    def display_timetable(self):
        # Clear existing data
        for row in self.timetable_tree.get_children():
            self.timetable_tree.delete(row)

        # Get selected class
        selected_class = self.class_var.get()

        # Get timetable for the class
        timetable = self.generator.get_timetable_for_class(selected_class)

        # Display timetable
        for period in range(PERIODS_PER_DAY):
            row_data = [timetable[day][period] for day in DAYS]
            self.timetable_tree.insert("", "end", values=row_data)

        messagebox.showinfo("Success", f"Timetable for {selected_class} displayed!")
        
        #export time table to excel
def export_to_excel(self, cls):
    timetable = self.generator.get_timetable_for_class(cls)
    df = pd.DataFrame(timetable)
    filename = f"{cls}_Timetable.xlsx"
    df.to_excel(filename, index_label="Period")
    messagebox.showinfo("Export Success", f"Timetable saved as {filename}!")


# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
