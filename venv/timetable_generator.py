import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from tkinter import filedialog
from ortools.sat.python import cp_model
from typing import TYPE_CHECKING, Dict, List, Tuple
import pandas as pd

if TYPE_CHECKING:
    from home import HomePage

DATA_DIR = "data"
SUBJECTS_FILE = os.path.join(DATA_DIR, "subjects.json")
TEACHERS_FILE = os.path.join(DATA_DIR, "teachers.json")
DAYS = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس"]
PERIODS = 8  # Number of periods per day

class TimetableGeneratorPage(ttk.Frame):
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
        
        # Title frame with back button
        title_frame = ttk.Frame(self.container, style='Card.TFrame')
        title_frame.pack(fill="x", pady=(0, 20))
        
        # Back button with arrow icon
        from home import HomePage
        ttk.Button(
            title_frame,
            text=">- العودة إلى الرئيسية",
            command=lambda: controller.show_frame(HomePage),
            style='Secondary.TButton'
        ).pack(side="right", padx=10)
        
        # Page title
        ttk.Label(
            title_frame,
            text="منشئ الجدول",
            style='Header.TLabel'
        ).pack(side="right", padx=10)
        
        # Grade selection frame with card styling
        grade_frame = ttk.LabelFrame(
            self.container,
            text="اختر الفصول",
            style='Card.TLabelframe'
        )
        grade_frame.pack(fill="x", padx=10, pady=10)
        
        self.grade_vars = {}
        grades =  ['ثالث أ', 'ثالث ب', 'رابع أ', 'رابع ب', 'خامس أ', 'خامس ب', 'سادس أ', 'سادس ب']
        
        # Create checkboxes for each grade with consistent styling
        for i, grade in enumerate(grades):
            self.grade_vars[grade] = tk.IntVar()
            cb = ttk.Checkbutton(
                grade_frame, 
                text=grade, 
                variable=self.grade_vars[grade],
                onvalue=1, 
                offvalue=0,
                style='Custom.TCheckbutton'
            )
            cb.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Select all grades button
        ttk.Button(
            grade_frame, 
            text="تحديد الكل", 
            command=lambda: [var.set(1) for var in self.grade_vars.values()],
            style='Small.TButton'
        ).grid(row=0, column=len(grades), padx=5, pady=5)

        # Subject selection notebook with custom styling
        self.subject_notebook = ttk.Notebook(
            self.container,
            style='Custom.TNotebook'
        )
        self.subject_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Dictionary to hold subject frames and variables for each grade
        self.grade_subject_frames: Dict[str, ttk.Frame] = {}
        self.grade_subject_vars: Dict[str, Dict[str, tk.IntVar]] = {}
        self.grade_period_entries: Dict[str, Dict[str, ttk.Entry]] = {}
        
        # Initialize subject frames for each grade
        for grade in grades:
            self.create_grade_subject_frame(grade)
        
        # Action buttons frame
        action_frame = ttk.Frame(self.container, style='Card.TFrame')
        action_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Refresh button
        ttk.Button(
            action_frame,
            text="🔄 تحديث المقررات",
            command=self.load_subjects,
            style='Secondary.TButton'
        ).pack(side="right", padx=5, ipadx=10)
        
        # Generate button with accent color
        ttk.Button(
            action_frame, 
            text="أنشئ الجدول", 
            command=self.generate_timetable,
            style='Accent.TButton'
        ).pack(side="left", padx=5, ipadx=10)
        
        # Output frame for displaying timetables
        self.output_frame = ttk.Frame(self.container, style='Card.TFrame')
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load subjects initially
        self.load_subjects()

    def _configure_styles(self):
        """Configure custom styles for the timetable generator"""
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
        
        # Checkbutton style
        self.style.configure('Custom.TCheckbutton',
                           font=('Arial', 9),
                           foreground='#34495e',
                           background='#ffffff')
        
        # Notebook style
        self.style.configure('Custom.TNotebook', background='#f5f7fa')
        self.style.configure('Custom.TNotebook.Tab', 
                           font=('Arial', 9, 'bold'),
                           padding=[10, 5],
                           background='#ecf0f1',
                           foreground='#2c3e50')
        self.style.map('Custom.TNotebook.Tab',
                      background=[('selected', '#3498db'), ('active', '#2980b9')],
                      foreground=[('selected', 'white'), ('active', 'white')])
        
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
        
        self.style.configure('Accent.TButton',
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
        
        self.style.configure('Small.TButton',
                           foreground='white',
                           background='#3498db',
                           font=('Arial', 9),
                           borderwidth=0,
                           padding=(5, 3))
        
        # Button hover effects
        button_styles = {
            'Primary': '#3498db',
            'Secondary': '#ecf0f1',
            'Accent': '#2ecc71',
            'Danger': '#e74c3c',
            'Small': '#3498db'
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

    def create_grade_subject_frame(self, grade: str):
        """Create a subject selection frame for a specific grade"""
        frame = ttk.Frame(self.subject_notebook, style='Card.TFrame')
        self.subject_notebook.add(frame, text=grade)
        self.grade_subject_frames[grade] = frame
        
        # Label for the grade's subject selection
        ttk.Label(frame, 
                 text=f"اختر مقررات فصل {grade}", 
                 style='Bold.TLabel').pack(pady=5)
        
        # Frame for subject checkboxes and period entries
        subj_frame = ttk.Frame(frame, style='Card.TFrame')
        subj_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Initialize dictionaries for this grade
        self.grade_subject_vars[grade] = {}
        self.grade_period_entries[grade] = {}
        
        # Placeholder for subject widgets - will be populated in load_subjects
        self.grade_subject_frames[grade].subj_frame = subj_frame

    def load_subjects(self):
        """Load subjects from JSON file and populate for each grade"""
        try:
            with open(SUBJECTS_FILE, "r") as f:
                subjects = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            subjects = []
            messagebox.showwarning("تحذير", "لم نعثر على مقررات، نرجوا إضافة مقررات أولاً.")
            return

        # Clear existing widgets in each grade's subject frame
        for grade, frame in self.grade_subject_frames.items():
            for widget in frame.subj_frame.winfo_children():
                widget.destroy()
            
            # Reset the dictionaries for this grade
            self.grade_subject_vars[grade].clear()
            self.grade_period_entries[grade].clear()

            # Create a canvas and scrollbar for the subject frame
            canvas = tk.Canvas(frame.subj_frame, 
                             bg='white',
                             highlightthickness=0)
            scrollbar = ttk.Scrollbar(frame.subj_frame, 
                                    orient="vertical", 
                                    command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="right", fill="both", expand=True)
            scrollbar.pack(side="left", fill="y")
            
            # Update the subj_frame reference to the scrollable frame
            frame.subj_frame = scrollable_frame

        # Create subject selection widgets for each grade
        for grade in self.grade_subject_frames.keys():
            for i, subject in enumerate(sorted(subjects)):
                # Subject checkbox
                var = tk.IntVar()
                cb = ttk.Checkbutton(
                    self.grade_subject_frames[grade].subj_frame,
                    text=subject,
                    variable=var,
                    command=lambda g=grade: self.update_entry_state(g),
                    style='Custom.TCheckbutton'
                )
                cb.grid(row=i, column=0, sticky="w", padx=5, pady=2)
                self.grade_subject_vars[grade][subject] = var
                
                # Periods entry
                entry = ttk.Entry(
                    self.grade_subject_frames[grade].subj_frame, 
                    width=5, 
                    style='Custom.TEntry'
                )
                entry.config(state="disabled")
                entry.grid(row=i, column=1, padx=5, pady=2)
                self.grade_period_entries[grade][subject] = entry
                
                # Periods label
                ttk.Label(
                    self.grade_subject_frames[grade].subj_frame,
                    text="periods/week",
                    style='Small.TLabel'
                ).grid(row=i, column=2, sticky="w", padx=5, pady=2)

    def update_entry_state(self, grade: str):
        """Enable/disable period entries based on checkbox state for a specific grade"""
        for subject, var in self.grade_subject_vars[grade].items():
            entry = self.grade_period_entries[grade][subject]
            if var.get():
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, "2")  # Default to 2 periods per week
            else:
                entry.delete(0, tk.END)
                entry.config(state="disabled")

    def generate_timetable(self):
        """Main method to generate timetables for selected grades"""
        # Get selected grades
        selected_grades = [grade for grade, var in self.grade_vars.items() if var.get()]
        if not selected_grades:
            messagebox.showwarning("تحذير", "يرجى اختيار فصل واحد على الأقل")
            return
            
        # Get selected subjects and periods for each grade
        grade_subject_periods = {}
        for grade in selected_grades:
            selected_subjects = [subj for subj, var in self.grade_subject_vars[grade].items() if var.get()]
            if not selected_subjects:
                messagebox.showwarning("تحذير", f"يرجى اختيار مقرر واحد على الأقل لفصل {grade}")
                return
                
            subject_periods = {}
            for subject in selected_subjects:
                periods = self.grade_period_entries[grade][subject].get()
                if not periods.isdigit() or int(periods) <= 0:
                    messagebox.showwarning("تحذير", f"يرجى إدخال عدد حصص صحيح لـ{subject} صف {grade}")
                    return
                subject_periods[subject] = int(periods)
            
            grade_subject_periods[grade] = subject_periods
        
        # Load teacher data
        try:
            with open(TEACHERS_FILE, "r") as f:
                teachers = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            teachers = []
            messagebox.showwarning("تحذير", "لم نعثر على بيانات معلمين")
            return
            
        # Generate timetable for all grades together
        try:
            all_timetables = self.generate_with_ortools(grade_subject_periods, teachers)
            self.show_timetables(all_timetables)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في إنشاء جدول: {str(e)}")

    def generate_with_ortools(self, grade_subject_periods: Dict[str, Dict[str, int]], teachers: List[dict]):
        """Generate timetable for multiple grades with no teacher clashes"""
        model = cp_model.CpModel()
        all_assignments = {}
        
        # Create variables for each grade
        for grade, subject_periods in grade_subject_periods.items():
            all_subjects = list(subject_periods.keys())
            
            # Get teachers qualified for this grade's subjects
            teacher_subjects = {}
            for teacher in teachers:
                for subj in teacher.get('subjects', []):
                    if subj['name'] in all_subjects and grade in subj.get('grades', []):
                        if teacher['name'] not in teacher_subjects:
                            teacher_subjects[teacher['name']] = []
                        teacher_subjects[teacher['name']].append(subj['name'])
            
            # Create assignment variables for this grade
            for day in DAYS:
                for period in range(PERIODS):
                    for subject in all_subjects:
                        for teacher in [t for t in teacher_subjects if subject in teacher_subjects[t]]:
                            var_name = f"{grade}_{day}_{period}_{subject}_{teacher}"
                            all_assignments[var_name] = model.NewBoolVar(var_name)
            
            # Subject must be scheduled required periods
            for subject, periods_needed in subject_periods.items():
                model.Add(
                    sum(all_assignments[f"{grade}_{day}_{period}_{subject}_{teacher}"]
                        for day in DAYS
                        for period in range(PERIODS)
                        for teacher in [t for t in teacher_subjects if subject in teacher_subjects[t]]
                    ) == periods_needed
                )
            
            # No two subjects at same time in same grade
            for day in DAYS:
                for period in range(PERIODS):
                    model.AddAtMostOne(
                        all_assignments[f"{grade}_{day}_{period}_{subject}_{teacher}"]
                        for subject in all_subjects
                        for teacher in [t for t in teacher_subjects if subject in teacher_subjects[t]]
                    )

        # Teacher can't be in two places at same time across all grades
        all_teachers = [t['name'] for t in teachers]
        for teacher in all_teachers:
            for day in DAYS:
                for period in range(PERIODS):
                    model.AddAtMostOne(
                        all_assignments[f"{grade}_{day}_{period}_{subject}_{teacher}"]
                        for grade in grade_subject_periods.keys()
                        for subject in grade_subject_periods[grade]
                        if f"{grade}_{day}_{period}_{subject}_{teacher}" in all_assignments
                    )

        # Solve the model
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            timetables = {}
            for grade in grade_subject_periods.keys():
                timetable = {day: [('', '') for _ in range(PERIODS)] for day in DAYS}
                for day in DAYS:
                    for period in range(PERIODS):
                        for subject in grade_subject_periods[grade]:
                            for teacher in all_teachers:
                                var_name = f"{grade}_{day}_{period}_{subject}_{teacher}"
                                if var_name in all_assignments and solver.Value(all_assignments[var_name]):
                                    timetable[day][period] = (subject, teacher)
                timetables[grade] = timetable
            return timetables
        else:
            raise RuntimeError("No solution found")

    def show_timetables(self, timetables: Dict[str, Dict[str, List[tuple]]]):
        """Display the generated timetables with enhanced styling"""
        for widget in self.output_frame.winfo_children():
            widget.destroy()
            
        notebook = ttk.Notebook(self.output_frame, style='Custom.TNotebook')
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure Treeview style for larger cells
        self.style.configure('Timetable.Treeview', 
                           rowheight=40,
                           font=('Arial', 10),
                           background='white',
                           fieldbackground='white',
                           foreground='#2c3e50')
        
        self.style.configure('Timetable.Treeview.Heading', 
                           font=('Arial', 10, 'bold'),
                           background='#3498db',
                           foreground='white',
                           relief='flat')
        
        self.style.map('Timetable.Treeview.Heading',
                      background=[('active', '#2980b9')])
        
        # Configure tag colors for alternating rows
        self.style.configure('Even.Treeview', background='white')
        self.style.configure('Odd.Treeview', background='#f5f7fa')
        
        for grade, timetable in timetables.items():
            frame = ttk.Frame(notebook, style='Card.TFrame')
            notebook.add(frame, text=grade)
            
            # Create Treeview with enhanced styling
            tree = ttk.Treeview(
                frame, 
                columns=['Period'] + DAYS, 
                show="headings",
                height=PERIODS,
                style='Timetable.Treeview'
            )
            
            # Configure columns with increased width
            tree.heading('Period', text='الحصة')
            tree.column('Period', width=100, anchor='center')
            
            for day in DAYS:
                tree.heading(day, text=day)
                tree.column(day, width=200, anchor='center')
            
            # Add timetable data with alternating row colors
            for period in range(PERIODS):
                period_data = [f"Period {period+1}"]
                for day in DAYS:
                    subject, teacher = timetable[day][period]
                    display_text = f"{subject}\n({teacher})" if subject else ""
                    period_data.append(display_text)
                
                tag = 'even' if period % 2 == 0 else 'odd'
                tree.insert("", "end", values=period_data, tags=(tag,))
            
            # Add scrollbars
            yscroll = ttk.Scrollbar(
                frame, 
                orient="vertical", 
                command=tree.yview,
                style='Custom.Vertical.TScrollbar'
            )
            xscroll = ttk.Scrollbar(
                frame, 
                orient="horizontal", 
                command=tree.xview,
                style='Custom.Horizontal.TScrollbar'
            )
            tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
            
            # Grid layout
            tree.grid(row=0, column=0, sticky="nsew")
            yscroll.grid(row=0, column=1, sticky="ns")
            xscroll.grid(row=1, column=0, sticky="ew")
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            
            # Add export button for this grade's timetable
            export_frame = ttk.Frame(frame, style='Card.TFrame')
            export_frame.grid(row=2, column=0, columnspan=2, sticky="e", pady=(5, 0))
            
            ttk.Button(
                export_frame,
                text=f"تصدير {grade} إلى أكسل",
                command=lambda g=grade, t=timetable: self.export_grade_to_excel(g, t),
                style='Small.TButton'
            ).pack(side="left", padx=5)
        
        # Add export all button
        export_all_frame = ttk.Frame(self.output_frame, style='Card.TFrame')
        export_all_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ttk.Button(
            export_all_frame,
            text="تصدير الكل إلى إكسل",
            command=lambda: self.export_to_excel(timetables),
            style='Accent.TButton'
        ).pack(side="left", padx=5, pady=5)

    def export_grade_to_excel(self, grade: str, timetable: Dict[str, List[tuple]]):
        """Export a single grade's timetable to Excel"""
        try:
            # Create a DataFrame for the timetable
            data = []
            for period in range(PERIODS):
                row = [f"Period {period+1}"]
                for day in DAYS:
                    subject, teacher = timetable[day][period]
                    row.append(f"{subject} ({teacher})" if subject else "")
                data.append(row)
            
            df = pd.DataFrame(data, columns=['Period'] + DAYS)
            
            # Prompt user to select save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title=f"حفظ جدول فصل {grade} كـ",
                initialfile=f"{grade}_timetable.xlsx",
                initialdir=DATA_DIR
            )
            
            if not file_path:  # User cancelled
                return
                
            # Write to Excel
            df.to_excel(file_path, sheet_name=grade[:31], index=False)
            messagebox.showinfo("تم", f"جدول فصل {grade} تصدر إلى:\n{file_path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تصدير جدول فصل {grade}:\n{str(e)}")

    def export_to_excel(self, timetables: Dict[str, Dict[str, List[tuple]]]):
        """Export all timetables to a single Excel file with multiple sheets"""
        try:
            # Prompt user to select save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="حفظ كل الجداول كـ",
                initialfile="all_timetables.xlsx",
                initialdir=DATA_DIR
            )
            
            if not file_path:  # User cancelled
                return
                
            # Create a Pandas Excel writer
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                for grade, timetable in timetables.items():
                    # Create a DataFrame for each grade
                    data = []
                    for period in range(PERIODS):
                        row = [f"Period {period+1}"]
                        for day in DAYS:
                            subject, teacher = timetable[day][period]
                            row.append(f"{subject} ({teacher})" if subject else "")
                        data.append(row)
                    
                    df = pd.DataFrame(data, columns=['Period'] + DAYS)
                    df.to_excel(writer, sheet_name=grade[:31], index=False)
                    
                    # Auto-adjust columns' width
                    worksheet = writer.sheets[grade[:31]]
                    for i, col in enumerate(df.columns):
                        max_len = max(df[col].astype(str).map(len).max(), len(col))
                        worksheet.set_column(i, i, min(max_len + 2, 50))
            
            messagebox.showinfo("تم", f"تم تصدير كل الجداول إلى:\n{file_path}")
        except PermissionError:
            messagebox.showerror("خطأ", "التصريح مرفوض، تأكد أن ملف الاكسل مغلق وحاول مرة أخرى.")
        except Exception as e:

            messagebox.showerror("خطأ", f"فشل في تصدير الجداول:\n{str(e)}")

