import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from home import HomePage

DATA_DIR = "data"
SUBJECTS_FILE = os.path.join(DATA_DIR, "subjects.json")

class SubjectManagerPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.style = ttk.Style()
        
        # Configure custom styles
        self._configure_styles()
        
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Main container with padding
        self.container = ttk.Frame(self, style='Main.TFrame')
        self.container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        ttk.Label(self.container, 
                 text="Subject Manager", 
                 style='Header.TLabel').pack(pady=(0, 20))
        
        # Subject list frame with card styling
        self.list_frame = ttk.LabelFrame(self.container, 
                                       text="Subject List",
                                       style='Card.TLabelframe')
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Custom listbox with modern styling
        self.subject_listbox = tk.Listbox(
            self.list_frame,
            height=12,
            bg='white',
            fg='#333333',
            selectbackground='#3498db',
            selectforeground='white',
            font=('Arial', 10),
            borderwidth=1,
            relief='solid',
            highlightthickness=0
        )
        self.subject_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Custom scrollbar
        scrollbar = ttk.Scrollbar(
            self.list_frame, 
            orient="vertical", 
            command=self.subject_listbox.yview
        )
        scrollbar.pack(side="right", fill="y", pady=5)
        self.subject_listbox.config(yscrollcommand=scrollbar.set)
        
        # Entry frame with card styling
        self.entry_frame = ttk.LabelFrame(self.container,
                                        text="Add New Subject",
                                        style='Card.TLabelframe')
        self.entry_frame.pack(fill="x", padx=10, pady=10)
        
        # Subject entry with label
        ttk.Label(self.entry_frame, 
                 text="Subject Name:", 
                 style='Bold.TLabel').pack(side="left", padx=10, pady=5)
        
        self.subject_entry = ttk.Entry(
            self.entry_frame,
            style='Custom.TEntry'
        )
        self.subject_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        
        # Bind Enter key to add subject
        self.subject_entry.bind('<Return>', lambda event: self.add_subject())
        
        # Buttons frame with action buttons
        self.button_frame = ttk.Frame(self.container, style='Card.TFrame')
        self.button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Add subject button
        ttk.Button(
            self.button_frame,
            text="Add Subject", 
            command=self.add_subject,
            style='Success.TButton'
        ).pack(side="left", padx=10, pady=5, ipadx=15)
        
        # Delete subject button
        ttk.Button(
            self.button_frame,
            text="Delete Selected", 
            command=self.delete_subject,
            style='Danger.TButton'
        ).pack(side="left", padx=10, pady=5, ipadx=15)
        
        # Back button
        from home import HomePage  # Avoid circular import
        ttk.Button(
            self.container,
            text="← Back to Home", 
            command=lambda: controller.show_frame(HomePage),
            style='Secondary.TButton'
        ).pack(pady=(10, 0))
        
        self.load_subjects()
        
    def _configure_styles(self):
        """Configure custom styles for the subject manager"""
        # Main background
        self.style.configure('Main.TFrame', background='#f5f7fa')
        
        # Header style
        self.style.configure('Header.TLabel', 
                           font=('Arial', 18, 'bold'),
                           foreground='#2c3e50',
                           background='#f5f7fa')
        
        # Card styles (for frames and labelframes)
        self.style.configure('Card.TFrame', 
                           background='#ffffff',
                           borderwidth=0)
        self.style.configure('Card.TLabelframe', 
                           background='#ffffff',
                           foreground='#2c3e50',
                           font=('Arial', 10, 'bold'),
                           borderwidth=1,
                           relief='solid',
                           bordercolor='#e0e0e0')
        
        # Label styles
        self.style.configure('Bold.TLabel',
                           font=('Arial', 10, 'bold'),
                           foreground='#34495e',
                           background='#ffffff')
        
        # Entry style
        self.style.configure('Custom.TEntry',
                           font=('Arial', 10),
                           foreground='#2c3e50',
                           fieldbackground='#ffffff',
                           padding=5,
                           bordercolor='#bdc3c7',
                           lightcolor='#bdc3c7',
                           darkcolor='#bdc3c7')
        
        # Button styles
        self.style.configure('Primary.TButton',
                           foreground='white',
                           background='#3498db',
                           font=('Arial', 10, 'bold'),
                           borderwidth=0,
                           padding=(10, 5))
        
        self.style.configure('Secondary.TButton',
                           foreground='#2c3e50',
                           background='#ecf0f1',
                           font=('Arial', 10, 'bold'),
                           borderwidth=0,
                           padding=(10, 5))
        
        self.style.configure('Success.TButton',
                           foreground='white',
                           background='#2ecc71',
                           font=('Arial', 10, 'bold'),
                           borderwidth=0,
                           padding=(10, 5))
        
        self.style.configure('Danger.TButton',
                           foreground='white',
                           background='#e74c3c',
                           font=('Arial', 10, 'bold'),
                           borderwidth=0,
                           padding=(10, 5))
        
        # Button hover effects
        button_styles = {
            'Primary': '#3498db',
            'Secondary': '#ecf0f1',
            'Success': '#2ecc71',
            'Danger': '#e74c3c'
        }
        
        for style, base_color in button_styles.items():
            self.style.map(f'{style}.TButton',
                          foreground=[('active', 'white'), ('pressed', 'white')],
                          background=[('active', self._darken_color(base_color)), 
                                    ('pressed', self._darken_color(base_color, 0.2))])
    
    def _darken_color(self, hex_color, factor=0.1):
        """Darken a hex color by a given factor"""
        if isinstance(hex_color, str) and hex_color.startswith('#'):
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f'#{int(rgb[0]*(1-factor)):02x}{int(rgb[1]*(1-factor)):02x}{int(rgb[2]*(1-factor)):02x}'
        return hex_color
        
    def load_subjects(self):
        try:
            with open(SUBJECTS_FILE, "r") as f:
                self.subjects = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.subjects = []
            
        self.update_listbox()
        
    def update_listbox(self):
        self.subject_listbox.delete(0, tk.END)
        for subject in sorted(self.subjects):
            self.subject_listbox.insert(tk.END, subject)
            
    def add_subject(self):
        subject_name = self.subject_entry.get().strip()
        if not subject_name:
            messagebox.showwarning("Warning", "Subject name cannot be empty.")
            return
            
        if subject_name in self.subjects:
            messagebox.showwarning("Warning", "Subject already exists.")
            return
            
        self.subjects.append(subject_name)
        self.save_subjects()
        self.update_listbox()
        self.subject_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Subject '{subject_name}' added successfully")
        
    def delete_subject(self):
        selected = self.subject_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a subject to delete.")
            return
            
        idx = selected[0]
        subject_name = self.subjects[idx]
        
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete '{subject_name}'?",
            icon='warning'
        )
        if confirm:
            self.subjects.pop(idx)
            self.save_subjects()
            self.update_listbox()
            messagebox.showinfo("Success", f"Subject '{subject_name}' deleted successfully")
            
    def save_subjects(self):
        try:
            with open(SUBJECTS_FILE, "w") as f:
                json.dump(self.subjects, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save subjects: {str(e)}")