from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from student import Student
from face_recognition import Face_Recognition
from attendance import Attendance

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.resizable(False, False)
        self.root.title("Face Recognition System")
        
        # Image Setup
        self._setup_images()

        # Title Section
        self._setup_title()

        # Button Setup
        self._setup_buttons()

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

    def _setup_title(self):
        title_lb1 = Label(self.root, text="Face Detection Attendance System", font=("Verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

    def _setup_buttons(self):
        # Student Panel Button
        std_img_btn = Image.open(r"Images_GUI\std1.jpg")
        std_img_btn = std_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)
        std_b1 = Button(self.root, image=self.std_img1, cursor="hand2", command=self.student_pannels)
        std_b1.place(x=350, y=210, width=180, height=180)
        std_b1_1 = Button(self.root, text="Student Panel", cursor="hand2", command=self.student_pannels, font=("Tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=350, y=385, width=180, height=45)

        # Face Detector Button
        det_img_btn = Image.open(r"Images_GUI\det1.jpg")
        det_img_btn = det_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.det_img1 = ImageTk.PhotoImage(det_img_btn)
        det_b1 = Button(self.root, image=self.det_img1, cursor="hand2", command=self.face_recognition)
        det_b1.place(x=580, y=210, width=180, height=180)
        det_b1_1 = Button(self.root, text="Face Detector", cursor="hand2", command=self.face_recognition, font=("Tahoma", 15, "bold"), bg="white", fg="navyblue")
        det_b1_1.place(x=580, y=385, width=180, height=45)

        # Attendance System Button
        att_img_btn = Image.open(r"Images_GUI\att.jpg")
        att_img_btn = att_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.att_img1 = ImageTk.PhotoImage(att_img_btn)
        att_b1 = Button(self.root, image=self.att_img1, cursor="hand2", command=self.attendance)
        att_b1.place(x=810, y=210, width=180, height=180)
        att_b1_1 = Button(self.root, text="Attendance", cursor="hand2", command=self.attendance, font=("Tahoma", 15, "bold"), bg="white", fg="navyblue")
        att_b1_1.place(x=810, y=385, width=180, height=45)

    def student_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def face_recognition(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    def attendance(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

if __name__ == "__main__":
    root = Tk()
    app = Face_Recognition_System(root)
    root.mainloop()
