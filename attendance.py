import os
import mysql.connector
import cv2
import numpy as np
import csv
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime

# Global variable for importCsv function
mydata = []

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Attendance Panel")

        # Variables
        self.var_id = StringVar()
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_subject = StringVar()
        self.var_dep = StringVar()
        self.var_time = StringVar()
        self.var_date = StringVar()
        self.var_attend = StringVar()

        # Image Setup
        self._setup_images()

        # UI Setup
        self._create_ui()

    def _setup_images(self):
        # Header Image
        img = Image.open(r"Images_GUI\banner1.jpg")
        img = img.resize((1366, 130), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # Background Image
        bg1 = Image.open(r"Images_GUI\bg3.jpg")
        bg1 = bg1.resize((1366, 768), Image.ANTIALIAS)
        self.photobg1 = ImageTk.PhotoImage(bg1)
        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

    def _create_ui(self):
        # Title Section
        title_lb1 = Label(self.root, text="Attendance Panel", font=("Verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Frame Section
        frame = Frame(self.root, bd=2, bg="white")
        frame.place(x=5, y=55, width=1355, height=575)

        # Left Frame Section for Student Details
        left_frame = LabelFrame(frame, bd=2, bg="white", relief=RIDGE, text="Student Attendance Details", font=("Verdana", 12, "bold"), fg="black")
        left_frame.place(x=10, y=160, width=660, height=405)

        # Student Fields (ID, Roll, Name, Course, Subject, etc.)
        self._create_student_fields(left_frame)

        # Button Section
        self._create_buttons(left_frame)

        # Table for Attendance Records
        self._create_table(frame)

    def _create_student_fields(self, parent_frame):
        # Student ID
        student_id_label = Label(parent_frame, text="StdID:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        student_id_label.grid(row=0, column=0, padx=5, pady=12, sticky=W)
        student_id_entry = ttk.Entry(parent_frame, textvariable=self.var_id, width=15, font=("Verdana", 12))
        student_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Student Roll
        student_roll_label = Label(parent_frame, text="Roll.No:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        student_roll_label.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        student_roll_entry = ttk.Entry(parent_frame, textvariable=self.var_roll, width=15, font=("Verdana", 12))
        student_roll_entry.grid(row=0, column=3, padx=5, pady=5, sticky=W)

        # Other Student Details (Name, Course, Subject, Time, Date, Attendance Status)
        student_name_label = Label(parent_frame, text="StdName:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        student_name_label.grid(row=1, column=0, padx=5, pady=12, sticky=W)
        student_name_entry = ttk.Entry(parent_frame, textvariable=self.var_name, width=15, font=("Verdana", 12))
        student_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        course_label = Label(parent_frame, text="Course:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        course_label.grid(row=1, column=2, padx=5, pady=5, sticky=W)
        course_entry = ttk.Entry(parent_frame, textvariable=self.var_course, width=15, font=("Verdana", 12))
        course_entry.grid(row=1, column=3, padx=5, pady=5, sticky=W)

        subject_label = Label(parent_frame, text="Subject:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        subject_label.grid(row=2, column=0, padx=5, pady=12, sticky=W)
        subject_entry = ttk.Entry(parent_frame, textvariable=self.var_subject, width=15, font=("Verdana", 12))
        subject_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        time_label = Label(parent_frame, text="Time:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        time_label.grid(row=2, column=2, padx=5, pady=5, sticky=W)
        time_entry = ttk.Entry(parent_frame, textvariable=self.var_time, width=15, font=("Verdana", 12))
        time_entry.grid(row=2, column=3, padx=5, pady=5, sticky=W)

        date_label = Label(parent_frame, text="Date:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        date_label.grid(row=3, column=0, padx=5, pady=12, sticky=W)
        date_entry = ttk.Entry(parent_frame, textvariable=self.var_date, width=15, font=("Verdana", 12))
        date_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        # Attendance Status
        attend_label = Label(parent_frame, text="Attend Status:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        attend_label.grid(row=3, column=2, padx=5, pady=5, sticky=W)
        attend_combo = ttk.Combobox(parent_frame, textvariable=self.var_attend, width=13, font=("Verdana", 12), state="readonly")
        attend_combo["values"] = ("Status", "Present", "Absent", "Half Day", "Bunk Lecture")
        attend_combo.current(0)
        attend_combo.grid(row=3, column=3, padx=5, pady=5, sticky=W)

    def _create_buttons(self, parent_frame):
        # Button Frame for Import/Export/Reset
        btn_frame = Frame(parent_frame, bg="white", relief=RIDGE)
        btn_frame.place(x=10, y=260, width=635, height=60)

        # Import CSV Button
        import_btn = Button(btn_frame, command=self.import_csv, text="Import CSV", width=12, font=("Verdana", 12, "bold"), fg="white", bg="navyblue")
        import_btn.grid(row=0, column=0, padx=6, pady=10, sticky=W)

        # Export CSV Button
        export_btn = Button(btn_frame, command=self.export_csv, text="Export CSV", width=12, font=("Verdana", 12, "bold"), fg="white", bg="navyblue")
        export_btn.grid(row=0, column=1, padx=6, pady=10, sticky=W)

        # Update Button
        update_btn = Button(btn_frame, command=self.update_csv, text="Update", width=12, font=("Verdana", 12, "bold"), fg="white", bg="navyblue")
        update_btn.grid(row=0, column=2, padx=6, pady=10, sticky=W)

        # Reset Button
        reset_btn = Button(btn_frame, command=self.reset_data, text="Reset", width=12, font=("Verdana", 12, "bold"), fg="white", bg="navyblue")
        reset_btn.grid(row=0, column=3, padx=6, pady=10, sticky=W)

    def _create_table(self, frame):
        # Right Frame for Attendance Details
        right_frame = LabelFrame(frame, bd=2, bg="white", relief=RIDGE, text="Attendance Details", font=("Verdana", 12, "bold"), fg="black")
        right_frame.place(x=680, y=10, width=660, height=555)

        # Table Frame for Searching System
        table_frame = Frame(right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=10, y=10, width=635, height=510)

        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # Create table
        self.attendanceReport = ttk.Treeview(table_frame, column=("ID", "Roll_No", "Name", "Course", "Subject", "Time", "Date", "Attend"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.attendanceReport.xview)
        scroll_y.config(command=self.attendanceReport.yview)

        # Column Headings
        self.attendanceReport.heading("ID", text="Std-ID")
        self.attendanceReport.heading("Roll_No", text="Roll.No")
        self.attendanceReport.heading("Name", text="Std-Name")
        self.attendanceReport.heading("Course", text="Course")
        self.attendanceReport.heading("Subject", text="Subject")
        self.attendanceReport.heading("Time", text="Time")
        self.attendanceReport.heading("Date", text="Date")
        self.attendanceReport.heading("Attend", text="Attend-status")
        self.attendanceReport["show"] = "headings"

        # Set Column Widths
        self.attendanceReport.column("ID", width=100, anchor=CENTER)
        self.attendanceReport.column("Roll_No", width=100, anchor=CENTER)
        self.attendanceReport.column("Name", width=100, anchor=CENTER)
        self.attendanceReport.column("Course", width=100, anchor=CENTER)
        self.attendanceReport.column("Subject", width=100, anchor=CENTER)
        self.attendanceReport.column("Time", width=100, anchor=CENTER)
        self.attendanceReport.column("Date", width=100, anchor=CENTER)
        self.attendanceReport.column("Attend", width=100, anchor=CENTER)

        self.attendanceReport.pack(fill=BOTH, expand=1)
        self.attendanceReport.bind("<ButtonRelease>", self.get_cursor)

    def import_csv(self):
        global mydata
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")), parent=self.root)
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata.append(i)
        self.fetch_data(mydata)

    def fetch_data(self, rows):
        global mydata
        mydata = rows
        self.attendanceReport.delete(*self.attendanceReport.get_children())
        for i in rows:
            self.attendanceReport.insert("", END, values=i)

    def export_csv(self):
        if len(mydata) < 1:
            messagebox.showerror("Error", "No Data Found!", parent=self.root)
            return False
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")), parent=self.root)
        with open(fln, mode="w", newline="") as myfile:
            exp_write = csv.writer(myfile, delimiter=",")
            for i in mydata:
                exp_write.writerow(i)
            messagebox.showinfo("Success", "Export Data Successfully!")

    def reset_data(self):
        self.var_id.set("")
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.var_subject.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attend.set("Status")

    def get_cursor(self, event=""):
        cursor_focus = self.attendanceReport.focus()
        content = self.attendanceReport.item(cursor_focus)
        data = content["values"]
        self.var_id.set(data[0])
        self.var_roll.set(data[1])
        self.var_name.set(data[2])
        self.var_course.set(data[3])
        self.var_subject.set(data[4])
        self.var_time.set(data[5])
        self.var_date.set(data[6])
        self.var_attend.set(data[7])

if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
