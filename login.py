from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from register import Register
import mysql.connector
from main import Face_Recognition_System
import os

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1366x768+0+0")
        
        # Variables
        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()

        # Header Image
        img = Image.open(r"Images_GUI\banner1.jpg")
        img = img.resize((1366, 130), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        # Set Image as Label
        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # Background Image
        bg1 = Image.open(r"Images_GUI\bg3.jpg")
        bg1 = bg1.resize((1366, 768), Image.ANTIALIAS)
        self.photobg1 = ImageTk.PhotoImage(bg1)
        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # Title Section
        title_lb1 = Label(bg_img, text="Face Detection Attendance System", font=("Verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Frame for Login Section
        frame1 = Frame(self.root, bg="#F2F2F2")
        frame1.place(x=560, y=250, width=340, height=430)

        # Login Image
        img1 = Image.open(r"Images_GUI\log1.png")
        img1 = img1.resize((100, 100), Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lb1img1 = Label(image=self.photoimage1, bg="#F2F2F2")
        lb1img1.place(x=690, y=260, width=100, height=100)

        # Title Text
        get_str = Label(frame1, text="Teacher's Login", font=("Times New Roman", 20, "bold"), fg="navyblue")
        get_str.place(x=80, y=110)

        # Username Label
        username = Label(frame1, text="Username:", font=("Times New Roman", 15, "bold"), fg="navyblue")
        username.place(x=30, y=160)

        # Username Entry
        self.txtuser = ttk.Entry(frame1, font=("Times New Roman", 15, "bold"))
        self.txtuser.place(x=33, y=190, width=270)

        # Password Label
        pwd = Label(frame1, text="Password:", font=("Times New Roman", 15, "bold"), fg="navyblue")
        pwd.place(x=30, y=230)

        # Password Entry
        self.txtpwd = ttk.Entry(frame1, font=("Times New Roman", 15, "bold"))
        self.txtpwd.place(x=33, y=260, width=270)

        # Login Button
        loginbtn = Button(frame1, command=self.login, text="Login", font=("Times New Roman", 15, "bold"), bd=0, relief=RIDGE, fg="white", bg="navyblue", activeforeground="white", activebackground="#007ACC")
        loginbtn.place(x=33, y=320, width=270, height=35)

        # Register Button
        loginbtn = Button(frame1, command=self.reg, text="Register", font=("Times New Roman", 10, "bold"), bd=0, relief=RIDGE, fg="navyblue", activeforeground="orange", activebackground="#0B5AB2")
        loginbtn.place(x=33, y=370, width=50, height=20)

        # Forget Password Button
        loginbtn = Button(frame1, command=self.forget_pwd, text="Forget", font=("Times New Roman", 10, "bold"), bd=0, relief=RIDGE, fg="navyblue", activeforeground="orange", activebackground="#0B5AB2")
        loginbtn.place(x=90, y=370, width=50, height=20)

    # Open Register Window
    def reg(self):
        self.new_window = Toplevel(self.root)
        self.app = Register(self.new_window)

    # Login Function
    def login(self):
        if (self.txtuser.get() == "" or self.txtpwd.get() == ""):
            messagebox.showerror("Error", "All fields are required!")
        elif (self.txtuser.get() == "admin" and self.txtpwd.get() == "admin"):
            messagebox.showinfo("Success", "Welcome to Attendance Management System Using Facial Recognition")
        else:
            conn = mysql.connector.connect(username='root', password='password', host='localhost', database='face_recognition', port=3306)
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM teacher WHERE email=%s AND pwd=%s", (self.txtuser.get(), self.txtpwd.get()))
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Username or Password!")
            else:
                open_min = 1
                if open_min > 0:
                    self.new_window = Toplevel(self.root)
                    self.app = Face_Recognition_System(self.new_window)
            conn.commit()
            conn.close()

    # Reset Password Function
    def reset_pass(self):
        if self.var_ssq.get() == "Select":
            messagebox.showerror("Error", "Select the Security Question!", parent=self.root2)
        elif self.var_sa.get() == "":
            messagebox.showerror("Error", "Please Enter the Answer!", parent=self.root2)
        elif self.var_pwd.get() == "":
            messagebox.showerror("Error", "Please Enter the New Password!", parent=self.root2)
        else:
            conn = mysql.connector.connect(username='root', password='password', host='localhost', database='face_recognition', port=3306)
            mycursor = conn.cursor()
            query = "SELECT * FROM teacher WHERE email=%s AND ss_que=%s AND s_ans=%s"
            value = (self.txtuser.get(), self.var_ssq.get(), self.var_sa.get())
            mycursor.execute(query, value)
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Incorrect Answer!", parent=self.root2)
            else:
                query = "UPDATE teacher SET pwd=%s WHERE email=%s"
                value = (self.var_pwd.get(), self.txtuser.get())
                mycursor.execute(query, value)
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Your password has been reset. Please login with the new password.", parent=self.root2)

    # Forget Password Function
    def forget_pwd(self):
        if self.txtuser.get() == "":
            messagebox.showerror("Error", "Please Enter the Email ID to reset Password!")
        else:
            conn = mysql.connector.connect(username='root', password='password', host='localhost', database='face_recognition', port=3306)
            mycursor = conn.cursor()
            query = "SELECT * FROM teacher WHERE email=%s"
            value = (self.txtuser.get(),)
            mycursor.execute(query, value)
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Please Enter a Valid Email ID!")
            else:
                conn.close()
                self.root2 = Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("400x400+610+170")
                l = Label(self.root2, text="Forget Password", font=("Times New Roman", 30, "bold"), fg="#0B5AB2", bg="#fff")
                l.place(x=0, y=10, relwidth=1)

                # Security Question and Answer
                ssq = Label(self.root2, text="Select Security Question:", font=("Times New Roman", 15, "bold"), fg="#0B5AB2", bg="#F2F2F2")
                ssq.place(x=70, y=80)
                self.combo_security = ttk.Combobox(self.root2, textvariable=self.var_ssq, font=("Times New Roman", 15, "bold"), state="readonly")
                self.combo_security["values"] = ("Select", "Your Date of Birth", "Your Nick Name", "Your Favorite Book")
                self.combo_security.current(0)
                self.combo_security.place(x=70, y=110, width=270)

                # Security Answer
                sa = Label(self.root2, text="Security Answer:", font=("Times New Roman", 15, "bold"), fg="#0B5AB2", bg="#F2F2F2")
                sa.place(x=70, y=150)
                self.txtpwd = ttk.Entry(self.root2, textvariable=self.var_sa, font=("Times New Roman", 15, "bold"))
                self.txtpwd.place(x=70, y=180, width=270)

                # New Password
                new_pwd = Label(self.root2, text="New Password:", font=("Times New Roman", 15, "bold"), fg="#0B5AB2", bg="#F2F2F2")
                new_pwd.place(x=70, y=220)
                self.new_pwd = ttk.Entry(self.root2, textvariable=self.var_pwd, font=("Times New Roman", 15, "bold"))
                self.new_pwd.place(x=70, y=250, width=270)

                # Reset Password Button
                loginbtn = Button(self.root2, command=self.reset_pass, text="Reset Password", font=("Times New Roman", 15, "bold"), bd=0, relief=RIDGE, fg="#fff", bg="#0B5AB2", activeforeground="white", activebackground="#007ACC")
                loginbtn.place(x=70, y=300, width=270, height=35)

    # Main Function
    def main(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition_System(self.new_window)

if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()
