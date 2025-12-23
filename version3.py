import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np

class StudentAttendanceSystem():
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Management System")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        # style setup for ttk widgets
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="#222222", foreground="#ffffff",
                        fieldbackground="#222222", rowheight=32)
        style.map('Treeview', background=[('selected', '#444444')])
        style.configure("TCombobox", fieldbackground="#333333", background="#222222", foreground="#ffffff")

        title = tk.Label(self.root, text="Student Attendance Management System", bd=4, relief="raised",
                         bg="#222222", fg="#ffffff", font=("Elephant", 40, "bold"))
        title.pack(side="top", fill="x")

        # option frame
        optFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#1a1a1a")
        optFrame.place(width=self.width/3, height=self.height-180, x=50, y=100)

        addBtn = tk.Button(optFrame, command=self.addFrameFun, text="Add Student", bd=3, relief="raised",
                           bg="#333333", fg="#ffffff", width=20, font=("Arial", 16, "bold"))
        addBtn.grid(row=0, column=0, padx=30, pady=15)

        srchBtn = tk.Button(optFrame, command=self.searchFrameFun, text="Search Student", bd=3, relief="raised",
                            bg="#333333", fg="#ffffff", width=20, font=("Arial", 16, "bold"))
        srchBtn.grid(row=1, column=0, padx=30, pady=15)

        updBtn = tk.Button(optFrame, command=self.updFrameFun, text="Update Record", bd=3, relief="raised",
                           bg="#333333", fg="#ffffff", width=20, font=("Arial", 16, "bold"))
        updBtn.grid(row=2, column=0, padx=30, pady=15)

        allBtn = tk.Button(optFrame, command=self.showAll, text="Show All", bd=3, relief="raised",
                           bg="#333333", fg="#ffffff", width=20, font=("Arial", 16, "bold"))
        allBtn.grid(row=3, column=0, padx=30, pady=15)

        delBtn = tk.Button(optFrame, command=self.delFrameFun, text="Remove Student", bd=3, relief="raised",
                           bg="#333333", fg="#ffffff", width=20, font=("Arial", 16, "bold"))
        delBtn.grid(row=4, column=0, padx=30, pady=15)

        # Attendance buttons
        markAttnBtn = tk.Button(optFrame, command=self.markAttendanceFrameFun, text="Mark Attendance", bd=3, relief="raised",
                               bg="#333333", fg="#ffffff", width=20, font=("Arial", 16, "bold"))
        markAttnBtn.grid(row=5, column=0, padx=30, pady=15)

        viewAttnBtn = tk.Button(optFrame, command=self.viewAttendanceFrameFun, text="View Attendance", bd=3, relief="raised",
                               bg="#333333", fg="#ffffff", width=20, font=("Arial", 16, "bold"))
        viewAttnBtn.grid(row=6, column=0, padx=30, pady=15)

        # Attendance Calculator button
        calcAttnBtn = tk.Button(optFrame, command=self.attendanceCalculatorFrameFun, text="Attendance Calculator", bd=3, relief="raised",
                               bg="#333333", fg="#ffffff", width=20, font=("Arial", 16, "bold"))
        calcAttnBtn.grid(row=7, column=0, padx=30, pady=15)

        # Chart buttons frame
        chartFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#1a1a1a")
        chartFrame.place(width=self.width/3, height=220, x=50, y=self.height-270)

        chartTitle = tk.Label(chartFrame, text="📈 Charts & Reports", bg="#1a1a1a", 
                              fg="#ffffff", font=("Arial", 16, "bold"))
        chartTitle.pack(pady=10)

        # Create chart buttons
        dailyChartBtn = tk.Button(chartFrame, command=self.showDailyAttendanceChart,
                                 text="Daily Chart", bg="#4CAF50", fg="white",
                                 width=15, font=("Arial", 12, "bold"))
        dailyChartBtn.pack(pady=5)

        monthlyChartBtn = tk.Button(chartFrame, command=self.showMonthlyTrendChart,
                                   text="Monthly Trend", bg="#2196F3", fg="white",
                                   width=15, font=("Arial", 12, "bold"))
        monthlyChartBtn.pack(pady=5)

        studentChartBtn = tk.Button(chartFrame, command=self.showStudentSummaryChart,
                                   text="Student Summary", bg="#FF9800", fg="white",
                                   width=15, font=("Arial", 12, "bold"))
        studentChartBtn.pack(pady=5)

        subjectChartBtn = tk.Button(chartFrame, command=self.showSubjectComparisonChart,
                                   text="Subject Compare", bg="#9C27B0", fg="white",
                                   width=15, font=("Arial", 12, "bold"))
        subjectChartBtn.pack(pady=5)

        # detail Frame
        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#111111")
        self.detFrame.place(width=self.width/2+50, height=self.height-180, x=self.width/3+100, y=100)

        lbl = tk.Label(self.detFrame, text="Record Details", font=("Arial", 30, "bold"),
                       bg="#111111", fg="#ffffff")
        lbl.pack(side="top", fill="x")

        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="#1a1a1a")
        tabFrame.place(width=self.width/2, height=self.height-280, x=23, y=70)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("roll", "name", "fname", "sub"))
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("roll", text="Roll_No")
        self.table.heading("name", text="Name")
        self.table.heading("fname", text="L_Name")
        self.table.heading("sub", text="Subject")
        self.table["show"] = "headings"

        # Set column widths
        self.table.column("roll", width=100)
        self.table.column("name", width=150)
        self.table.column("fname", width=150)
        self.table.column("sub", width=200)

        self.table.pack(fill="both", expand=1)

    def dbFun(self):
        """Database connection with proper error handling"""
        try:
            self.con = pymysql.connect(host="localhost", user="root", passwd="haha", 
                                      database="student_attendance", charset='utf8mb4')
            self.cur = self.con.cursor()
            return True
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            return False

    def safe_int_conversion(self, value, field_name):
        """Safely convert string to integer with error handling"""
        try:
            return int(value)
        except ValueError:
            messagebox.showerror("Input Error", f"{field_name} must be a valid number!")
            return None

    def clear_table(self):
        """Clear all items from the table"""
        for item in self.table.get_children():
            self.table.delete(item)

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        if not self.dbFun():
            return False
        
        try:
            # Create students table
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    rollNo INT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    fname VARCHAR(100) NOT NULL,
                    sub VARCHAR(50) NOT NULL
                )
            """)
            
            # Create attendance table
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    rollNo INT,
                    date DATE NOT NULL,
                    status ENUM('Present', 'Absent') NOT NULL,
                    subject VARCHAR(50) NOT NULL,
                    FOREIGN KEY (rollNo) REFERENCES students(rollNo) ON DELETE CASCADE
                )
            """)
            
            self.con.commit()
            self.con.close()
            return True
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to create tables: {e}")
            return False

    def addFrameFun(self):
        # Clear any existing frame first
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.root, bd=5, relief="ridge", bg="#222222")
        self.current_frame.place(width=self.width/3, height=self.height-180, x=self.width/3+80, y=100)

        rnLbl = tk.Label(self.current_frame, text="Roll_No:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        rnLbl.grid(row=0, column=0, padx=20, pady=25)
        self.rollNo = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.rollNo.grid(row=0, column=1, padx=10, pady=25)

        nameLbl = tk.Label(self.current_frame, text="Name:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        nameLbl.grid(row=1, column=0, padx=20, pady=25)
        self.name = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.name.grid(row=1, column=1, padx=10, pady=25)

        fLbl = tk.Label(self.current_frame, text="LAST_NAME:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        fLbl.grid(row=2, column=0, padx=20, pady=25)
        self.fname = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.fname.grid(row=2, column=1, padx=10, pady=25)

        subLbl = tk.Label(self.current_frame, text="Subject:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        subLbl.grid(row=3, column=0, padx=20, pady=25)
        self.sub = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.sub.grid(row=3, column=1, padx=10, pady=25)

        okBtn = tk.Button(self.current_frame, command=self.addFun, text="Enter", bd=3, relief="raised",
                          font=("Arial", 20, "bold"), width=20, bg="#333333", fg="#ffffff")
        okBtn.grid(row=4, column=0, padx=30, pady=25, columnspan=2)
        cancelBtn = tk.Button(self.current_frame, text="Cancel", command=self.desAdd, bg="#444444", fg="#ffffff")
        cancelBtn.grid(row=5, column=0, padx=30, pady=10, columnspan=2)

    def desAdd(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()

    def addFun(self):
        rn = self.rollNo.get()
        name = self.name.get()
        fname = self.fname.get()
        sub = self.sub.get()

        if not all([rn, name, fname, sub]):
            messagebox.showerror("Error", "Please Fill All Input Fields!")
            return

        rNo = self.safe_int_conversion(rn, "Roll Number")
        if rNo is None:
            return

        if not self.dbFun():
            return

        try:
            # Check if roll number already exists
            self.cur.execute("SELECT * FROM students WHERE rollNo=%s", (rNo,))
            if self.cur.fetchone():
                messagebox.showerror("Error", f"Student with Roll No. {rNo} already exists!")
                return

            self.cur.execute("INSERT INTO students(rollNo,name,fname,sub) VALUES(%s,%s,%s,%s)",
                             (rNo, name, fname, sub))
            self.con.commit()
            messagebox.showinfo("Success", f"Student {name} with Roll_No.{rNo} is Registered!")
            self.desAdd()
            self.showAll()  # Refresh the table

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to add student: {e}")
        finally:
            self.con.close()

    def searchFrameFun(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.root, bd=5, relief="ridge", bg="#222222")
        self.current_frame.place(width=self.width/3, height=self.height-350, x=self.width/3+80, y=100)

        optLbl = tk.Label(self.current_frame, text="Select:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        optLbl.grid(row=0, column=0, padx=20, pady=25)
        self.option = ttk.Combobox(self.current_frame, width=17, values=("rollNo", "name", "sub"), font=("Arial", 15, "bold"))
        self.option.set("Select Option")
        self.option.grid(row=0, column=1, padx=10, pady=30)

        valLbl = tk.Label(self.current_frame, text="Value:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        valLbl.grid(row=1, column=0, padx=20, pady=25)
        self.value = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.value.grid(row=1, column=1, padx=10, pady=25)

        okBtn = tk.Button(self.current_frame, command=self.searchFun, text="Enter", bd=3, relief="raised",
                          font=("Arial", 20, "bold"), width=20, bg="#333333", fg="#ffffff")
        okBtn.grid(row=2, column=0, padx=30, pady=25, columnspan=2)

    def searchFun(self):
        opt = self.option.get()
        val = self.value.get()

        if opt == "Select Option" or not val:
            messagebox.showerror("Error", "Please select an option and enter a value!")
            return

        if not self.dbFun():
            return

        try:
            self.clear_table()
            
            if opt == "rollNo":
                rn = self.safe_int_conversion(val, "Roll Number")
                if rn is None:
                    return
                self.cur.execute("SELECT * FROM students WHERE rollNo=%s", (rn,))
                row = self.cur.fetchone()
                if row:
                    self.table.insert('', tk.END, values=row)
                else:
                    messagebox.showinfo("Not Found", "No student found with the given roll number.")
            else:
                allowed_columns = ["name", "sub"]
                if opt not in allowed_columns:
                    messagebox.showerror("Error", "Invalid search option!")
                    return
                    
                self.cur.execute(f"SELECT * FROM students WHERE {opt}=%s", (val,))
                data = self.cur.fetchall()
                if data:
                    for row in data:
                        self.table.insert('', tk.END, values=row)
                else:
                    messagebox.showinfo("Not Found", "No students found with the given criteria.")

            self.desAdd()

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Search failed: {e}")
        finally:
            self.con.close()

    def updFrameFun(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.root, bd=5, relief="ridge", bg="#000000")
        self.current_frame.place(width=self.width/3, height=self.height-300, x=self.width/3+80, y=100)

        optLbl = tk.Label(self.current_frame, text="Select:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        optLbl.grid(row=0, column=0, padx=20, pady=25)
        self.option = ttk.Combobox(self.current_frame, width=17, values=("name", "sub"), font=("Arial", 15, "bold"))
        self.option.set("Select Option")
        self.option.grid(row=0, column=1, padx=10, pady=30)

        valLbl = tk.Label(self.current_frame, text="New_Value:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        valLbl.grid(row=1, column=0, padx=20, pady=25)
        self.value = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.value.grid(row=1, column=1, padx=10, pady=25)

        rollLbl = tk.Label(self.current_frame, text="Roll_No:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        rollLbl.grid(row=2, column=0, padx=20, pady=25)
        self.roll = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.roll.grid(row=2, column=1, padx=10, pady=25)

        okBtn = tk.Button(self.current_frame, command=self.updFun, text="Enter", bd=3, relief="raised",
                          font=("Arial", 20, "bold"), width=20, bg="#333333", fg="#ffffff")
        okBtn.grid(row=3, column=0, padx=30, pady=25, columnspan=2)

    def updFun(self):
        opt = self.option.get()
        val = self.value.get()
        roll_text = self.roll.get()

        if opt == "Select Option" or not val or not roll_text:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        rNo = self.safe_int_conversion(roll_text, "Roll Number")
        if rNo is None:
            return

        if not self.dbFun():
            return

        try:
            # Check if student exists
            self.cur.execute("SELECT * FROM students WHERE rollNo=%s", (rNo,))
            if not self.cur.fetchone():
                messagebox.showerror("Error", f"Student with Roll No. {rNo} does not exist!")
                return

            allowed_columns = ["name", "sub"]
            if opt not in allowed_columns:
                messagebox.showerror("Error", "Invalid update option!")
                return

            self.cur.execute(f"UPDATE students SET {opt}=%s WHERE rollNo=%s", (val, rNo))
            self.con.commit()
            
            if self.cur.rowcount > 0:
                messagebox.showinfo("Success", f"Record updated for student with Roll No. {rNo}")
                self.desAdd()
                self.showAll()
            else:
                messagebox.showinfo("Info", "No changes were made.")

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Update failed: {e}")
        finally:
            self.con.close()

    def showAll(self):
        if not self.dbFun():
            return

        try:
            self.cur.execute("SELECT * FROM students")
            data = self.cur.fetchall()
            self.clear_table()

            for row in data:
                self.table.insert('', tk.END, values=row)

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to load data: {e}")
        finally:
            self.con.close()

    def delFrameFun(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.root, bd=5, relief="ridge", bg="#222222")
        self.current_frame.place(width=self.width/3, height=self.height-400, x=self.width/3+80, y=100)

        rnLbl = tk.Label(self.current_frame, text="Roll_No:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        rnLbl.grid(row=0, column=0, padx=20, pady=25)
        self.rollNo = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.rollNo.grid(row=0, column=1, padx=10, pady=25)

        okBtn = tk.Button(self.current_frame, command=self.delFun, text="Enter", bd=3, relief="raised",
                          font=("Arial", 20, "bold"), width=20, bg="#333333", fg="#ffffff")
        okBtn.grid(row=1, column=0, padx=30, pady=25, columnspan=2)

    def delFun(self):
        roll_text = self.rollNo.get()
        if not roll_text:
            messagebox.showerror("Error", "Please enter a roll number!")
            return

        rNo = self.safe_int_conversion(roll_text, "Roll Number")
        if rNo is None:
            return

        if not self.dbFun():
            return

        try:
            result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with Roll No. {rNo}?")
            if not result:
                return

            self.cur.execute("DELETE FROM students WHERE rollNo=%s", (rNo,))
            self.con.commit()
            
            if self.cur.rowcount > 0:
                messagebox.showinfo("Success", f"Student with Roll No. {rNo} has been removed")
                self.desAdd()
                self.showAll()
            else:
                messagebox.showinfo("Not Found", f"No student found with Roll No. {rNo}")

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Delete failed: {e}")
        finally:
            self.con.close()

    # ============ ATTENDANCE FUNCTIONS ============

    def markAttendanceFrameFun(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.root, bd=5, relief="ridge", bg="#222222")
        self.current_frame.place(width=self.width/3, height=self.height-300, x=self.width/3+80, y=100)

        current_date = date.today().strftime("%Y-%m-%d")

        dateLbl = tk.Label(self.current_frame, text="Date:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        dateLbl.grid(row=0, column=0, padx=20, pady=15)
        self.attn_date = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.attn_date.insert(0, current_date)
        self.attn_date.grid(row=0, column=1, padx=10, pady=15)

        subLbl = tk.Label(self.current_frame, text="Subject:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        subLbl.grid(row=1, column=0, padx=20, pady=15)
        self.attn_subject = ttk.Combobox(self.current_frame, width=16, 
                                        values=("Engineering Math", "DBMS", "DLCOA", "DSGT", "Computer ARCHITECTURE"), 
                                        font=("Arial", 15, "bold"))
        self.attn_subject.set("Select Subject")
        self.attn_subject.grid(row=1, column=1, padx=10, pady=15)

        self.create_attendance_table()

        okBtn = tk.Button(self.current_frame, command=self.markAttendanceFun, text="Save Attendance", bd=3, relief="raised",
                          font=("Arial", 16, "bold"), width=20, bg="#333333", fg="#ffffff")
        okBtn.grid(row=3, column=0, padx=30, pady=20, columnspan=2)

    def create_attendance_table(self):
        if not self.dbFun():
            return

        try:
            attn_table_frame = tk.Frame(self.current_frame, bd=4, relief="sunken", bg="#1a1a1a")
            attn_table_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

            scrollbar = tk.Scrollbar(attn_table_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.attn_table = ttk.Treeview(attn_table_frame, yscrollcommand=scrollbar.set,
                                          columns=("roll", "name", "status"), height=8)
            scrollbar.config(command=self.attn_table.yview)

            self.attn_table.heading("roll", text="Roll No")
            self.attn_table.heading("name", text="Name")
            self.attn_table.heading("status", text="Status")
            self.attn_table["show"] = "headings"

            self.attn_table.column("roll", width=80)
            self.attn_table.column("name", width=150)
            self.attn_table.column("status", width=100)

            self.attn_table.pack(fill="both", expand=1)

            self.cur.execute("SELECT rollNo, name FROM students ORDER BY rollNo")
            students = self.cur.fetchall()

            for student in students:
                roll_no, name = student
                self.attn_table.insert('', tk.END, values=(roll_no, name, "Present"), tags=('present',))

            self.attn_table.bind('<Double-1>', self.toggle_attendance_status)

            self.attn_table.tag_configure('present', background='#224422')
            self.attn_table.tag_configure('absent', background='#442222')

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to load students: {e}")
        finally:
            self.con.close()

    def toggle_attendance_status(self, event):
        item = self.attn_table.selection()[0]
        current_values = self.attn_table.item(item, 'values')
        
        if current_values[2] == "Present":
            self.attn_table.set(item, 'status', 'Absent')
            self.attn_table.item(item, tags=('absent',))
        else:
            self.attn_table.set(item, 'status', 'Present')
            self.attn_table.item(item, tags=('present',))

    def markAttendanceFun(self):
        date_val = self.attn_date.get()
        subject = self.attn_subject.get()

        if not date_val or subject == "Select Subject":
            messagebox.showerror("Error", "Please select date and subject!")
            return

        if not self.dbFun():
            return

        try:
            attendance_data = []
            for item in self.attn_table.get_children():
                values = self.attn_table.item(item, 'values')
                roll_no = int(values[0])
                status = values[2]
                attendance_data.append((roll_no, date_val, status, subject))

            for roll_no, date_val, status, subject in attendance_data:
                self.cur.execute("SELECT id FROM attendance WHERE rollNo=%s AND date=%s AND subject=%s", 
                               (roll_no, date_val, subject))
                existing = self.cur.fetchone()
                
                if existing:
                    self.cur.execute("UPDATE attendance SET status=%s WHERE rollNo=%s AND date=%s AND subject=%s",
                                   (status, roll_no, date_val, subject))
                else:
                    self.cur.execute("INSERT INTO attendance (rollNo, date, status, subject) VALUES (%s, %s, %s, %s)",
                                   (roll_no, date_val, status, subject))

            self.con.commit()
            messagebox.showinfo("Success", f"Attendance marked successfully for {date_val}!")
            self.desAdd()

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to save attendance: {e}")
        finally:
            self.con.close()

    def viewAttendanceFrameFun(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.root, bd=5, relief="ridge", bg="#222222")
        self.current_frame.place(width=self.width/3, height=self.height-300, x=self.width/3+80, y=100)

        searchLbl = tk.Label(self.current_frame, text="Search By:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        searchLbl.grid(row=0, column=0, padx=20, pady=15)
        self.attn_search_option = ttk.Combobox(self.current_frame, width=16, 
                                              values=("Roll No", "Date", "Subject", "All Records"), 
                                              font=("Arial", 15, "bold"))
        self.attn_search_option.set("Select Option")
        self.attn_search_option.grid(row=0, column=1, padx=10, pady=15)

        valueLbl = tk.Label(self.current_frame, text="Value:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        valueLbl.grid(row=1, column=0, padx=20, pady=15)
        self.attn_search_value = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.attn_search_value.grid(row=1, column=1, padx=10, pady=15)

        searchBtn = tk.Button(self.current_frame, command=self.viewAttendanceFun, text="Search", bd=3, relief="raised",
                             font=("Arial", 16, "bold"), width=20, bg="#333333", fg="#ffffff")
        searchBtn.grid(row=2, column=0, padx=30, pady=20, columnspan=2)

        self.attn_search_option.bind('<<ComboboxSelected>>', self.on_attn_search_option_change)

    def on_attn_search_option_change(self, event):
        if self.attn_search_option.get() == "All Records":
            self.attn_search_value.grid_remove()
        else:
            self.attn_search_value.grid()

    def viewAttendanceFun(self):
        search_option = self.attn_search_option.get()
        search_value = self.attn_search_value.get()

        if search_option == "Select Option":
            messagebox.showerror("Error", "Please select a search option!")
            return

        if search_option != "All Records" and not search_value:
            messagebox.showerror("Error", "Please enter a search value!")
            return

        if not self.dbFun():
            return

        try:
            self.clear_table()
            self.table.configure(columns=("roll", "name", "date", "subject", "status"))
            
            for col in self.table["columns"]:
                self.table.heading(col, text="")
                self.table.column(col, width=0)

            self.table.heading("roll", text="Roll No")
            self.table.heading("name", text="Name")
            self.table.heading("date", text="Date")
            self.table.heading("subject", text="Subject")
            self.table.heading("status", text="Status")

            self.table.column("roll", width=80)
            self.table.column("name", width=120)
            self.table.column("date", width=100)
            self.table.column("subject", width=100)
            self.table.column("status", width=80)

            if search_option == "All Records":
                query = """
                    SELECT s.rollNo, s.name, a.date, a.subject, a.status 
                    FROM attendance a 
                    JOIN students s ON a.rollNo = s.rollNo 
                    ORDER BY a.date DESC, s.rollNo
                """
                params = ()
            elif search_option == "Roll No":
                roll_no = self.safe_int_conversion(search_value, "Roll Number")
                if roll_no is None:
                    return
                query = """
                    SELECT s.rollNo, s.name, a.date, a.subject, a.status 
                    FROM attendance a 
                    JOIN students s ON a.rollNo = s.rollNo 
                    WHERE s.rollNo = %s 
                    ORDER BY a.date DESC
                """
                params = (roll_no,)
            elif search_option == "Date":
                query = """
                    SELECT s.rollNo, s.name, a.date, a.subject, a.status 
                    FROM attendance a 
                    JOIN students s ON a.rollNo = s.rollNo 
                    WHERE a.date = %s 
                    ORDER BY s.rollNo
                """
                params = (search_value,)
            elif search_option == "Subject":
                query = """
                    SELECT s.rollNo, s.name, a.date, a.subject, a.status 
                    FROM attendance a 
                    JOIN students s ON a.rollNo = s.rollNo 
                    WHERE a.subject = %s 
                    ORDER BY a.date DESC, s.rollNo
                """
                params = (search_value,)

            self.cur.execute(query, params)
            records = self.cur.fetchall()

            if records:
                for record in records:
                    self.table.insert('', tk.END, values=record)
                messagebox.showinfo("Success", f"Found {len(records)} attendance records!")
            else:
                messagebox.showinfo("No Records", "No attendance records found!")

            self.desAdd()

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch attendance records: {e}")
        finally:
            self.con.close()

    def attendanceCalculatorFrameFun(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.root, bd=5, relief="ridge", bg="#222222")
        self.current_frame.place(width=self.width/3, height=self.height-300, x=self.width/3+80, y=100)

        titleLbl = tk.Label(self.current_frame, text="Attendance Calculator", bg="#222222", fg="#ffffff", 
                           font=("Arial", 18, "bold"))
        titleLbl.grid(row=0, column=0, padx=20, pady=15, columnspan=2)

        rollLbl = tk.Label(self.current_frame, text="Roll No:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        rollLbl.grid(row=1, column=0, padx=20, pady=15)
        self.calc_roll = tk.Entry(self.current_frame, width=18, font=("Arial", 15, "bold"), bd=3)
        self.calc_roll.grid(row=1, column=1, padx=10, pady=15)

        subjectLbl = tk.Label(self.current_frame, text="Subject:", bg="#222222", fg="#ffffff", font=("Arial", 15, "bold"))
        subjectLbl.grid(row=2, column=0, padx=20, pady=15)
        self.calc_subject = ttk.Combobox(self.current_frame, width=16, 
                                        values=("Engineering Math", "DBMS", "DLCOA", "DSGT", "Computer ARCHITECTURE", "All Subjects"), 
                                        font=("Arial", 15, "bold"))
        self.calc_subject.set("Select Subject")
        self.calc_subject.grid(row=2, column=1, padx=10, pady=15)

        calculateBtn = tk.Button(self.current_frame, command=self.calculateAttendance, text="Calculate", bd=3, relief="raised",
                               font=("Arial", 16, "bold"), width=20, bg="#333333", fg="#ffffff")
        calculateBtn.grid(row=3, column=0, padx=30, pady=20, columnspan=2)

        self.result_label = tk.Label(self.current_frame, text="", bg="#222222", fg="#ffffff", 
                                    font=("Arial", 14, "bold"), wraplength=300)
        self.result_label.grid(row=4, column=0, padx=20, pady=15, columnspan=2)

    def calculateAttendance(self):
        roll_text = self.calc_roll.get()
        subject = self.calc_subject.get()

        if not roll_text or subject == "Select Subject":
            messagebox.showerror("Error", "Please enter roll number and select subject!")
            return

        rNo = self.safe_int_conversion(roll_text, "Roll Number")
        if rNo is None:
            return

        if not self.dbFun():
            return

        try:
            self.cur.execute("SELECT name FROM students WHERE rollNo=%s", (rNo,))
            student = self.cur.fetchone()
            if not student:
                messagebox.showerror("Error", f"Student with Roll No. {rNo} does not exist!")
                return

            student_name = student[0]

            if subject == "All Subjects":
                self.cur.execute("""
                    SELECT 
                        COUNT(*) as total_classes,
                        SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_classes
                    FROM attendance 
                    WHERE rollNo = %s
                """, (rNo,))
            else:
                self.cur.execute("""
                    SELECT 
                        COUNT(*) as total_classes,
                        SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_classes
                    FROM attendance 
                    WHERE rollNo = %s AND subject = %s
                """, (rNo, subject))

            result = self.cur.fetchone()
            total_classes = result[0]
            present_classes = result[1] if result[1] is not None else 0

            if total_classes == 0:
                self.result_label.config(text=f"No attendance records found for\nRoll No: {rNo}\nName: {student_name}")
                return

            attendance_percentage = (present_classes / total_classes) * 100

            if attendance_percentage >= 75:
                status = "GOOD ATTENDANCE ✅"
                color = "#00ff00"
            elif attendance_percentage >= 50:
                status = "AVERAGE ATTENDANCE ⚠️"
                color = "#ffff00"
            else:
                status = "LOW ATTENDANCE ❌"
                color = "#ff0000"

            result_text = (
                f"Roll No: {rNo}\n"
                f"Name: {student_name}\n"
                f"Subject: {subject}\n"
                f"Total Classes: {total_classes}\n"
                f"Present: {present_classes}\n"
                f"Absent: {total_classes - present_classes}\n"
                f"Attendance: {attendance_percentage:.2f}%\n"
                f"Status: {status}"
            )

            self.result_label.config(text=result_text, fg=color)

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to calculate attendance: {e}")
        finally:
            self.con.close()

    # ============ MATPLOTLIB CHART FUNCTIONS ============

    def showDailyAttendanceChart(self):
        """Show pie chart for today's attendance"""
        if not self.dbFun():
            return
        
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            query = """
                SELECT a.status, COUNT(*) as count, a.subject
                FROM attendance a
                WHERE a.date = %s
                GROUP BY a.status, a.subject
                ORDER BY a.subject, a.status
            """
            self.cur.execute(query, (today,))
            results = self.cur.fetchall()
            
            if not results:
                messagebox.showinfo("No Data", f"No attendance records for {today}")
                self.con.close()
                return
            
            chart_window = tk.Toplevel(self.root)
            chart_window.title(f"Daily Attendance - {today}")
            chart_window.geometry("900x700")
            chart_window.configure(bg="#222222")
            
            subjects = {}
            for status, count, subject in results:
                if subject not in subjects:
                    subjects[subject] = {'Present': 0, 'Absent': 0}
                subjects[subject][status] = count
            
            num_subjects = len(subjects)
            fig, axes = plt.subplots(1, num_subjects, figsize=(5*num_subjects, 5))
            if num_subjects == 1:
                axes = [axes]
            
            fig.patch.set_facecolor('#222222')
            
            colors = {'Present': '#4CAF50', 'Absent': '#F44336'}
            
            for idx, (subject, data) in enumerate(subjects.items()):
                labels = ['Present', 'Absent']
                sizes = [data.get('Present', 0), data.get('Absent', 0)]
                
                actual_labels = []
                actual_sizes = []
                actual_colors = []
                
                for i, (label, size) in enumerate(zip(labels, sizes)):
                    if size > 0:
                        actual_labels.append(f"{label}\n({size})")
                        actual_sizes.append(size)
                        actual_colors.append(colors[label])
                
                if actual_sizes:
                    axes[idx].pie(actual_sizes, labels=actual_labels, colors=actual_colors,
                                autopct='%1.1f%%', startangle=90, textprops={'color': 'white', 'fontsize': 10})
                    axes[idx].set_title(subject, color='white', fontsize=14, fontweight='bold')
                else:
                    axes[idx].text(0.5, 0.5, 'No Data', horizontalalignment='center',
                                 verticalalignment='center', color='white', fontsize=12)
                    axes[idx].set_title(subject, color='white', fontsize=14, fontweight='bold')
                
                axes[idx].set_facecolor('#222222')
            
            plt.suptitle(f"Daily Attendance - {today}", color='white', fontsize=16, fontweight='bold')
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            close_btn = tk.Button(chart_window, text="Close", command=chart_window.destroy,
                                bg="#333333", fg="white", font=("Arial", 12))
            close_btn.pack(pady=10)
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

    def showMonthlyTrendChart(self):
        """Show line chart of attendance trend over the month"""
        if not self.dbFun():
            return
        
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            query = """
                SELECT a.date, 
                       a.subject,
                       SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
                       COUNT(*) as total_count
                FROM attendance a
                WHERE MONTH(a.date) = %s AND YEAR(a.date) = %s
                GROUP BY a.date, a.subject
                ORDER BY a.date, a.subject
            """
            self.cur.execute(query, (current_month, current_year))
            results = self.cur.fetchall()
            
            if not results:
                messagebox.showinfo("No Data", f"No attendance records for {current_month}/{current_year}")
                self.con.close()
                return
            
            chart_window = tk.Toplevel(self.root)
            chart_window.title(f"Monthly Trend - {current_month}/{current_year}")
            chart_window.geometry("1000x700")
            chart_window.configure(bg="#222222")
            
            data_by_subject = {}
            dates = set()
            
            for date, subject, present, total in results:
                dates.add(date)
                if subject not in data_by_subject:
                    data_by_subject[subject] = {}
                percentage = (present / total * 100) if total > 0 else 0
                data_by_subject[subject][date] = percentage
            
            dates = sorted(list(dates))
            
            fig, ax = plt.subplots(figsize=(12, 7))
            fig.patch.set_facecolor('#222222')
            ax.set_facecolor('#222222')
            
            colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0']
            
            for idx, (subject, data) in enumerate(data_by_subject.items()):
                percentages = [data.get(date, 0) for date in dates]
                color = colors[idx % len(colors)]
                
                ax.plot(dates, percentages, marker='o', linewidth=2, label=subject, color=color)
                
                for date, percentage in zip(dates, percentages):
                    if percentage > 0:
                        ax.text(date, percentage + 1, f'{percentage:.1f}%', 
                               ha='center', va='bottom', fontsize=9, color=color)
            
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
            plt.xticks(rotation=45)
            
            ax.set_xlabel('Date', color='white', fontsize=12)
            ax.set_ylabel('Attendance Percentage (%)', color='white', fontsize=12)
            ax.set_title(f'Monthly Attendance Trend - {current_month}/{current_year}', 
                        color='white', fontsize=16, fontweight='bold')
            ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
            ax.grid(True, alpha=0.3, color='gray')
            ax.set_ylim(0, 105)
            
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            close_btn = tk.Button(chart_window, text="Close", command=chart_window.destroy,
                                bg="#333333", fg="white", font=("Arial", 12))
            close_btn.pack(pady=10)
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

    def showStudentSummaryChart(self):
        """Show bar chart of top students by attendance"""
        if not self.dbFun():
            return
        
        try:
            query = """
                SELECT s.rollNo, s.name, 
                       SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_days,
                       COUNT(a.id) as total_days
                FROM students s
                LEFT JOIN attendance a ON s.rollNo = a.rollNo
                GROUP BY s.rollNo, s.name
                HAVING total_days > 0
                ORDER BY (present_days/total_days) DESC
                LIMIT 10
            """
            self.cur.execute(query)
            results = self.cur.fetchall()
            
            if not results:
                messagebox.showinfo("No Data", "No attendance records found for students")
                self.con.close()
                return
            
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Top Students by Attendance")
            chart_window.geometry("1000x700")
            chart_window.configure(bg="#222222")
            
            students = []
            attendance_rates = []
            present_days_list = []
            total_days_list = []
            
            for roll_no, name, present_days, total_days in results:
                students.append(f"{name}\n(Roll: {roll_no})")
                rate = (present_days / total_days * 100) if total_days > 0 else 0
                attendance_rates.append(rate)
                present_days_list.append(present_days)
                total_days_list.append(total_days)
            
            fig, ax = plt.subplots(figsize=(12, 8))
            fig.patch.set_facecolor('#222222')
            ax.set_facecolor('#222222')
            
            bars = ax.barh(students, attendance_rates, color='#2196F3', height=0.6)
            
            for i, (bar, rate) in enumerate(zip(bars, attendance_rates)):
                if rate >= 75:
                    bar.set_color('#4CAF50')
                elif rate >= 50:
                    bar.set_color('#FF9800')
                else:
                    bar.set_color('#F44336')
            
            for i, (bar, rate, present, total) in enumerate(zip(bars, attendance_rates, present_days_list, total_days_list)):
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                       f'{rate:.1f}% ({present}/{total})', 
                       va='center', fontsize=10, color='white')
            
            ax.set_xlabel('Attendance Percentage (%)', color='white', fontsize=12)
            ax.set_title('Top 10 Students by Attendance Rate', 
                        color='white', fontsize=16, fontweight='bold')
            ax.set_xlim(0, 100)
            ax.grid(True, alpha=0.3, color='gray', axis='x')
            
            ax.tick_params(colors='white', labelsize=10)
            ax.set_yticklabels(students, color='white', fontsize=11)
            
            for spine in ax.spines.values():
                spine.set_color('white')
            
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='#4CAF50', label='≥ 75% (Good)'),
                Patch(facecolor='#FF9800', label='50-74% (Average)'),
                Patch(facecolor='#F44336', label='< 50% (Low)')
            ]
            ax.legend(handles=legend_elements, loc='upper right', 
                     facecolor='#333333', edgecolor='white', 
                     labelcolor='white', fontsize=10)
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            close_btn = tk.Button(chart_window, text="Close", command=chart_window.destroy,
                                bg="#333333", fg="white", font=("Arial", 12))
            close_btn.pack(pady=10)
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

    def showSubjectComparisonChart(self):
        """Compare attendance across different subjects"""
        if not self.dbFun():
            return
        
        try:
            query = """
                SELECT a.subject,
                       SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
                       COUNT(*) as total_count
                FROM attendance a
                GROUP BY a.subject
                ORDER BY a.subject
            """
            self.cur.execute(query)
            results = self.cur.fetchall()
            
            if not results:
                messagebox.showinfo("No Data", "No attendance records found")
                self.con.close()
                return
            
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Subject-wise Attendance Comparison")
            chart_window.geometry("900x600")
            chart_window.configure(bg="#222222")
            
            subjects = []
            present_counts = []
            total_counts = []
            percentages = []
            
            for subject, present, total in results:
                subjects.append(subject)
                present_counts.append(present)
                total_counts.append(total)
                percentages.append((present / total * 100) if total > 0 else 0)
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            fig.patch.set_facecolor('#222222')
            ax1.set_facecolor('#222222')
            ax2.set_facecolor('#222222')
            
            x = np.arange(len(subjects))
            width = 0.35
            
            bars1 = ax1.bar(x - width/2, present_counts, width, label='Present', color='#4CAF50')
            bars2 = ax1.bar(x + width/2, total_counts, width, label='Total', color='#2196F3', alpha=0.7)
            
            ax1.set_xlabel('Subjects', color='white')
            ax1.set_ylabel('Number of Classes', color='white')
            ax1.set_title('Attendance by Subject (Absolute)', color='white', fontweight='bold')
            ax1.set_xticks(x)
            ax1.set_xticklabels(subjects, rotation=45, ha='right', color='white')
            ax1.legend(facecolor='#333333', labelcolor='white')
            ax1.tick_params(colors='white')
            
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                            f'{int(height)}', ha='center', va='bottom', 
                            fontsize=9, color='white')
            
            colors = plt.cm.Set3(np.linspace(0, 1, len(subjects)))
            wedges, texts, autotexts = ax2.pie(percentages, labels=subjects, colors=colors,
                                              autopct='%1.1f%%', startangle=90)
            ax2.set_title('Attendance Percentage by Subject', color='white', fontweight='bold')
            
            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            close_btn = tk.Button(chart_window, text="Close", command=chart_window.destroy,
                                bg="#333333", fg="white", font=("Arial", 12))
            close_btn.pack(pady=10)
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentAttendanceSystem(root)
    
    app.create_tables()
    
    root.mainloop()