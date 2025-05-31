import tkinter as tk
from teacher_manager import TeacherManagerPage
from timetable_generator import TimetableGeneratorPage
from subject_manager import SubjectManagerPage  # Import the new SubjectManagerPage

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Main title
        tk.Label(self, text="School Management System", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self, text="Home Page", font=("Arial", 14)).pack(pady=10)

        # Button container frame for better layout
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Buttons with consistent styling
        button_style = {
            'font': ('Arial', 12),
            'width': 20,
            'pady': 8
        }

        # Manage Teachers button
        tk.Button(button_frame, text="Manage Teachers",
                 command=lambda: controller.show_frame(TeacherManagerPage),
                 **button_style).pack(pady=10, fill=tk.X)

        # New Manage Subjects button
        tk.Button(button_frame, text="Manage Subjects",
                 command=lambda: controller.show_frame(SubjectManagerPage),
                 **button_style).pack(pady=10, fill=tk.X)

        # Generate Timetable button
        tk.Button(button_frame, text="Generate Timetable",
                 command=lambda: controller.show_frame(TimetableGeneratorPage),
                 **button_style).pack(pady=10, fill=tk.X)

        # Footer
        tk.Label(self, text="© School Management System", font=("Arial", 10)).pack(side=tk.BOTTOM, pady=10)