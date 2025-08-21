import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from home import HomePage

DATA_DIR = "data"
TEACHERS_FILE = os.path.join(DATA_DIR, "teachers.json")
SUBJECTS_FILE = os.path.join(DATA_DIR, "subjects.json")

class TeacherManagerPage(ttk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grades = ['ثالث أ', 'ثالث ب', 'رابع أ', 'رابع ب', 'خامس أ', 'خامس ب', 'سادس أ', 'سادس ب']
        
        # Configure styles
        self.style = ttk.Style()
        self._configure_styles()
        
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Main container with padding
        self.container = ttk.Frame(self, style='Main.TFrame')
        self.container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Main title
        ttk.Label(self.container, 
                 text="إدارة المعلمين والمقررات", 
                 style='Header.TLabel').pack(pady=(0, 20))
        
        # Teacher selection frame
        self.teacher_frame = ttk.LabelFrame(self.container, 
                                          text="إدارة المعلمين",
                                          style='Card.TLabelframe')
        self.teacher_frame.pack(fill="x", pady=10, padx=5)
        
        # Teacher combobox
        ttk.Label(self.teacher_frame, 
                 text="اختر معلم:", 
                 style='Bold.TLabel').grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.teacher_var = tk.StringVar()
        self.teacher_combobox = ttk.Combobox(
            self.teacher_frame, 
            textvariable=self.teacher_var, 
            state="readonly",
            style='Custom.TCombobox'
        )
        self.teacher_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Teacher action buttons
        btn_frame = ttk.Frame(self.teacher_frame, style='Card.TFrame')
        btn_frame.grid(row=0, column=2, padx=10)
        
        self.add_teacher_btn = ttk.Button(
            btn_frame, 
            text="إضافة معلم", 
            command=self.show_add_teacher_dialog,
            style='Accent.TButton'
        )
        self.add_teacher_btn.pack(side="right", padx=5, ipadx=10)
        
        self.edit_btn = ttk.Button(
            btn_frame, 
            text="تعديل المقررات", 
            command=self.load_teacher_data,
            style='Primary.TButton'
        )
        self.edit_btn.pack(side="right", padx=5, ipadx=10)
        
        self.refresh_btn = ttk.Button(
            btn_frame, 
            text="تحديث", 
            command=self.refresh_data,
            style='Secondary.TButton'
        )
        self.refresh_btn.pack(side="right", padx=5, ipadx=10)

        # Subject management frame (initially hidden)
        self.subject_frame = ttk.LabelFrame(
            self.container, 
            text="تعيين المقررات حسب الفصل",
            style='Card.TLabelframe'
        )
        
        # Notebook style configuration
        self.style.configure('Custom.TNotebook', background='#f0f0f0')
        self.style.configure('Custom.TNotebook.Tab', 
                           font=('Arial', 9, 'bold'),
                           padding=[10, 5])
        
        self.grade_notebook = ttk.Notebook(
            self.subject_frame, 
            style='Custom.TNotebook'
        )
        self.grade_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create grade-specific tabs
        self.grade_frames = {}
        self.subject_vars = {}
        self.subject_combos = {}
        
        for grade in self.grades:
            frame = ttk.Frame(self.grade_notebook, style='Card.TFrame')
            self.grade_frames[grade] = frame
            self.grade_notebook.add(frame, text=grade)
            
            # Subject selection
            ttk.Label(frame, 
                     text="تحديد المقرر:", 
                     style='Bold.TLabel').grid(row=0, column=0, padx=10, pady=10, sticky="w")
            
            self.subject_vars[grade] = tk.StringVar()
            self.subject_combos[grade] = ttk.Combobox(
                frame, 
                textvariable=self.subject_vars[grade],
                state="readonly",
                style='Custom.TCombobox'
            )
            self.subject_combos[grade].grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            # Add subject button
            ttk.Button(
                frame, 
                text="إضافة مقرر", 
                command=lambda g=grade: self.add_subject_to_grade(g),
                style='Small.TButton'
            ).grid(row=0, column=2, padx=10, pady=10)
        
        # Subject list display with scrollbar
        list_frame = ttk.Frame(self.subject_frame, style='Card.TFrame')
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Custom listbox style
        self.subject_listbox = tk.Listbox(
            list_frame, 
            height=8,
            bg='white',
            fg='#333333',
            selectbackground='#3498db',
            selectforeground='white',
            font=('Arial', 10),
            borderwidth=1,
            relief='solid',
            highlightthickness=0
        )
        self.subject_listbox.pack(side="right", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(
            list_frame, 
            orient="vertical", 
            command=self.subject_listbox.yview
        )
        scrollbar.pack(side="left", fill="y")
        self.subject_listbox.config(yscrollcommand=scrollbar.set)
        
        # Action buttons frame
        btn_frame = ttk.Frame(self.subject_frame, style='Card.TFrame')
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.del_subject_btn = ttk.Button(
            btn_frame, 
            text="حذف المحدد", 
            command=self.delete_subject_from_teacher,
            style='Danger.TButton'
        )
        self.del_subject_btn.pack(side="right", padx=5, ipadx=10)
        
        self.save_btn = ttk.Button(
            btn_frame, 
            text="حفظ التغييرات", 
            command=self.save_teacher_data,
            style='Success.TButton'
        )
        self.save_btn.pack(side="left", padx=5, ipadx=10)
        
        # Back button
        from home import HomePage
        ttk.Button(
            self.container, 
            text=">- العودة إلى الرئيسية", 
            command=lambda: controller.show_frame(HomePage),
            style='Secondary.TButton'
        ).pack(pady=(20, 0))
        
        self.load_data()

    def _configure_styles(self):
        """Configure custom styles for the teacher manager"""
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
        
        # Combobox style
        self.style.configure('Custom.TCombobox',
                           fieldbackground='white',
                           foreground='#2c3e50',
                           padding=5,
                           bordercolor='#bdc3c7',
                           lightcolor='#bdc3c7',
                           darkcolor='#bdc3c7')
        
        # Button styles
        self.style.configure('Primary.TButton',
                           foreground='white',
                           background='#3498db',
                           font=('Arial', 9, 'bold'),
                           borderwidth=0,
                           padding=(10, 5))
        
        self.style.configure('Accent.TButton',
                           foreground='white',
                           background='#9b59b6',
                           font=('Arial', 9, 'bold'),
                           borderwidth=0,
                           padding=(10, 5))
        
        self.style.configure('Secondary.TButton',
                           foreground='#2c3e50',
                           background='#ecf0f1',
                           font=('Arial', 9, 'bold'),
                           borderwidth=0,
                           padding=(10, 5))
        
        self.style.configure('Success.TButton',
                           foreground='white',
                           background='#2ecc71',
                           font=('Arial', 9, 'bold'),
                           borderwidth=0,
                           padding=(10, 5))
        
        self.style.configure('Danger.TButton',
                           foreground='white',
                           background='#e74c3c',
                           font=('Arial', 9, 'bold'),
                           borderwidth=0,
                           padding=(10, 5))
        
        self.style.configure('Small.TButton',
                           foreground='white',
                           background='#3498db',
                           font=('Arial', 8),
                           borderwidth=0,
                           padding=(5, 3))
        
        # Button hover effects
        for style in ['Primary', 'Accent', 'Secondary', 'Success', 'Danger', 'Small']:
            self.style.map(f'{style}.TButton',
                          foreground=[('active', 'white'), ('pressed', 'white')],
                          background=[('active', f'#{int("3498db"[1:3], 16)-0x101010:#06x}'), 
                                    ('pressed', f'#{int("3498db"[1:3], 16)-0x202020:#06x}')])

    def refresh_data(self):
        """Refresh both teachers and subjects"""
        self.load_data()
        messagebox.showinfo("تم", "تم تحديث البيانات بنجاح")

    def load_data(self):
        """Load data from JSON files"""
        try:
            with open(TEACHERS_FILE, "r") as f:
                self.teachers = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.teachers = []
            
        try:
            with open(SUBJECTS_FILE, "r") as f:
                self.subjects = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.subjects = []
            
        self.update_teacher_combobox()
        self.update_subject_comboboxes()

    def update_teacher_combobox(self):
        """Update teacher dropdown"""
        teacher_names = [t["name"] for t in self.teachers]
        self.teacher_combobox["values"] = teacher_names
        if teacher_names:
            self.teacher_var.set(teacher_names[0])
        else:
            self.teacher_var.set("")

    def update_subject_comboboxes(self):
        """Update all grade subject comboboxes"""
        for grade in self.grades:
            self.subject_combos[grade]["values"] = sorted(self.subjects)
            if self.subjects:
                self.subject_vars[grade].set(self.subjects[0])
            else:
                self.subject_vars[grade].set("")

    def show_add_teacher_dialog(self):
        """Show dialog to add new teacher"""
        dialog = tk.Toplevel(self)
        dialog.title("أضف معلم جديد")
        dialog.resizable(False, False)
        dialog.configure(bg='#f5f7fa')
        
        # Center the dialog
        self._center_dialog(dialog)
        
        ttk.Label(dialog, 
                 text="اسم المعلم:", 
                 style='Bold.TLabel').pack(pady=5)
        
        name_entry = ttk.Entry(dialog, style='Custom.TCombobox')
        name_entry.pack(pady=5, padx=20, fill="x")
        
        btn_frame = ttk.Frame(dialog, style='Card.TFrame')
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, 
                  text="إلغاء", 
                  command=dialog.destroy,
                  style='Secondary.TButton').pack(side="right", padx=10)
        
        ttk.Button(btn_frame, 
                  text="إضافة", 
                  command=lambda: self.add_teacher(name_entry.get(), dialog),
                  style='Success.TButton').pack(side="left", padx=10)
        
        name_entry.focus_set()

    def _center_dialog(self, dialog):
        """Center the dialog window on screen"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')

    def add_teacher(self, name, dialog):
        """Add new teacher to the system"""
        name = name.strip()
        if not name:
            messagebox.showwarning("تحذير", "لا يمكن لاسم المعلم أن يكون فارغ")
            return
            
        if any(t["name"].lower() == name.lower() for t in self.teachers):
            messagebox.showwarning("تحذير", "المعلم موجود بالفعل.")
            return
            
        self.teachers.append({
            "name": name,
            "subjects": []
        })
        self.save_teacher_data()  # Fixed this line
        self.update_teacher_combobox()
        self.teacher_var.set(name)
        dialog.destroy()
        messagebox.showinfo("تم", f"المعلم {name} أضيف بنجاح")

    def load_teacher_data(self):
        """Load subjects for selected teacher"""
        teacher_name = self.teacher_var.get()
        if not teacher_name:
            messagebox.showwarning("تحذير", "الرجاء اختيار معلم أولاً.")
            return
            
        if not self.subject_frame.winfo_ismapped():
            self.subject_frame.pack(fill="both", expand=True, padx=5, pady=10)
            
        teacher = next((t for t in self.teachers if t["name"] == teacher_name), None)
        if not teacher:
            messagebox.showerror("خطأ", "المعلم غير موجود!")
            return
            
        self.update_subject_listbox(teacher)

    def update_subject_listbox(self, teacher):
        """Update the subject listbox for a teacher"""
        self.subject_listbox.delete(0, tk.END)
        for subject in sorted(teacher["subjects"], key=lambda x: x["name"]):
            grades = ", ".join(sorted(subject["grades"]))
            self.subject_listbox.insert(tk.END, f"{subject['name']} (Grades: {grades})")

    def add_subject_to_grade(self, grade):
        """Add subject to teacher for specific grade"""
        teacher_name = self.teacher_var.get()
        if not teacher_name:
            messagebox.showwarning("تحذير", "الرجاء اختيار معلم أولاً.")
            return
            
        subject_name = self.subject_vars[grade].get()
        if not subject_name:
            messagebox.showwarning("تحذير", "الرجاء اختيار مقرر.")
            return
            
        teacher = next((t for t in self.teachers if t["name"] == teacher_name), None)
        if not teacher:
            messagebox.showerror("خطأ", "المعلم غير موجود!")
            return
            
        # Check if subject exists for this teacher
        subject_data = next((s for s in teacher["subjects"] if s["name"] == subject_name), None)
        
        if subject_data:
            if grade in subject_data["grades"]:
                messagebox.showwarning("تحذير", 
                    f"{subject_name} تم تعيينه إلى المعلم {teacher_name} لفصل {grade}")
                return
            else:
                subject_data["grades"].append(grade)
        else:
            teacher["subjects"].append({
                "name": subject_name,
                "grades": [grade]
            })
        
        self.update_subject_listbox(teacher)
        self.subject_vars[grade].set("")

    def delete_subject_from_teacher(self):
        """Delete selected subject from teacher"""
        teacher_name = self.teacher_var.get()
        if not teacher_name:
            messagebox.showwarning("تحذير", "الرجاء اختيار معلم أولاً")
            return
            
        selected = self.subject_listbox.curselection()
        if not selected:
            messagebox.showwarning("تحذير", "الرجاء تحديد مقرر للحذف.")
            return
            
        idx = selected[0]
        teacher = next((t for t in self.teachers if t["name"] == teacher_name), None)
        if not teacher:
            messagebox.showerror("خطأ", "المعلم غير موجود!")
            return
            
        subject_name = teacher["subjects"][idx]["name"]
        
        confirm = messagebox.askyesno(
            "تأكيد الحذف",
            f"أتريد حذف {subject_name} من مقررات المعلم {teacher_name}'؟",
            icon="warning"
        )
        
        if confirm:
            teacher["subjects"].pop(idx)
            self.update_subject_listbox(teacher)
            messagebox.showinfo("تم", f"حذفنا {subject_name} من {teacher_name}")

    def save_teacher_data(self):
        """Save teacher data to file"""
        try:
            with open(TEACHERS_FILE, "w") as f:
                json.dump(self.teachers, f, indent=4)
            messagebox.showinfo("تم", "تم حفظ بيانات المعلم بنجاح.")
            return True
        except Exception as e:
            messagebox.showerror("خطأ", f"فشلنا في حفظ بيانات المعلم: {str(e)}")
            return False

    def save_subjects(self):
        """Save subjects data to file"""
        try:
            with open(SUBJECTS_FILE, "w") as f:
                json.dump(self.subjects, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("خطأ", f"فشلنا في حفظ بيانات المقرر: {str(e)}")

            return False
