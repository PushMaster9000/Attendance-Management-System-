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

    # ============ VIEW ATTENDANCE WITH GRAPHS ============

    def viewAttendanceFrameFun(self):
        """View attendance with integrated graphs functionality"""
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
            
        # Create a larger frame for view attendance with graphs
        self.current_frame = tk.Frame(self.root, bd=5, relief="ridge", bg="#222222")
        self.current_frame.place(width=self.width/2+200, height=self.height-180, x=self.width/3+80, y=100)

        # Title
        titleLbl = tk.Label(self.current_frame, text="📊 View Attendance & Analytics", bg="#222222", 
                           fg="#ffffff", font=("Arial", 20, "bold"))
        titleLbl.pack(pady=10)

        # Search Frame
        search_frame = tk.Frame(self.current_frame, bg="#222222")
        search_frame.pack(pady=10)

        searchLbl = tk.Label(search_frame, text="Search By:", bg="#222222", fg="#ffffff", 
                            font=("Arial", 14, "bold"))
        searchLbl.grid(row=0, column=0, padx=10, pady=5)
        
        self.attn_search_option = ttk.Combobox(search_frame, width=15, 
                                              values=("Roll No", "Date", "Subject", "All Records"), 
                                              font=("Arial", 12))
        self.attn_search_option.set("Select Option")
        self.attn_search_option.grid(row=0, column=1, padx=10, pady=5)

        valueLbl = tk.Label(search_frame, text="Value:", bg="#222222", fg="#ffffff", 
                           font=("Arial", 14, "bold"))
        valueLbl.grid(row=0, column=2, padx=10, pady=5)
        
        self.attn_search_value = tk.Entry(search_frame, width=20, font=("Arial", 12), bd=2)
        self.attn_search_value.grid(row=0, column=3, padx=10, pady=5)

        searchBtn = tk.Button(search_frame, command=self.viewAttendanceWithGraphs, 
                             text="Search & Show Graphs", bd=3, relief="raised",
                             font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
        searchBtn.grid(row=0, column=4, padx=20, pady=5)

        # Bind combobox selection
        self.attn_search_option.bind('<<ComboboxSelected>>', self.on_attn_search_option_change)

        # Quick Graph Buttons Frame
        quick_graph_frame = tk.Frame(self.current_frame, bg="#222222")
        quick_graph_frame.pack(pady=10)

        # Quick graph buttons
        dailyBtn = tk.Button(quick_graph_frame, command=self.showDailyChart, 
                            text="📅 Today's Attendance", bg="#2196F3", fg="white",
                            font=("Arial", 11), width=20)
        dailyBtn.grid(row=0, column=0, padx=5, pady=5)

        monthlyBtn = tk.Button(quick_graph_frame, command=self.showMonthlyChart,
                              text="📈 Monthly Trend", bg="#FF9800", fg="white",
                              font=("Arial", 11), width=20)
        monthlyBtn.grid(row=0, column=1, padx=5, pady=5)

        studentBtn = tk.Button(quick_graph_frame, command=self.showStudentChart,
                              text="👥 Student Ranking", bg="#4CAF50", fg="white",
                              font=("Arial", 11), width=20)
        studentBtn.grid(row=0, column=2, padx=5, pady=5)

        subjectBtn = tk.Button(quick_graph_frame, command=self.showSubjectChart,
                              text="📚 Subject Comparison", bg="#9C27B0", fg="white",
                              font=("Arial", 11), width=20)
        subjectBtn.grid(row=0, column=3, padx=5, pady=5)

        # Results display area (for table and graphs)
        results_frame = tk.Frame(self.current_frame, bg="#222222")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Notebook for tabbed interface
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Table View
        self.table_tab = tk.Frame(self.results_notebook, bg="#1a1a1a")
        self.results_notebook.add(self.table_tab, text="📋 Table View")
        
        # Create table in table tab
        table_container = tk.Frame(self.table_tab, bg="#1a1a1a")
        table_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar_y = tk.Scrollbar(table_container)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(table_container, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.attendance_table = ttk.Treeview(table_container, 
                                            yscrollcommand=scrollbar_y.set,
                                            xscrollcommand=scrollbar_x.set,
                                            columns=("roll", "name", "date", "subject", "status"),
                                            height=15)
        scrollbar_y.config(command=self.attendance_table.yview)
        scrollbar_x.config(command=self.attendance_table.xview)
        
        self.attendance_table.heading("roll", text="Roll No")
        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("subject", text="Subject")
        self.attendance_table.heading("status", text="Status")
        
        self.attendance_table.column("roll", width=80)
        self.attendance_table.column("name", width=150)
        self.attendance_table.column("date", width=100)
        self.attendance_table.column("subject", width=150)
        self.attendance_table.column("status", width=80)
        
        self.attendance_table.pack(fill=tk.BOTH, expand=True)

        # Tab 2: Graph View
        self.graph_tab = tk.Frame(self.results_notebook, bg="#1a1a1a")
        self.results_notebook.add(self.graph_tab, text="📊 Graph View")

        # Graph type selection
        graph_select_frame = tk.Frame(self.graph_tab, bg="#1a1a1a")
        graph_select_frame.pack(pady=10)

        graphLbl = tk.Label(graph_select_frame, text="Select Graph Type:", bg="#1a1a1a", 
                           fg="#ffffff", font=("Arial", 12))
        graphLbl.grid(row=0, column=0, padx=10, pady=5)
        
        self.graph_type = ttk.Combobox(graph_select_frame, width=20,
                                      values=("Daily Pie Chart", "Monthly Trend", 
                                              "Student Ranking", "Subject Comparison"),
                                      font=("Arial", 11))
        self.graph_type.set("Daily Pie Chart")
        self.graph_type.grid(row=0, column=1, padx=10, pady=5)
        
        refreshBtn = tk.Button(graph_select_frame, command=self.refreshGraph,
                              text="Refresh Graph", bg="#2196F3", fg="white",
                              font=("Arial", 11))
        refreshBtn.grid(row=0, column=2, padx=10, pady=5)

        # Graph display frame
        self.graph_display_frame = tk.Frame(self.graph_tab, bg="#1a1a1a")
        self.graph_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def on_attn_search_option_change(self, event):
        if self.attn_search_option.get() == "All Records":
            self.attn_search_value.grid_remove()
        else:
            self.attn_search_value.grid()

    def viewAttendanceWithGraphs(self):
        """Search attendance and display results with graphs"""
        search_option = self.attn_search_option.get()
        search_value = self.attn_search_value.get()

        if search_option == "Select Option":
            messagebox.showerror("Error", "Please select a search option!")
            return

        if search_option != "All Records" and not search_value:
            messagebox.showerror("Error", "Please enter a search value!")
            return

        # Store search parameters for graph generation
        self.current_search_option = search_option
        self.current_search_value = search_value

        # Load data into table
        self.loadAttendanceTable(search_option, search_value)
        
        # Show default graph
        self.showDefaultGraph()

    def loadAttendanceTable(self, search_option, search_value):
        """Load attendance data into the table"""
        if not self.dbFun():
            return

        try:
            # Clear existing data
            for item in self.attendance_table.get_children():
                self.attendance_table.delete(item)

            # Build query based on search option
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
                    self.attendance_table.insert('', tk.END, values=record)
                
                # Update status label
                if hasattr(self, 'status_label'):
                    self.status_label.config(text=f"Found {len(records)} records")
                
                # Store records for graphs
                self.current_records = records
            else:
                messagebox.showinfo("No Records", "No attendance records found!")

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch attendance records: {e}")
        finally:
            self.con.close()

    def showDefaultGraph(self):
        """Show default graph based on current search"""
        if hasattr(self, 'current_search_option'):
            if self.current_search_option == "Date":
                self.displayDailyPieChart()
            elif self.current_search_option == "Roll No":
                self.displayStudentAttendanceChart()
            elif self.current_search_option == "Subject":
                self.displaySubjectAttendanceChart()
            else:
                self.displayMonthlyTrendChart()

    def refreshGraph(self):
        """Refresh graph based on selected type"""
        graph_type = self.graph_type.get()
        
        if graph_type == "Daily Pie Chart":
            self.displayDailyPieChart()
        elif graph_type == "Monthly Trend":
            self.displayMonthlyTrendChart()
        elif graph_type == "Student Ranking":
            self.displayStudentRankingChart()
        elif graph_type == "Subject Comparison":
            self.displaySubjectComparisonChart()

    # ============ QUICK GRAPH BUTTON FUNCTIONS ============

    def showDailyChart(self):
        """Show daily attendance chart"""
        self.graph_type.set("Daily Pie Chart")
        self.displayDailyPieChart()

    def showMonthlyChart(self):
        """Show monthly trend chart"""
        self.graph_type.set("Monthly Trend")
        self.displayMonthlyTrendChart()

    def showStudentChart(self):
        """Show student ranking chart"""
        self.graph_type.set("Student Ranking")
        self.displayStudentRankingChart()

    def showSubjectChart(self):
        """Show subject comparison chart"""
        self.graph_type.set("Subject Comparison")
        self.displaySubjectComparisonChart()

    # ============ GRAPH DISPLAY FUNCTIONS ============

    def displayDailyPieChart(self):
        """Display daily attendance pie chart"""
        if not self.dbFun():
            return
        
        try:
            # Clear previous graph
            for widget in self.graph_display_frame.winfo_children():
                widget.destroy()
            
            # Get today's date or use search value if searching by date
            if hasattr(self, 'current_search_option') and self.current_search_option == "Date":
                date_val = self.current_search_value
            else:
                date_val = datetime.now().strftime('%Y-%m-%d')
            
            # Query for daily attendance
            query = """
                SELECT a.status, COUNT(*) as count, a.subject
                FROM attendance a
                WHERE a.date = %s
                GROUP BY a.status, a.subject
                ORDER BY a.subject, a.status
            """
            self.cur.execute(query, (date_val,))
            results = self.cur.fetchall()
            
            if not results:
                no_data_label = tk.Label(self.graph_display_frame, 
                                        text=f"No attendance records for {date_val}",
                                        bg="#1a1a1a", fg="#ffffff", font=("Arial", 14))
                no_data_label.pack(expand=True)
                return
            
            # Prepare data
            subjects = {}
            for status, count, subject in results:
                if subject not in subjects:
                    subjects[subject] = {'Present': 0, 'Absent': 0}
                subjects[subject][status] = count
            
            # Create figure
            num_subjects = len(subjects)
            fig, axes = plt.subplots(1, num_subjects, figsize=(5*num_subjects, 5))
            if num_subjects == 1:
                axes = [axes]
            
            fig.patch.set_facecolor('#1a1a1a')
            
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
                                autopct='%1.1f%%', startangle=90, 
                                textprops={'color': 'white', 'fontsize': 9})
                    axes[idx].set_title(subject, color='white', fontsize=12, fontweight='bold')
                else:
                    axes[idx].text(0.5, 0.5, 'No Data', horizontalalignment='center',
                                 verticalalignment='center', color='white', fontsize=10)
                    axes[idx].set_title(subject, color='white', fontsize=12, fontweight='bold')
                
                axes[idx].set_facecolor('#1a1a1a')
            
            plt.suptitle(f"Daily Attendance - {date_val}", color='white', fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            # Embed in Tkinter frame
            canvas = FigureCanvasTkAgg(fig, master=self.graph_display_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add navigation to notebook
            self.results_notebook.select(1)  # Switch to graph tab
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

    def displayMonthlyTrendChart(self):
        """Display monthly attendance trend chart"""
        if not self.dbFun():
            return
        
        try:
            # Clear previous graph
            for widget in self.graph_display_frame.winfo_children():
                widget.destroy()
            
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Query for monthly data
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
                no_data_label = tk.Label(self.graph_display_frame, 
                                        text=f"No attendance records for {current_month}/{current_year}",
                                        bg="#1a1a1a", fg="#ffffff", font=("Arial", 14))
                no_data_label.pack(expand=True)
                return
            
            # Prepare data
            data_by_subject = {}
            dates = set()
            
            for date, subject, present, total in results:
                dates.add(date)
                if subject not in data_by_subject:
                    data_by_subject[subject] = {}
                percentage = (present / total * 100) if total > 0 else 0
                data_by_subject[subject][date] = percentage
            
            dates = sorted(list(dates))
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#1a1a1a')
            ax.set_facecolor('#1a1a1a')
            
            colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0']
            
            for idx, (subject, data) in enumerate(data_by_subject.items()):
                percentages = [data.get(date, 0) for date in dates]
                color = colors[idx % len(colors)]
                
                ax.plot(dates, percentages, marker='o', linewidth=2, label=subject, color=color)
                
                for date, percentage in zip(dates, percentages):
                    if percentage > 0:
                        ax.text(date, percentage + 1, f'{percentage:.1f}%', 
                               ha='center', va='bottom', fontsize=8, color=color)
            
            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
            plt.xticks(rotation=45)
            
            # Customize
            ax.set_xlabel('Date', color='white', fontsize=11)
            ax.set_ylabel('Attendance Percentage (%)', color='white', fontsize=11)
            ax.set_title(f'Monthly Attendance Trend - {current_month}/{current_year}', 
                        color='white', fontsize=14, fontweight='bold')
            ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white', fontsize=9)
            ax.grid(True, alpha=0.3, color='gray')
            ax.set_ylim(0, 105)
            
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')
            
            plt.tight_layout()
            
            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_display_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.results_notebook.select(1)
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

    def displayStudentRankingChart(self):
        """Display student ranking chart"""
        if not self.dbFun():
            return
        
        try:
            # Clear previous graph
            for widget in self.graph_display_frame.winfo_children():
                widget.destroy()
            
            # Query for student ranking
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
                no_data_label = tk.Label(self.graph_display_frame, 
                                        text="No attendance records found for students",
                                        bg="#1a1a1a", fg="#ffffff", font=("Arial", 14))
                no_data_label.pack(expand=True)
                return
            
            # Prepare data
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
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 7))
            fig.patch.set_facecolor('#1a1a1a')
            ax.set_facecolor('#1a1a1a')
            
            bars = ax.barh(students, attendance_rates, color='#2196F3', height=0.6)
            
            # Color code bars
            for i, (bar, rate) in enumerate(zip(bars, attendance_rates)):
                if rate >= 75:
                    bar.set_color('#4CAF50')
                elif rate >= 50:
                    bar.set_color('#FF9800')
                else:
                    bar.set_color('#F44336')
            
            # Add value labels
            for i, (bar, rate, present, total) in enumerate(zip(bars, attendance_rates, present_days_list, total_days_list)):
                width = bar.get_width()
                ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                       f'{rate:.1f}% ({present}/{total})', 
                       va='center', fontsize=9, color='white')
            
            # Customize
            ax.set_xlabel('Attendance Percentage (%)', color='white', fontsize=11)
            ax.set_title('Top 10 Students by Attendance Rate', 
                        color='white', fontsize=14, fontweight='bold')
            ax.set_xlim(0, 100)
            ax.grid(True, alpha=0.3, color='gray', axis='x')
            
            ax.tick_params(colors='white', labelsize=9)
            ax.set_yticklabels(students, color='white', fontsize=10)
            
            for spine in ax.spines.values():
                spine.set_color('white')
            
            # Add legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='#4CAF50', label='≥ 75% (Good)'),
                Patch(facecolor='#FF9800', label='50-74% (Average)'),
                Patch(facecolor='#F44336', label='< 50% (Low)')
            ]
            ax.legend(handles=legend_elements, loc='lower right', 
                     facecolor='#333333', edgecolor='white', 
                     labelcolor='white', fontsize=9)
            
            plt.tight_layout()
            
            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_display_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.results_notebook.select(1)
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

    def displaySubjectComparisonChart(self):
        """Display subject comparison chart"""
        if not self.dbFun():
            return
        
        try:
            # Clear previous graph
            for widget in self.graph_display_frame.winfo_children():
                widget.destroy()
            
            # Query for subject data
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
                no_data_label = tk.Label(self.graph_display_frame, 
                                        text="No attendance records found",
                                        bg="#1a1a1a", fg="#ffffff", font=("Arial", 14))
                no_data_label.pack(expand=True)
                return
            
            # Prepare data
            subjects = []
            present_counts = []
            total_counts = []
            percentages = []
            
            for subject, present, total in results:
                subjects.append(subject)
                present_counts.append(present)
                total_counts.append(total)
                percentages.append((present / total * 100) if total > 0 else 0)
            
            # Create figure with two subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            fig.patch.set_facecolor('#1a1a1a')
            ax1.set_facecolor('#1a1a1a')
            ax2.set_facecolor('#1a1a1a')
            
            # Bar chart
            x = np.arange(len(subjects))
            width = 0.35
            
            bars1 = ax1.bar(x - width/2, present_counts, width, label='Present', color='#4CAF50')
            bars2 = ax1.bar(x + width/2, total_counts, width, label='Total', color='#2196F3', alpha=0.7)
            
            ax1.set_xlabel('Subjects', color='white', fontsize=10)
            ax1.set_ylabel('Number of Classes', color='white', fontsize=10)
            ax1.set_title('Attendance by Subject', color='white', fontsize=12, fontweight='bold')
            ax1.set_xticks(x)
            ax1.set_xticklabels(subjects, rotation=45, ha='right', color='white', fontsize=9)
            ax1.legend(facecolor='#333333', labelcolor='white', fontsize=9)
            ax1.tick_params(colors='white')
            
            # Add value labels
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                            f'{int(height)}', ha='center', va='bottom', 
                            fontsize=8, color='white')
            
            # Pie chart
            colors = plt.cm.Set3(np.linspace(0, 1, len(subjects)))
            wedges, texts, autotexts = ax2.pie(percentages, labels=subjects, colors=colors,
                                              autopct='%1.1f%%', startangle=90, 
                                              textprops={'fontsize': 8})
            ax2.set_title('Attendance Percentage', color='white', fontsize=12, fontweight='bold')
            
            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.tight_layout()
            
            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_display_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.results_notebook.select(1)
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

    def displayStudentAttendanceChart(self):
        """Display individual student attendance chart"""
        if not self.dbFun() or not hasattr(self, 'current_search_value'):
            return
        
        try:
            # Clear previous graph
            for widget in self.graph_display_frame.winfo_children():
                widget.destroy()
            
            roll_no = self.safe_int_conversion(self.current_search_value, "Roll Number")
            if roll_no is None:
                return
            
            # Get student info
            self.cur.execute("SELECT name FROM students WHERE rollNo=%s", (roll_no,))
            student = self.cur.fetchone()
            if not student:
                no_data_label = tk.Label(self.graph_display_frame, 
                                        text=f"Student with Roll No {roll_no} not found",
                                        bg="#1a1a1a", fg="#ffffff", font=("Arial", 14))
                no_data_label.pack(expand=True)
                return
            
            student_name = student[0]
            
            # Get attendance by subject
            query = """
                SELECT a.subject,
                       SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
                       COUNT(*) as total_count
                FROM attendance a
                WHERE a.rollNo = %s
                GROUP BY a.subject
                ORDER BY a.subject
            """
            self.cur.execute(query, (roll_no,))
            results = self.cur.fetchall()
            
            if not results:
                no_data_label = tk.Label(self.graph_display_frame, 
                                        text=f"No attendance records for {student_name}",
                                        bg="#1a1a1a", fg="#ffffff", font=("Arial", 14))
                no_data_label.pack(expand=True)
                return
            
            # Prepare data
            subjects = []
            present_counts = []
            total_counts = []
            percentages = []
            
            for subject, present, total in results:
                subjects.append(subject)
                present_counts.append(present)
                total_counts.append(total)
                percentages.append((present / total * 100) if total > 0 else 0)
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#1a1a1a')
            ax.set_facecolor('#1a1a1a')
            
            # Color bars based on percentage
            bar_colors = []
            for percentage in percentages:
                if percentage >= 75:
                    bar_colors.append('#4CAF50')
                elif percentage >= 50:
                    bar_colors.append('#FF9800')
                else:
                    bar_colors.append('#F44336')
            
            bars = ax.bar(subjects, percentages, color=bar_colors, width=0.6)
            
            # Add value labels
            for bar, percentage, present, total in zip(bars, percentages, present_counts, total_counts):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{percentage:.1f}%\n({present}/{total})', 
                       ha='center', va='bottom', fontsize=9, color='white')
            
            # Customize
            ax.set_xlabel('Subjects', color='white', fontsize=11)
            ax.set_ylabel('Attendance Percentage (%)', color='white', fontsize=11)
            ax.set_title(f'Attendance for {student_name} (Roll No: {roll_no})', 
                        color='white', fontsize=14, fontweight='bold')
            ax.set_ylim(0, 105)
            ax.grid(True, alpha=0.3, color='gray', axis='y')
            
            ax.tick_params(colors='white', labelsize=9)
            ax.set_xticklabels(subjects, rotation=45, ha='right', color='white')
            
            for spine in ax.spines.values():
                spine.set_color('white')
            
            plt.tight_layout()
            
            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_display_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.results_notebook.select(1)
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

    def displaySubjectAttendanceChart(self):
        """Display attendance chart for specific subject"""
        if not self.dbFun() or not hasattr(self, 'current_search_value'):
            return
        
        try:
            # Clear previous graph
            for widget in self.graph_display_frame.winfo_children():
                widget.destroy()
            
            subject = self.current_search_value
            
            # Get attendance by date for this subject
            query = """
                SELECT a.date,
                       SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
                       COUNT(*) as total_count
                FROM attendance a
                WHERE a.subject = %s
                GROUP BY a.date
                ORDER BY a.date
            """
            self.cur.execute(query, (subject,))
            results = self.cur.fetchall()
            
            if not results:
                no_data_label = tk.Label(self.graph_display_frame, 
                                        text=f"No attendance records for {subject}",
                                        bg="#1a1a1a", fg="#ffffff", font=("Arial", 14))
                no_data_label.pack(expand=True)
                return
            
            # Prepare data
            dates = []
            percentages = []
            present_counts = []
            total_counts = []
            
            for date_val, present, total in results:
                dates.append(date_val)
                present_counts.append(present)
                total_counts.append(total)
                percentage = (present / total * 100) if total > 0 else 0
                percentages.append(percentage)
            
            # Create figure
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            fig.patch.set_facecolor('#1a1a1a')
            ax1.set_facecolor('#1a1a1a')
            ax2.set_facecolor('#1a1a1a')
            
            # Line chart for trend
            ax1.plot(dates, percentages, marker='o', linewidth=2, color='#2196F3')
            ax1.set_xlabel('Date', color='white', fontsize=10)
            ax1.set_ylabel('Attendance %', color='white', fontsize=10)
            ax1.set_title(f'{subject} - Attendance Trend', color='white', fontsize=12, fontweight='bold')
            ax1.grid(True, alpha=0.3, color='gray')
            ax1.set_ylim(0, 105)
            
            # Format x-axis
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            # Bar chart for daily attendance
            x = np.arange(len(dates))
            width = 0.35
            
            bars1 = ax2.bar(x - width/2, present_counts, width, label='Present', color='#4CAF50')
            bars2 = ax2.bar(x + width/2, total_counts, width, label='Total', color='#2196F3', alpha=0.7)
            
            ax2.set_xlabel('Date', color='white', fontsize=10)
            ax2.set_ylabel('Number of Students', color='white', fontsize=10)
            ax2.set_title(f'{subject} - Daily Attendance', color='white', fontsize=12, fontweight='bold')
            ax2.set_xticks(x)
            ax2.set_xticklabels([d.strftime('%d-%b') for d in dates], rotation=45, ha='right', color='white', fontsize=8)
            ax2.legend(facecolor='#333333', labelcolor='white', fontsize=9)
            
            ax1.tick_params(colors='white')
            ax2.tick_params(colors='white')
            
            for spine in ax1.spines.values():
                spine.set_color('white')
            for spine in ax2.spines.values():
                spine.set_color('white')
            
            plt.tight_layout()
            
            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_display_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.results_notebook.select(1)
            
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
        finally:
            self.con.close()

    # ============ ATTENDANCE CALCULATOR ============

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

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentAttendanceSystem(root)
    
    app.create_tables()
    
    root.mainloop()