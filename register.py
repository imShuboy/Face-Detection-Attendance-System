from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("1366x768+0+0")

        # ============ Variables =================
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_cnum = StringVar()
        self.var_email = StringVar()
        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()
        self.var_cpwd = StringVar()
        self.var_check = IntVar()

        # First Header Image
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

        # Frame for Registration Section
        frame = Frame(self.root, bg="#F2F2F2")
        frame.place(x=240, y=210, width=900, height=480)

        # Registration Title
        get_str = Label(frame, text="Registration", font=("Times New Roman", 30, "bold"), fg="#002B53", bg="#F2F2F2")
        get_str.place(x=350, y=20)

        # First Name Label and Entry
        fname = Label(frame, text="First Name:", font=("Times New Roman", 15, "bold"), fg="#002B53", bg="#F2F2F2")
        fname.place(x=100, y=100)
        self.txtuser = ttk.Entry(frame, textvariable=self.var_fname, font=("Times New Roman", 15, "bold"))
        self.txtuser.place(x=103, y=125, width=270)

        # Last Name Label and Entry
        lname = Label(frame, text="Last Name:", font=("Times New Roman", 15, "bold"), fg="#002B53", bg="#F2F2F2")
        lname.place(x=100, y=170)
        self.txtpwd = ttk.Entry(frame, textvariable=self.var_lname, font=("Times New Roman", 15, "bold"))
        self.txtpwd.place(x=103, y=195, width=270)

        # Contact No. Label and Entry
        cnum = Label(frame, text="Contact No:", font=("Times New Roman", 15, "bold"), fg="#002B53", bg="#F2F2F2")
        cnum.place(x=530, y=100)
        self.txtuser = ttk.Entry(frame, textvariable=self.var_cnum, font=("Times New Roman", 15, "bold"))
        self.txtuser.place(x=533, y=125, width=270)

        # Email Label and Entry
        email = Label(frame, text="Email:", font=("Times New Roman", 15, "bold"), fg="#002B53", bg="#F2F2F2")
        email.place(x=530, y=170)
        self.txtpwd = ttk.Entry(frame, textvariable=self.var_email, font=("Times New Roman", 15, "bold"))
        self.txtpwd.place(x=533, y=195, width=270)

        # Security Question Section
        ssq = Label(frame, text="Select Security Question:", font=("Times New Roman", 15, "bold"), fg="#002B53", bg="#F2F2F2")
        ssq.place(x=100, y=250)
        self.combo_security = ttk.Combobox(frame, textvariable=self.var_ssq, font=("Times New Roman", 15, "bold"), state="readonly")
        self.combo_security["values"] = ("Select", "Your Date of Birth", "Your Nick Name", "Your Favorite Book")
        self.combo_security.current(0)
        self.combo_security.place(x=103, y=275, width=270)

        # Security Answer Label and Entry
        sa = Label(frame, text="Security Answer:", font=("Times New Roman", 15, "bold"), fg="#002B53", bg="#F2F2F2")
        sa.place(x=100, y=320)
        self.txtpwd = ttk.Entry(frame, textvariable=self.var_sa, font=("Times New Roman", 15, "bold"))
        self.txtpwd.place(x=103, y=345, width=270)

        # Password Section
        pwd = Label(frame, text="Password:", font=("Times New Roman", 15, "bold"), fg="#002B53", bg="#F2F2F2")
        pwd.place(x=530, y=250)
        self.txtuser = ttk.Entry(frame, textvariable=self.var_pwd, font=("Times New Roman", 15, "bold"))
        self.txtuser.place(x=533, y=275, width=270)

        # Confirm Password Section
        cpwd = Label(frame, text="Confirm Password:", font=("Times New Roman", 15, "bold"), fg="#002B53", bg="#F2F2F2")
        cpwd.place(x=530, y=320)
        self.txtpwd = ttk.Entry(frame, textvariable=self.var_cpwd, font=("Times New Roman", 15, "bold"))
        self.txtpwd.place(x=533, y=345, width=270)

        # Terms and Conditions Checkbox
        checkbtn = Checkbutton(frame, variable=self.var_check, text="I Agree the Terms & Conditions", font=("Times New Roman", 13, "bold"), fg="#002B53", bg="#F2F2F2")
        checkbtn.place(x=100, y=380, width=270)

        # Register Button
        loginbtn = Button(frame, command=self.reg, text="Register", font=("Times New Roman", 15, "bold"), bd=0, relief=RIDGE, fg="#fff", bg="#002B53", activeforeground="white", activebackground="#007ACC")
        loginbtn.place(x=103, y=410, width=270, height=35)

    # Register Function
    def reg(self):
        if (self.var_fname.get() == "" or self.var_lname.get() == "" or self.var_cnum.get() == "" or self.var_email.get() == "" or self.var_ssq.get() == "Select" or self.var_sa.get() == "" or self.var_pwd.get() == "" or self.var_cpwd.get() == ""):
            messagebox.showerror("Error", "All Fields are Required!")
        elif (self.var_pwd.get() != self.var_cpwd.get()):
            messagebox.showerror("Error", "Passwords do not match!")
        elif (self.var_check.get() == 0):
            messagebox.showerror("Error", "Please Agree to the Terms and Conditions!")
        else:
            try:
                conn = mysql.connector.connect(username='root', password='password', host='localhost', database='face_recognition', port=3306)
                mycursor = conn.cursor()
                query = "SELECT * FROM teacher WHERE email=%s"
                value = (self.var_email.get(),)
                mycursor.execute(query, value)
                row = mycursor.fetchone()
                if row != None:
                    messagebox.showerror("Error", "User already exists, please try another email")
                else:
                    mycursor.execute("INSERT INTO teacher (first_name, last_name, contact_number, email, security_question, security_answer, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                                     (self.var_fname.get(), self.var_lname.get(), self.var_cnum.get(), self.var_email.get(), self.var_ssq.get(), self.var_sa.get(), self.var_pwd.get()))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Successfully Registered!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    app = Register(root)
    root.mainloop()
