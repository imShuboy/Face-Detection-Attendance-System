from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import numpy as np
import os
from sys import path

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.resizable(False, False)
        self.root.title("Student Panel")

        # ============ Variables =================
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_mob = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()

        # Setup Images and UI Elements
        self._setup_images()
        self._setup_title()
        self._setup_frames()

    def _setup_images(self):
        # First Header Image
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

    def _setup_title(self):
        title_lb1 = Label(self.root, text="Student Panel", font=("Verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

    def _setup_frames(self):
        main_frame = Frame(self.root, bd=2, bg="white")
        main_frame.place(x=5, y=55, width=1355, height=575)

        # Left Frame for Student Information
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details", font=("Verdana", 12, "bold"), fg="black")
        left_frame.place(x=10, y=10, width=660, height=555)

        # Current Course Frame
        current_course_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Current Course", font=("Verdana", 12, "bold"), fg="black")
        current_course_frame.place(x=10, y=5, width=635, height=150)

        # Department Label and ComboBox
        dep_label = Label(current_course_frame, text="Department", font=("Verdana", 12, "bold"), bg="white", fg="black")
        dep_label.grid(row=0, column=0, padx=5, pady=15)
        dep = ["Select Department", "Management", "ICS", "Pharmacy"]
        dep_combo = self._create_combo_box(current_course_frame, 0, 1, dep, self.var_dep)

        # Course Label and ComboBox
        cou_label = Label(current_course_frame, text="Course", font=("Verdana", 12, "bold"), bg="white", fg="black")
        cou_label.grid(row=0, column=2, padx=5, pady=15)
        courM = ["PGDM (e-Business)", "PGP EMBA", "PGP SBA", "MMS", "Ph.D. in Management"]
        courIT = ["MCA", "PGP in Data Science", "PGDAC", "DACA", "Pre DAC", "e-DAC"]
        courPh = ["B.Pharm", "D.Pharm", "ADPBM", "ADTAC"]
        cour_combo = self._create_combo_box(current_course_frame, 0, 3, [], self.var_course)

        def pick_dep(e):
            if dep_combo.get() == "Management":
                cour_combo.config(value=courM)
            elif dep_combo.get() == "ICS":
                cour_combo.config(value=courIT)
            elif dep_combo.get() == "Pharmacy":
                cour_combo.config(value=courPh)

        dep_combo.bind("<<ComboboxSelected>>", pick_dep)

        # Year ComboBox
        year_label = Label(current_course_frame, text="Year", font=("Verdana", 12, "bold"), bg="white", fg="black")
        year_label.grid(row=1, column=0, padx=5, sticky=W)
        year = ["Select Year", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
        year_combo = self._create_combo_box(current_course_frame, 1, 1, year, self.var_year)

        # Semester ComboBox
        semester_label = Label(current_course_frame, text="Semester", font=("Verdana", 12, "bold"), bg="white", fg="black")
        semester_label.grid(row=1, column=2, padx=5, sticky=W)
        semester = ["Select Semester", "Semester-1", "Semester-2", "Semester-3", "Semester-4"]
        semester_combo = self._create_combo_box(current_course_frame, 1, 3, semester, self.var_semester)

    def _create_combo_box(self, frame, row, col, values, var):
        combo = ttk.Combobox(frame, textvariable=var, width=15, font=("Verdana", 12), state="readonly", values=values)
        combo.grid(row=row, column=col, padx=5, pady=15, sticky=W)
        combo.current(0)
        return combo

    # Fetch Data from Database
    def fetch_data(self):
        conn = mysql.connector.connect(username='root', password='password', host='localhost', database='face_recognition', port=3306)
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM student")
        data = mycursor.fetchall()

        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("", END, values=i)

        conn.commit()
        conn.close()

    # Reset Data Function
    def reset_data(self):
        conn = mysql.connector.connect(username='root', password='password', host='localhost', database='face_recognition', port=3306)
        mycursor = conn.cursor()
        mycursor.execute("SELECT std_id FROM student ORDER BY std_id DESC LIMIT 1")
        data = mycursor.fetchall()
        self.var_std_id.set(int(data[0][0]) + 1)
        conn.commit()
        conn.close()

        # Reset input fields
        self.var_std_name.set("")
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_div.set("Morning")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_mob.set("")
        self.var_address.set("")
        self.var_roll.set("")
        self.var_email.set("")
        self.var_radio1.set("")

    # Get Selected Row (Cursor) Function
    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_std_id.set(data[0])
        self.var_std_name.set(data[1])
        self.var_roll.set(data[2])
        self.var_dep.set(data[3])
        self.var_course.set(data[4])
        self.var_year.set(data[5])
        self.var_semester.set(data[6])
        self.var_div.set(data[7])
        self.var_gender.set(data[8])
        self.var_dob.set(data[9])
        self.var_mob.set(data[10])
        self.var_address.set(data[11])
        self.var_email.set(data[12])
        self.var_radio1.set(data[13])

    # Update Data Function
    def update_data(self):
        if self.var_dep.get() == "Select Department" or self.var_course.get() == "" or self.var_year.get() == "Select Year" or self.var_semester.get() == "Select Semester" or self.var_std_id.get() == "" or self.var_std_name.get() == "" or self.var_div.get() == "" or self.var_roll.get() == "" or self.var_gender.get() == "" or self.var_dob.get() == "" or self.var_email.get() == "" or self.var_mob.get() == "" or self.var_address.get() == "":
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
        else:
            try:
                update = messagebox.askyesno("Update", "Do you want to Update this Student Details?", parent=self.root)
                if update > 0:
                    conn = mysql.connector.connect(username='root', password='password', host='localhost', database='face_recognition', port=3306)
                    mycursor = conn.cursor()
                    mycursor.execute("""
                        UPDATE student 
                        SET std_id=%s, std_name=%s, dep=%s, course=%s, yrs=%s, semester=%s, division=%s, gender=%s, dob=%s, mob=%s, address=%s, roll=%s, email=%s, photosample=%s
                        WHERE roll=%s
                    """, (
                        self.var_std_id.get(),
                        self.var_std_name.get(),
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_div.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_mob.get(),
                        self.var_address.get(),
                        self.var_roll.get(),
                        self.var_email.get(),
                        self.var_radio1.get(),
                        self.var_roll.get()
                    ))
                    messagebox.showinfo("Success", "Successfully Updated!", parent=self.root)
                    conn.commit()
                    self.fetch_data()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    # Delete Data Function
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student Id Must be Required!", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", "Do you want to Delete?", parent=self.root)
                if delete > 0:
                    conn = mysql.connector.connect(username='root', password='password', host='localhost', database='face_recognition', port=3306)
                    mycursor = conn.cursor()
                    mycursor.execute("DELETE FROM student WHERE std_id=%s", (self.var_std_id.get(),))
                    messagebox.showinfo("Delete", "Successfully Deleted!", parent=self.root)
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    self.reset_data()
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    # Generate Dataset and Take Image
    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or self.var_course.get() == "Select Course" or self.var_year.get() == "Select Year" or self.var_semester.get() == "Select Semester" or self.var_std_id.get() == "" or self.var_std_name.get() == "" or self.var_div.get() == "" or self.var_roll.get() == "" or self.var_gender.get() == "" or self.var_dob.get() == "" or self.var_email.get() == "" or self.var_mob.get() == "" or self.var_address.get() == "":
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(username='root', password='password', host='localhost', database='face_recognition', port=3306)
                mycursor = conn.cursor()
                mycursor.execute("SELECT * FROM student")
                myresult = mycursor.fetchall()

                for _ in myresult:
                    mycursor.execute("UPDATE student SET std_name=%s, dep=%s, course=%s, yrs=%s, semester=%s, division=%s, gender=%s, dob=%s, mob=%s, address=%s, roll=%s, email=%s, photosample=%s WHERE std_id=%s", (
                        self.var_std_name.get(),
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_div.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_mob.get(),
                        self.var_address.get(),
                        self.var_roll.get(),
                        self.var_email.get(),
                        self.var_radio1.get(),
                        self.var_std_id.get() + 1
                    ))
                conn.commit()
                self.fetch_data()
                conn.close()

                messagebox.showinfo("Result", "Generating dataset completed!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    # ========================== Train Classifier ==========================
    def train_classifier(self):
        data_dir = "data_img"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L')
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('_')[1])
            faces.append(imageNp)
            ids.append(id)

        cv2.imshow("Training", imageNp)
        cv2.waitKey(1) == 13

        ids = np.array(ids)

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Training Dataset Completed!", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
