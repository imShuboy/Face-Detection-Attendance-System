import re
from sys import path
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import mysql.connector
import cv2
import numpy as np
from tkinter import messagebox
from datetime import datetime

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Panel")

        # ============ Variables =================
        self.var_faculty_name = StringVar()
        self.var_subject = StringVar()
        self.var_dep = StringVar()
        self.var_course = StringVar()

        # ============ Setup Images ================
        self._setup_images()

        # ============ Create UI Elements =========
        self._setup_ui()

    def _setup_images(self):
        # First Header Image
        img = Image.open(r"Images_GUI\banner1.jpg")
        img = img.resize((1366, 130), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        # Set image as label
        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # Background image
        bg1 = Image.open(r"Images_GUI\bg3.jpg")
        bg1 = bg1.resize((1366, 768), Image.ANTIALIAS)
        self.photobg1 = ImageTk.PhotoImage(bg1)
        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

    def _setup_ui(self):
        # Title Section
        title_lb1 = Label(self.root, text="Face Recognition Panel", font=("Verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Main Frame
        main_frame = Frame(self.root, bd=2, bg="white")
        main_frame.place(x=340, y=120, width=635, height=380)

        # Center Frame for Student Details
        center_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Automate Attendance", font=("Verdana", 12, "bold"), fg="black")
        center_frame.place(x=10, y=10, width=610, height=355)

        # Department and Course Combo Boxes
        self._create_department_course_section(center_frame)

        # Faculty Name and Subject Inputs
        self._create_faculty_subject_section(center_frame)

        # Attendance Button
        self._create_attendance_button(center_frame)

    def _create_department_course_section(self, parent_frame):
        # Department Label and Combo Box
        dep_label = Label(parent_frame, text="Department", font=("Verdana", 12, "bold"), bg="white", fg="black")
        dep_label.grid(row=0, column=0, padx=5, pady=15)

        dep = ["Select Department", "Management", "ICS", "Pharmacy"]
        dep_combo = ttk.Combobox(parent_frame, textvariable=self.var_dep, width=15, font=("Verdana", 12), state="readonly", values=dep)
        dep_combo.grid(row=0, column=1, padx=5, pady=15, sticky=W)
        dep_combo.current(0)

        # Course Label and Combo Box
        cou_label = Label(parent_frame, text="Course", font=("Verdana", 12, "bold"), bg="white", fg="black")
        cou_label.grid(row=0, column=2, padx=5, pady=15)

        cou_combo = ttk.Combobox(parent_frame, textvariable=self.var_course, width=15, font=("Verdana", 12), state="readonly", values=[" "])
        cou_combo.grid(row=0, column=3, padx=5, pady=15, sticky=W)
        cou_combo.current(0)

    def _create_faculty_subject_section(self, parent_frame):
        # Faculty Name Input
        faculty_name_label = Label(parent_frame, text="Faculty Name:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        faculty_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        faculty_name_entry = ttk.Entry(parent_frame, width=15, textvariable=self.var_faculty_name, font=("Verdana", 12))
        faculty_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # Subject Input
        subject_label = Label(parent_frame, text="Subject:", font=("Verdana", 12, "bold"), fg="black", bg="white")
        subject_label.grid(row=1, column=2, padx=5, pady=5, sticky=W)

        subject_entry = ttk.Entry(parent_frame, width=15, textvariable=self.var_subject, font=("Verdana", 12))
        subject_entry.grid(row=1, column=3, padx=5, pady=5, sticky=W)

    def _create_attendance_button(self, parent_frame):
        # Button for Face Recognition
        std_img_btn = Image.open(r"Images_GUI\f_bg.jpg")
        std_img_btn = std_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)
        
        std_b1 = Button(parent_frame, command=self.face_recog, image=self.std_img1, cursor="hand2")
        std_b1.place(x=230, y=110, width=180, height=180)

        std_b1_1 = Button(parent_frame, command=self.face_recog, text="Face Detector", cursor="hand2", font=("Tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=230, y=280, width=180, height=45)

    def face_recog(self):
        if self.var_dep.get() == "Select Department" or self.var_course.get() == "" or self.var_faculty_name.get() == "" or self.var_subject.get() == "":
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
        else:
            # Load face detection model
            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("classifier.xml")
            videoCap = cv2.VideoCapture(0)

            while True:
                ret, img = videoCap.read()
                img = self.recognize(img, clf, face_classifier)
                cv2.imshow("Face Detector", img)

                if cv2.waitKey(1) == 13:
                    break

            videoCap.release()
            cv2.destroyAllWindows()

    def recognize(self, img, clf, faceCascade):
        coord = self.draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
        return img

    def draw_boundary(self, img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            id, predict = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int((100 * (1 - predict / 300)))
            self.mark_attendance(id, confidence)
        return img

    def mark_attendance(self, i, confidence):
        if confidence > 77:
            now = datetime.now()
            date_str = now.strftime("%d-%m-%Y")
            time_str = now.strftime("%H:%M:%S")

            with open(f"attendance/{self.var_course.get()}_{self.var_faculty_name.get()}_{self.var_subject.get()}_{date_str}.csv", "a+") as f:
                f.writelines(f"{i}, {time_str}, {date_str}, Present\n")

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
