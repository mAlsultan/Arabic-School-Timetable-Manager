import tkinter as tk
from tkinter import ttk
import os
import sys
from pathlib import Path

def get_data_dir():
    """Returns the correct data directory for all environments"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = Path(os.getenv('APPDATA')) / "TimetableGenerator"
    else:
        # Running in development
        base_path = Path(__file__).parent / "data"
    
    base_path.mkdir(exist_ok=True, parents=True)
    return str(base_path)
# Add resource path function for PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

from login import LoginPage
from home import HomePage
from teacher_manager import TeacherManagerPage
from timetable_generator import TimetableGeneratorPage
from subject_manager import SubjectManagerPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure data directory
        self.DATA_DIR = resource_path("data")
        os.makedirs(self.DATA_DIR, exist_ok=True)
        
        # Configure main window
        self.title("School Timetable Generator")
        self.geometry("1280x720")
        self.minsize(1280, 720)
        # Optionally set maxsize if you want to prevent maximizing
        # self.maxsize(1280, 720)
        
        # Configure ttk style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Modern theme
        
        # Custom styling
        self._configure_styles()
        
        # Create main container with scrollbars
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill="both", expand=True)
        
        # Create canvas for scrolling
        self.canvas = tk.Canvas(self.main_container, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Add vertical scrollbar
        self.v_scroll = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.v_scroll.pack(side="right", fill="y")
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create scrollable frame inside canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure the scrollable frame to resize with canvas
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Bind mousewheel to scroll
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Initialize pages
        self.frames = {}
        for F in (LoginPage, HomePage, TeacherManagerPage, 
                 TimetableGeneratorPage, SubjectManagerPage):
            frame = F(self.scrollable_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure column/row weights so frames expand properly
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        
        self.show_frame(LoginPage)
    
    def _on_mousewheel(self, event):
        """Handle vertical scrolling with mouse wheel"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _configure_styles(self):
        """Configure consistent styling for all widgets"""
        self.style.configure('.', font=('Arial', 10))
        
        # Frame styles
        self.style.configure('TFrame', background="#f0f0f0")
        self.style.configure('Header.TFrame', background="#3a7ff6")
        
        # Label styles
        self.style.configure('TLabel', background="#f0f0f0", foreground="#333333")
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'), 
                           foreground="white", background="#3a7ff6")
        
        # Button styles
        self.style.configure('TButton', padding=6)
        self.style.configure('Primary.TButton', foreground="white", 
                           background="#3a7ff6", font=('Arial', 10, 'bold'))
        
        # Entry styles
        self.style.configure('TEntry', padding=5)
        
        # Notebook styles
        self.style.configure('TNotebook', background="#f0f0f0")
        self.style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), 
                           padding=[10, 5])
        
        # Treeview styles
        self.style.configure('Treeview', rowheight=35, font=('Arial', 9))
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
        # Button states
        self.style.map('TButton',
                      foreground=[('pressed', 'black'), ('active', 'blue')],
                      background=[('pressed', '!disabled', '#c0c0c0'), 
                                ('active', '#e0e0e0')])
        
        self.style.map('Primary.TButton',
                      background=[('pressed', '!disabled', '#2a6fd6'), 
                                 ('active', '#4a8ff6')])
    
    def show_frame(self, page_class):
        """Show a frame for the given page class"""
        frame = self.frames[page_class]
        frame.tkraise()
        
        # Reset the scroll position when changing pages
        self.canvas.yview_moveto(0)
        
        # Update window title based on current page
        if page_class == LoginPage:
            self.title("School Timetable - Login")
        elif page_class == HomePage:
            self.title("School Timetable - Dashboard")
        elif page_class == TeacherManagerPage:
            self.title("School Timetable - Teacher Management")
        elif page_class == TimetableGeneratorPage:
            self.title("School Timetable - Generator")
        elif page_class == SubjectManagerPage:
            self.title("School Timetable - Subject Management")

if __name__ == "__main__":
    app = App()
    app.mainloop()