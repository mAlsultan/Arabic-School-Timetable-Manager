import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from home import HomePage    

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.style = ttk.Style()
        
        # Configure styles
        self._configure_styles()
        
        # Main container frame for better layout control
        self.container = ttk.Frame(self, style='Login.TFrame')
        self.container.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Header
        ttk.Label(self.container, 
                 text="أهلا بك في نظام إدارة الجدول", 
                 style='LoginHeader.TLabel').pack(pady=(0, 30))
        
        # Login frame
        login_frame = ttk.Frame(self.container, style='LoginBox.TFrame')
        login_frame.pack(pady=10, padx=20, fill='x')
        
        # Login title
        ttk.Label(login_frame, 
                 text="تسجيل دخول", 
                 style='LoginTitle.TLabel').pack(pady=(20, 30))
        
        # Username field
        username_frame = ttk.Frame(login_frame, style='LoginBox.TFrame')
        username_frame.pack(fill='x', padx=30, pady=(0, 15))
        ttk.Label(username_frame, 
                 text="اسم المستخدم:", 
                 style='LoginLabel.TLabel').pack(side='left', padx=(0, 10))
        self.username_entry = ttk.Entry(username_frame, style='Login.TEntry')
        self.username_entry.pack(side='right', expand=True, fill='x')
        
        # Password field
        password_frame = ttk.Frame(login_frame, style='LoginBox.TFrame')
        password_frame.pack(fill='x', padx=30, pady=(0, 30))
        ttk.Label(password_frame, 
                 text="كلمة المرور:", 
                 style='LoginLabel.TLabel').pack(side='left', padx=(0, 10))
        self.password_entry = ttk.Entry(password_frame, show="*", style='Login.TEntry')
        self.password_entry.pack(side='right', expand=True, fill='x')
        
        # Login button
        ttk.Button(login_frame, 
                  text="دخول", 
                  command=self.login,
                  style='Login.TButton').pack(pady=(0, 20), ipadx=20, ipady=5)
        
        # Set default credentials
        self.username_entry.insert(0, "admin")
        self.password_entry.insert(0, "admin")
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda event: self.login())

    def _configure_styles(self):
        """Configure custom styles for the login page"""
        # Background style
        self.style.configure('Login.TFrame', background='#f5f7fa')
        
        # Header style
        self.style.configure('LoginHeader.TLabel', 
                           font=('Arial', 18, 'bold'),
                           foreground='#2c3e50',
                           background='#f5f7fa')
        
        # Login box style
        self.style.configure('LoginBox.TFrame', 
                           background='#ffffff',
                           borderwidth=1,
                           relief='solid',
                           bordercolor='#e0e0e0')
        
        # Title style
        self.style.configure('LoginTitle.TLabel',
                           font=('Arial', 16, 'bold'),
                           foreground='#3498db',
                           background='#ffffff')
        
        # Label style
        self.style.configure('LoginLabel.TLabel',
                           font=('Arial', 10),
                           foreground='#7f8c8d',
                           background='#ffffff')
        
        # Entry style
        self.style.configure('Login.TEntry',
                           font=('Arial', 10),
                           foreground='#2c3e50',
                           fieldbackground='#ffffff',
                           padding=5,
                           bordercolor='#bdc3c7',
                           lightcolor='#bdc3c7',
                           darkcolor='#bdc3c7')
        
        # Button style
        self.style.configure('Login.TButton',
                           font=('Arial', 10, 'bold'),
                           foreground='#ffffff',
                           background='#3498db',
                           borderwidth=0,
                           padding=(15, 5),
                           focusthickness=0,
                           focuscolor='none')
        
        # Button hover effects
        self.style.map('Login.TButton',
                      background=[('active', '#2980b9'), ('pressed', '#2980b9')],
                      foreground=[('active', '#ffffff'), ('pressed', '#ffffff')])

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("خطأ", "أرجوا إدخال اسم المستخدم وكلمة المرور")
            return

        try:
            if not os.path.exists(USERS_FILE):
                messagebox.showerror("خطأ", f"لم أعثر على ملف المستخدمين: {USERS_FILE}")
                return

            with open(USERS_FILE, "r") as f:
                users = json.load(f)

            if username in users and users[username] == password:
                self.controller.show_frame(HomePage)
            else:
                messagebox.showerror("خطأ", "خطأ في اسم المستخدم أو كلمة المرور")
        except Exception as e:

            messagebox.showerror("خطأ", f"حدث خطأ غير متوقع: {str(e)}")
