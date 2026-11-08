from tkinter import *
from tkinter import ttk
from tkmacosx import Button
from tkinter import messagebox
from time import sleep
from PIL import Image, ImageTk
import sqlite3 as sql
from datetime import datetime
import hashlib

#Window and Frame Instances
startup = Tk()
loginframe = Frame(
     startup,
     bg = "#ffffbd",
     highlightthickness = 3,
     highlightbackground = "#000000")


#Tkinter Variables
uservar = StringVar()
passvar = StringVar()

def_font = "Literata 18pt"
def_bg = "#ffffbd"

loggedin_user = None

#\\-------------------------\\#
#\\---Window Fundamentals---\\#
width = startup.winfo_screenwidth()
height = startup.winfo_screenheight()
resolution = str(width) + "x" + str(height)
startup.config(background = def_bg)
startup.geometry(resolution)
startup.title("FocusLog")
#---Window Fundamentals---#

#----------------Create Database and Tables---------------#

#define connection and cursor
connection = sql.connect("FocusLog.db")

#A cursor is an object that allows sql commands to be executed
cursor = connection.cursor()

#creating Users table
create_users_table = """CREATE TABLE IF NOT EXISTS
Users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR(20) UNIQUE,
hashed_password VARCHAR(255) NOT NULL,
remembrance_word VARCHAR(30) NOT NULL)
"""

create_entries_table = """CREATE TABLE IF NOT EXISTS
Entries(entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
entry_title VARCHAR(100) NOT NULL,
entry_text TEXT NOT NULL,
entry_date DATE NOT NULL,
FOREIGN KEY(user_id) REFERENCES Users(user_id))
"""

create_tasks_table = """CREATE TABLE IF NOT EXISTS
Tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
task_text TEXT NOT NULL,
completed INTEGER DEFAULT 0,
FOREIGN KEY(user_id) REFERENCES Users(user_id))"""

cursor.execute(create_users_table)
cursor.execute(create_entries_table)
cursor.execute(create_tasks_table)

#----------------//Create Database and Tables//---------------#

#xxxxxxxxxx User Class xxxxxxxxxx

class User:
     def __init__(self, user_id):
          self.user_id = int(user_id)
     
     def SignOut(self):
          self.user_id = None

#xxxxxxxxxx User Class END xxxxxxxxxx






#--ALL Functions--#

def hashlib_password_or_remembrance(passwordORremembrance):
     return hashlib.sha256(passwordORremembrance.encode()).hexdigest()

def SubmitLogin():
     global loggedin_user
     entered_password = PasswordEntry.get()
     entered_username = UsernameEntry.get()
     entered_password_hashed = hashlib_password_or_remembrance(entered_password)

     #Clear username and password boxes:
     UsernameEntry.delete(0, END)
     PasswordEntry.delete(0, END)

     print(entered_password_hashed)
     try:
          cursor.execute("""
                         SELECT * FROM Users
                         WHERE username = ? AND hashed_password = ?""",
                         (entered_username, entered_password_hashed))
          
          in_database_result = cursor.fetchone()
          
          if in_database_result:
               signinconfirmation = messagebox.showinfo("Confirmation", "Login Successful")
               loggedin_user = User(in_database_result[0])
               showhomepage(loginframe)
          else:
               messagebox.showerror("ERROR", "Your username or password is incorrect")
     except:
          messagebox.showerror("ERROR", "Unexpected Error. Please try again.")


def check_fields(*args):
    if len(uservar.get()) > 4 and len(passvar.get()) > 7 and len(uservar.get()) <= 30:
        if " " in uservar.get():
             messagebox.showerror("ERROR", "Username cannot contain spaces")
        else:
             LoginSubmitButton.config(bg = "#A1FFBA",
                                      state = NORMAL)
    else:
        LoginSubmitButton.config(state = DISABLED)

def redirectCreateAccount():
     loginframe.place_forget()
     createaccountframe.place(relx=0.5, rely = 0.5, anchor = CENTER)
     startup.update_idletasks()        # forces grid layout
     CreateUsernameEntry.focus_set()   # forces redraw & focus

def redirectForgotPassword():
     loginframe.place_forget()
     forgotpasswordframe.place(relx=0.5, rely = 0.5, anchor = CENTER)
     startup.update_idletasks()        # forces grid layout
     CreateUsernameEntry.focus_set()   # forces redraw & focus

def showloginpage(curr_page):
     curr_page.place_forget()
     curr_page.grid_forget()
     loginframe.place(relx=0.5, rely = 0.5, anchor = CENTER)
     startup.update_idletasks()        # forces grid layout
     CreateUsernameEntry.focus_set()   # forces redraw & focus

def showhomepage(curr_page):
     curr_page.place_forget()
     homepageframe.grid(row = 0, column = 0, sticky = "nsew", padx = 40, pady = (20, 30))
     startup.update_idletasks()        # forces grid layout

def validateCreateAccount():
     entered_username = CreateUsernameEntry.get()
     entered_password = CreatePasswordEntry.get()
     entered_remembrance = CreateRemembranceEntry.get()

     if len(entered_username) < 5:
          messagebox.showerror("ERROR", "Username must be at least 5 characters")
     
     elif len(entered_username) > 20:
          messagebox.showerror("ERROR", "Username must not be more than 20 characters")

     elif any(char == " " for char in entered_username):
          messagebox.showerror("ERROR", "Username must not contain spaces")

     elif len(entered_password) < 8:
          messagebox.showerror("ERROR", "Password must be at least 8 characters")
     
     elif len(entered_password) > 30:
          messagebox.showerror("ERROR", "Password must not be more than 30 characters")

     elif entered_password.lower() == entered_password:
          messagebox.showerror("ERROR", "Password must have at least one uppercase character")

     elif entered_password.upper() == entered_password:
          messagebox.showerror("ERROR", "Password must have at least one lowercase character")

     elif not any(char.isdigit() for char in entered_password):
          messagebox.showerror("ERROR", "Password must contain at least one number")

     elif len(entered_remembrance) < 5:
          messagebox.showerror("ERROR", "Remembrance Word must be at least 5 characters long")
     
     elif len(entered_remembrance) > 30:
          messagebox.showerror("ERROR", "Remembrance Word must not be more than 30 characters")

     else:
          DBvalidateCreateAccount(entered_username, entered_password, entered_remembrance)

def DBvalidateCreateAccount(user_username, user_password, user_remembrance_word):

     user_hashed_password = hashlib_password_or_remembrance(user_password)
     user_hashed_remembrance_word = hashlib_password_or_remembrance(user_remembrance_word)

     cursor.execute("SELECT * FROM users WHERE username = ?", (user_username,))
     result = cursor.fetchone()

     if result:
          messagebox.showerror("ERROR", "Username already exists. Please enter a different username.")
     else:
          try:
               cursor.execute(
                    "INSERT INTO Users (username, hashed_password, remembrance_word) VALUES (?, ?, ?)",
                              (user_username, user_hashed_password, user_hashed_remembrance_word))
               connection.commit()
               creationconfirmation = messagebox.showinfo("Confirmation", "Account created! Please sign in again.")
               showloginpage(createaccountframe)
          
          except:
               creationerror = messagebox.showerror("ERROR", "Failed to create account. Please try again.")

def CreateAccount():
     createaccountframe.place_forget()
     loginframe.place(relx=0.5, rely = 0.5, anchor = CENTER)
     startup.update_idletasks()        # forces grid layout
     CreateUsernameEntry.focus_set()   # forces redraw & focus

def ResetPassword():
     reset_password_username_entry = ForgotUsernameEntry.get()
     reset_password_remembrance_entry = ForgotRemembranceEntry.get()
     entered_password = ForgotCreatePasswordEntry.get()

     #check if details are correct first.
     try:
          cursor.execute("""
                         SELECT * FROM Users
                         WHERE username = ? AND remembrance_word = ?""",
                         (reset_password_username_entry, hashlib_password_or_remembrance(reset_password_remembrance_entry)))        
          in_database_result = cursor.fetchone()
          if in_database_result:
               #If details are correct, we can now reset the password.
               if len(entered_password) < 8:
                    messagebox.showerror("ERROR", "Password must be at least 8 characters")
               
               elif len(entered_password) > 30:
                    messagebox.showerror("ERROR", "Password must not be more than 30 characters")

               elif entered_password.lower() == entered_password:
                    messagebox.showerror("ERROR", "Password must have at least one uppercase character")

               elif entered_password.upper() == entered_password:
                    messagebox.showerror("ERROR", "Password must have at least one lowercase character")

               elif not any(char.isdigit() for char in entered_password):
                    messagebox.showerror("ERROR", "Password must contain at least one number")
               else:
                    hashed_new_password = hashlib_password_or_remembrance(entered_password)
                    cursor.execute("""
                                   UPDATE Users
                                   SET hashed_password = ?
                                   WHERE username = ?""", (hashed_new_password, reset_password_username_entry))
                    
                    connection.commit()

                    resetconfirmation = messagebox.showinfo("Confirmation", "Password Reset! Please sign in again.")
                    showloginpage(forgotpasswordframe)
          else:
               messagebox.showerror("ERROR", "Your username or remembrance word is incorrect. Please enter the correct details.")

     except:
          messagebox.showerror("ERROR", "Unexpected Error. Please try again.")

def LogOut():
     global loggedin_user
     loggedin_user.SignOut()
     showloginpage(homepageframe)

#--ALL Functions--#

#Homepage TopLevel Functions#
#ADD ENTRY SECTION
def open_addentry_window():
     addentry_window = Toplevel(startup)
     addentry_window.title("Add Entry")
     resolution_TopLevel = str(width-100) + "x" + str(height-100)
     addentry_window.geometry(resolution_TopLevel)
     addentry_window.config(bg = "#C3F0B9")

     def submit_AddEntry():

          title = EntryTitleEntry.get().strip()
          content = EntryContent.get("1.0", "end-1c")

          day = int(day_box.get())
          month = int(month_box.get())
          year = int(year_box.get())
          today = datetime.today().date()

          try:
               valid_date = datetime(year, month, day)
               if valid_date.date() > today:
                    messagebox.showerror("Date Error", "Date cannot be in the future.")
               else:
                    date_for_db = valid_date.strftime("%Y-%m-%d")
                    cursor.execute("""
                                   SELECT 1 FROM Entries
                                   WHERE user_id = ? AND entry_date = ? """,
                                   (loggedin_user.user_id, date_for_db))

                    existing_entry = cursor.fetchone()

                    if existing_entry:
                         messagebox.showerror("Duplicate Entry","You already have an entry for this date.")
               
                    elif len(title) < 1:
                         messagebox.showerror("Invalid Title", "Title cannot be empty.")

                    elif len(title) > 50:
                         messagebox.showerror("Invalid Title", "Title cannot exceed 50 characters.")
                    else:
                         if len(content) < 1:
                              messagebox.showerror("Invalid Content", "Entry content cannot be empty.")
                         elif len(content) > 5000:
                              messagebox.showerror("Invalid Content", "Entry content cannot exceed 5000 characters.")
                         else:
                              cursor.execute("""
                                             INSERT INTO Entries (user_id, entry_title, entry_text, entry_date)
                                             VALUES (?, ?, ?, ?)""",
                                             (loggedin_user.user_id, title, content, date_for_db))

                              connection.commit()
                              messagebox.showinfo("Successful", "Entry added!")
                              addentry_window.destroy()
                           
          except ValueError:
               messagebox.showerror("Invalid Date", "Please enter a valid date")
          




     #Widgets:
     today = datetime.today()

     date_frame = Frame(
          addentry_window,
          bg = "#C3F0B9")

     day_box = ttk.Combobox(
          date_frame,
          values=list(range(1, 32)),
          font = (def_font, 18),
          width=4,
          state="readonly",
          takefocus=False)
     day_box.set(today.day)

     month_box = ttk.Combobox(
          date_frame,
          values=list(range(1, 13)),
          font = (def_font, 18),
          width=4,
          state="readonly",
          takefocus=False)
     month_box.set(today.month)

     year_box = ttk.Combobox(
          date_frame,
          values=list(range(2015, today.year)),
          font = (def_font, 18),
          width=6,
          state="readonly",
          takefocus=False)
     year_box.set(today.year)

     EntryTitleEntry = Entry(
          addentry_window,
          font = (def_font, 20),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")
     EntryTitleLabel = Label(
          addentry_window,
          text = "Entry Title: ",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")


     EntryDateLabel = Label(
          addentry_window,
          text = "Date: ",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")

     EntryContentLabel = Label(
          addentry_window,
          text = "Type entry here: ",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")

     EntryContent = Text(
          addentry_window,
          font=(def_font, 14),
          fg = "#000000",
          wrap="word",
          bg="#FFFFFF")

     AddEntrySubmit = Button(
          addentry_window,
          text="Submit",
          font=(def_font, 22),
          bg = "#FECDFF",
          fg="#000000",
          justify = "center",
          borderless = 1,
          command = submit_AddEntry)

     EntryTitleLabel.pack()
     EntryTitleEntry.pack(pady = (10,20))

     EntryDateLabel.pack(pady = (0,10))
     date_frame.pack(pady=15)
     day_box.pack(side="left", padx=5)
     month_box.pack(side="left", padx=5)
     year_box.pack(side="left", padx=5)

     EntryContentLabel.pack(pady = 10)
     EntryContent.pack(pady=10, padx=10, expand=True, fill="both")

     AddEntrySubmit.pack(pady = 15)



#EDIT ENTRY SECTION
def open_editentry_window():
     editentry_window = Toplevel(startup)
     editentry_window.title("Edit Entry")
     resolution_TopLevel = str(width-100) + "x" + str(height-100)
     editentry_window.geometry(resolution_TopLevel)
     editentry_window.config(bg = "#C3F0B9")

     def SearchDB():
          day = day_box.get()
          month = month_box.get()
          year = year_box.get()

          try:
               day = int(day_box.get())
               month = int(month_box.get())
               year = int(year_box.get())
               valid_date = datetime(year, month, day)
               today = datetime.today().date()

               if valid_date.date() > today:
                    messagebox.showerror("Date Error", "Date cannot be in the future. Please enter a valid date.")
               else:
                    date_for_db_search = valid_date.strftime("%Y-%m-%d")
                    cursor.execute("""
                                   SELECT entry_title, entry_text FROM Entries
                                   WHERE user_id = ? AND entry_date = ? """,
                                   (loggedin_user.user_id, date_for_db_search))

                    existing_entry = cursor.fetchone()

                    if existing_entry:
                         db_entry_title = existing_entry[0]
                         db_entry_text = existing_entry[1]
                         show_entry_fields(db_entry_title, db_entry_text)
                    else:
                         messagebox.showerror("Error", "You have no existing entries for this date.")
          except ValueError:
               messagebox.showerror("Invalid Date", "Please enter a valid date.")

     def editentry_dbsubmit():
          title = EntryTitleEntry.get().strip()
          content = EntryContent.get("1.0", "end-1c")

          day = int(day_box.get())
          month = int(month_box.get())
          year = int(year_box.get())
          valid_date = datetime(year, month, day)
          date_for_db_edit = valid_date.strftime("%Y-%m-%d")
          
          try:
               if len(title) < 1:
                    messagebox.showerror("Invalid Title", "Title cannot be empty.")

               elif len(title) > 50:
                    messagebox.showerror("Invalid Title", "Title cannot exceed 50 characters.")
               else:
                    if len(content) < 1:
                         messagebox.showerror("Invalid Content", "Entry content cannot be empty.")
                    elif len(content) > 5000:
                         messagebox.showerror("Invalid Content", "Entry content cannot exceed 5000 characters.")
                    else:
                         cursor.execute("""
                                        UPDATE Entries
                                        SET entry_title = ?, entry_text = ?
                                        WHERE user_id = ? AND entry_date = ?""",
                                        (title, content, loggedin_user.user_id, date_for_db_edit))

                         connection.commit()
                         messagebox.showinfo("Success", "Entry updated successfully!")
                         editentry_window.destroy()
                           
          except ValueError:
               messagebox.showerror("Invalid Date", "Please enter a valid date")

     today = datetime.today()

     date_frame = Frame(
          editentry_window,
          bg = "#C3F0B9")

     day_box = ttk.Combobox(
          date_frame,
          values=list(range(1, 32)),
          font = (def_font, 18),
          width=4,
          state="readonly",
          takefocus=False)
     day_box.set(today.day)

     month_box = ttk.Combobox(
          date_frame,
          values=list(range(1, 13)),
          font = (def_font, 18),
          width=4,
          state="readonly",
          takefocus=False)
     month_box.set(today.month)

     year_box = ttk.Combobox(
          date_frame,
          values=list(range(2015, today.year)),
          font = (def_font, 18),
          width=6,
          state="readonly",
          takefocus=False)
     year_box.set(today.year)

     EditDateLabel = Label(
          editentry_window,
          text = "Enter Date: ",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")
     
     EditDateSearchButton = Button(
          date_frame,
          command = SearchDB,
          text = "Search date",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#FECDFF",
          borderwidth = 0,
          justify = "center",
          borderless = 1)
     
     EntryTitleEntry = Entry(
          editentry_window,
          font = (def_font, 20),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")
     EntryTitleLabel = Label(
          editentry_window,
          text = "Entry Title: ",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")
     
     EntryContentLabel = Label(
          editentry_window,
          text = "Type entry here: ",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")

     EntryContent = Text(
          editentry_window,
          font=(def_font, 14),
          fg = "#000000",
          wrap="word",
          bg="#FFFFFF")
     
     EditEntrySubmit = Button(
          editentry_window,
          text="Submit",
          font=(def_font, 22),
          bg = "#FECDFF",
          fg="#000000",
          justify = "center",
          borderless = 1,
          command = editentry_dbsubmit)

     EditDateLabel.pack(pady = (0,10))
     date_frame.pack(pady=15)
     day_box.pack(side="left", padx=5)
     month_box.pack(side="left", padx=5)
     year_box.pack(side="left", padx=5)
     EditDateSearchButton.pack(side = "left", padx = 5)

     def show_entry_fields(entrytitle, entrytext):

          EntryTitleLabel.pack()
          EntryTitleEntry.pack(pady = (10,20))
          EntryContentLabel.pack(pady = 10)
          EntryContent.pack(pady=10, padx=10, expand=True, fill="both")
          EditEntrySubmit.pack(pady = 5)

          EntryTitleEntry.delete(0, END)
          EntryTitleEntry.insert(0, entrytitle)
          EntryContent.delete("1.0", END)
          EntryContent.insert("1.0", entrytext)


#VIEW ENTRY SECTION
def open_viewentry_window():
     viewentry_window = Toplevel(startup)
     viewentry_window.title("View Entry")
     resolution_TopLevel = str(width-100) + "x" + str(height-100)
     viewentry_window.geometry(resolution_TopLevel)
     viewentry_window.config(bg = "#C3F0B9")

     def SearchDB():
          day = day_box.get()
          month = month_box.get()
          year = year_box.get()

          try:
               day = int(day_box.get())
               month = int(month_box.get())
               year = int(year_box.get())
               valid_date = datetime(year, month, day)
               today = datetime.today().date()

               if valid_date.date() > today:
                    messagebox.showerror("Date Error", "Date cannot be in the future. Please enter a valid date.")
               else:
                    date_for_db_search = valid_date.strftime("%Y-%m-%d")
                    cursor.execute("""
                                   SELECT entry_title, entry_text FROM Entries
                                   WHERE user_id = ? AND entry_date = ? """,
                                   (loggedin_user.user_id, date_for_db_search))

                    existing_entry = cursor.fetchone()

                    if existing_entry:
                         db_entry_title = existing_entry[0]
                         db_entry_text = existing_entry[1]
                         show_entry_fields(db_entry_title, db_entry_text)
                    else:
                         messagebox.showerror("Error", "You have no existing entries for this date.")
          except ValueError:
               messagebox.showerror("Invalid Date", "Please enter a valid date.")

     def CloseView():
          viewentry_window.destroy()

     today = datetime.today()

     date_frame = Frame(
          viewentry_window,
          bg = "#C3F0B9")

     day_box = ttk.Combobox(
          date_frame,
          values=list(range(1, 32)),
          font = (def_font, 18),
          width=4,
          state="readonly",
          takefocus=False)
     day_box.set(today.day)

     month_box = ttk.Combobox(
          date_frame,
          values=list(range(1, 13)),
          font = (def_font, 18),
          width=4,
          state="readonly",
          takefocus=False)
     month_box.set(today.month)

     year_box = ttk.Combobox(
          date_frame,
          values=list(range(2015, today.year)),
          font = (def_font, 18),
          width=6,
          state="readonly",
          takefocus=False)
     year_box.set(today.year)

     ViewDateLabel = Label(
          viewentry_window,
          text = "Enter Date: ",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")
     
     ViewDateSearchButton = Button(
          date_frame,
          command = SearchDB,
          text = "Search date",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#FECDFF",
          borderwidth = 0,
          justify = "center",
          borderless = 1)
     
     EntryTitleEntry = Entry(
          viewentry_window,
          font = (def_font, 20),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")
     EntryTitleLabel = Label(
          viewentry_window,
          text = "Title: ",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")
     
     EntryContentLabel = Label(
          viewentry_window,
          text = "Entry: ",
          font = (def_font, 18),
          fg = "#000000",
          bg = "#C3F0B9",
          borderwidth = 0,
          justify = "center")

     EntryContent = Text(
          viewentry_window,
          font=(def_font, 14),
          fg = "#000000",
          wrap="word",
          bg="#FFFFFF")
     
     CloseViewWindow = Button(
          viewentry_window,
          text="Done",
          font=(def_font, 22),
          bg = "#FECDFF",
          fg="#000000",
          justify = "center",
          borderless = 1,
          command = CloseView)

     ViewDateLabel.pack(pady = (0,10))
     date_frame.pack(pady=15)
     day_box.pack(side="left", padx=5)
     month_box.pack(side="left", padx=5)
     year_box.pack(side="left", padx=5)
     ViewDateSearchButton.pack(side = "left", padx = 5)

     def show_entry_fields(entrytitle, entrytext):

          EntryTitleLabel.pack()
          EntryTitleEntry.pack(pady = (10,20))
          EntryContentLabel.pack(pady = 10)
          EntryContent.pack(pady=10, padx=10, expand=True, fill="both")
          CloseViewWindow.pack(pady = 5)

          EntryTitleEntry.delete(0, END)
          EntryTitleEntry.insert(0, entrytitle)
          EntryContent.delete("1.0", END)
          EntryContent.insert("1.0", entrytext)

          EntryTitleEntry.config(state = "readonly",
                                 readonlybackground="white",
                                 fg="black")
          EntryContent.config(state = "disabled")

#Homepage TopLevel Functions#



#Live Changes (Trace)$
uservar.trace_add("write", check_fields)
passvar.trace_add("write", check_fields)
#\\-------------------------\\#
#\\-------------------------\\#



#//------------------------------//#
#//---Widgets for Login screen---//#
Welcome = Label(loginframe,
                text = "Welcome to FocusLog",
                bg = def_bg,
                fg = "#000000",
                font = (def_font, 50))

UsernameLabel = Label(loginframe,
                      text = "Username",
                      font = (def_font, 13),
                      bg = def_bg,
                      fg = "#000000")
UsernameEntry = Entry(loginframe,
                      textvariable = uservar,
                      font = (def_font, 28),
                      bg = "#ffffff",
                      fg = "#000000",
                      insertbackground="#000000")

PasswordLabel = Label(loginframe,
                      text = "Password",
                      font = (def_font, 13),
                      bg = def_bg,
                      fg = "#000000")
PasswordEntry = Entry(loginframe,
                      textvariable = passvar,
                      show = "•",
                      font = (def_font, 28),
                      bg = "#ffffff",
                      fg = "#000000",
                      insertbackground="#000000")

LoginSubmitButton = Button(loginframe,
                           text = "Login",
                           font = (def_font, 17),
                           padx = 10,
                           command = SubmitLogin,
                           activebackground = "#FFFFFF",
                           fg = "#000000",
                           bg = "#A1FFBA",
                           borderless = 1,
                           state = DISABLED)

CreateAccountButton = Button(loginframe,
                           text = "Create Account",
                           font = (def_font, 17),
                           padx = 14,
                           command = redirectCreateAccount,
                           activebackground = "#FFFFFF",
                           bg = "#BDECFA",
                           borderless = 1,
                           state = NORMAL
                           )

ForgotPasswordButton = Button(loginframe,
                           text = "Forgot Password?",
                           font = (def_font, 17),
                           padx = 5,
                           command = redirectForgotPassword,
                           bg = "#FECDFF",
                           activebackground = "#FFFFFF",
                           borderless = 1,
                           state = NORMAL)




#loginframe.place(relx=0.5, rely = 0.5, anchor = CENTER)

Welcome.grid(row = 0, column = 0, columnspan = 2)

UsernameLabel.grid(row = 4, column = 0, sticky = "w", padx = (20,0), pady = (30,0))
UsernameEntry.grid(row = 5, column = 0, sticky = "ew", columnspan = 2, padx = 20, pady = 10)

PasswordLabel.grid(row = 7, column = 0, sticky = "w", padx = (20,0), pady = (30,0))
PasswordEntry.grid(row = 8, column = 0, sticky = "ew", columnspan = 2, padx = 20, pady = 10)

LoginSubmitButton.grid(row = 9, column = 0, sticky = "w", padx = (20,0), pady = (0,20))

CreateAccountButton.grid(row = 9, column = 1, sticky = "e", padx = (0,20), pady = (0,20))
ForgotPasswordButton.grid(row = 10, column = 1, sticky = "e", padx = (0,20), pady = (0,20))
#//--------------------------//#
#//--------------------------//#


#<----------                   -------->#
#<---Widgets for Create Account Page--->#
createaccountframe = Frame(
     startup,
     bg = def_bg,
     highlightthickness = 2,
     highlightbackground = "#000000")

CreateAccountLabel = Label(createaccountframe,
                           text = "Create Account",
                           font = (def_font, 30),
                           fg = "#000000",
                           bg = def_bg)

CreateUsernameLabel = Label(
     createaccountframe,
     text = "Username",
     font = (def_font, 13),
     bg = def_bg,
     fg = "#000000"
)
CreateUsernameLabel2 = Label(
     createaccountframe,
     text = "Must be at least 5 characters long and not contain spaces.",
     font = (def_font, 9),
     bg = def_bg,
     fg = "#000000"
)
CreateUsernameEntry = Entry(
     createaccountframe,
     font = (def_font, 28),
     bg = "#ffffff",
     fg = "#000000",
     insertbackground="#000000",
     width = 50
)

CreatePasswordLabel = Label(
     createaccountframe,
     text = "Password",
     font = (def_font, 13),
     bg = def_bg,
     fg = "#000000"
)
CreatePasswordLabel2 = Label(
     createaccountframe,
     text = "Must be at least eight characters, including one uppercase, and one number.",
     font = (def_font, 9),
     bg = def_bg,
     fg = "#000000"
)
CreatePasswordEntry = Entry(
     createaccountframe,
     font = (def_font, 28),
     bg = "#ffffff",
     fg = "#000000",
     insertbackground="#000000",
     width = 50
)

CreateRemembranceLabel = Label(
     createaccountframe,
     text = "Remembrance Word",
     font = (def_font, 13),
     bg = def_bg,
     fg = "#000000"
)
CreateRemembranceLabel2 = Label(
     createaccountframe,
     text = "This will help you reset your pasword if forgotten. Must be at least 5 characters long.",
     font = (def_font, 9),
     bg = def_bg,
     fg = "#000000"
)
CreateRemembranceEntry = Entry(
     createaccountframe,
     font = (def_font, 28),
     bg = "#ffffff",
     fg = "#000000",
     insertbackground="#000000",
     width = 50
)

ActualCreateAccountButton = Button(
     createaccountframe,
     text = "Create Account",
     font = (def_font, 20),
     fg = "#000000",
     bg = "#BDECFA",
     width = 35,
     padx = 10,
     activebackground = "#ffffff",
     borderless = 1,
     command = validateCreateAccount

)

CreateAccountLabel.grid(row = 0, column = 2, padx = 20, pady = (10, 30), columnspan = 4)

CreateUsernameLabel.grid(row = 1, column = 2, sticky = "w", padx = (37,0), pady = (15,0))
CreateUsernameLabel2.grid(row = 1, column = 2, sticky = "e", padx = (0,40))
CreateUsernameEntry.grid(row = 2, column = 2, padx = 40, pady = (0, 30))

CreatePasswordLabel.grid(row = 3, column = 2, sticky = "w", padx = (37,0), pady = (15,0))
CreatePasswordLabel2.grid(row = 3, column = 2, sticky = "e", padx = (0,40))
CreatePasswordEntry.grid(row = 4, column = 2, padx = 40, pady = (0, 30))

CreateRemembranceLabel.grid(row = 5, column = 2, sticky = "w", padx = (37,0), pady = (15,0))
CreateRemembranceLabel2.grid(row = 5, column = 2, sticky = "e", padx = (0,40))
CreateRemembranceEntry.grid(row = 6, column = 2, padx = 40, pady = (0, 30))

ActualCreateAccountButton.grid(row = 7, column = 2, pady = (15,30), sticky = "ew", padx = 60)
#<------------------>#
#<------------------>#


#<Y------------------Y>#
#<Y---------Widgets for Forgot Password Page---------Y>#

forgotpasswordframe = Frame(
     startup,
     bg = def_bg,
     highlightthickness = 2,
     highlightbackground = "#000000")

ForgotPasswordLabel = Label(
     forgotpasswordframe,
     text = "Reset Password",
     font = (def_font, 30),
     fg = "#000000",
     bg = def_bg
)

ForgotUsernameLabel = Label(
     forgotpasswordframe,
     text = "Username",
     font = (def_font, 13),
     bg = def_bg,
     fg = "#000000"
)
ForgotUsernameEntry = Entry(
     forgotpasswordframe,
     font = (def_font, 28),
     bg = "#ffffff",
     fg = "#000000",
     insertbackground="#000000",
     width = 50
)

ForgotCreatePasswordLabel = Label(
     forgotpasswordframe,
     text = "Password",
     font = (def_font, 13),
     bg = def_bg,
     fg = "#000000"
)
ForgotCreatePasswordLabel2 = Label(
     forgotpasswordframe,
     text = "Must be at leat eight characters, including one uppercase, and one number.",
     font = (def_font, 9),
     bg = def_bg,
     fg = "#000000"
)
ForgotCreatePasswordEntry = Entry(
     forgotpasswordframe,
     font = (def_font, 28),
     bg = "#ffffff",
     fg = "#000000",
     insertbackground="#000000",
     width = 50,
     state = NORMAL
)

ForgotRemembranceLabel = Label(
     forgotpasswordframe,
     text = "Remembrance Word",
     font = (def_font, 13),
     bg = def_bg,
     fg = "#000000"
)
ForgotRemembranceEntry = Entry(
     forgotpasswordframe,
     font = (def_font, 28),
     bg = "#ffffff",
     fg = "#000000",
     insertbackground="#000000",
     width = 50
)

ActualResetPasswordButton = Button(
     forgotpasswordframe,
     text = "Reset Password",
     font = (def_font, 20),
     fg = "#000000",
     width = 30,
     padx = 10,
     bg = "#FECDFF",
     activebackground = "#FFFFFF",
     borderless = 1,
     command = ResetPassword,
     state = NORMAL

)

ForgotPasswordLabel.grid(row = 0, column = 2, padx = 20, pady = (10, 30), columnspan = 4)

ForgotUsernameLabel.grid(row = 1, column = 2, sticky = "w", padx = (37,0), pady = (15,0))
ForgotUsernameEntry.grid(row = 2, column = 2, padx = 40, pady = (0, 30))

ForgotRemembranceLabel.grid(row = 3, column = 2, sticky = "w", padx = (37,0), pady = (15,0))
ForgotRemembranceEntry.grid(row = 4, column = 2, padx = 40, pady = (0, 30))

CreatePasswordLabel.grid(row = 3, column = 2, sticky = "w", padx = (37,0), pady = (15,0))
CreatePasswordEntry.grid(row = 4, column = 2, padx = 40, pady = (0, 30))

ActualResetPasswordButton.grid(row = 7, column = 2, pady = (15,30), padx = 60, sticky = "ew")

ForgotCreatePasswordLabel.grid(row = 5, column = 2, sticky = "w", padx = (37,0), pady = (15,0))
ForgotCreatePasswordLabel2.grid(row = 5, column = 2, sticky = "e", padx = (0,40))
ForgotCreatePasswordEntry.grid(row = 6, column = 2, padx = 40, pady = (0, 30))

#<Y------------------Y>#


#^^^^^HOMEPAGE STUFF^^^^^#

img = Image.open("icon.png")
img = img.resize((60, 60))

homeicon = ImageTk.PhotoImage(img)

homepageframe = Frame(
     startup,
     bg = def_bg,
     highlightthickness = 0,
     highlightbackground = "#000000",
     width = width,
     height = height
)

button_frame = Frame(
        homepageframe,
        bg = def_bg
)

todoframe = Frame(
        homepageframe,
        bg = "#BDECFA",
        highlightthickness = 1,
        highlightbackground = "#000000"
        )

todoLabel = Label(
     todoframe,
     text = "To-Do List",
     bg = "#BDECFA",
     font = (def_font, 30, "underline"),
     fg = "#000000"
)

AddEntryButton = Button(
     button_frame,
     text = "Add Entry",
     command = open_addentry_window,
     font = (def_font, 18, "bold"),
     bg="#C8FFB8",
     activebackground="#B2F2A3",
     borderless = 1,
     bd = 0,
     padx = 25,
     pady = 20
)

EditEntryButton = Button(
     button_frame,
     text = "Edit Entry",
     command = open_editentry_window,
     font = (def_font, 18, "bold"),
     bg="#C8FFB8",
     activebackground="#B2F2A3",
     borderless = 1,
     bd = 0,
     padx = 25,
     pady = 20
)

ViewEntryButton = Button(
     button_frame,
     text = "View Entry",
     command = open_viewentry_window,
     font = (def_font, 18, "bold"),
     bg="#C8FFB8",
     activebackground="#B2F2A3",
     borderless = 1,
     bd = 0,
     padx = 25,
     pady = 20
)

IconLabel = Button(
     button_frame,
     image = homeicon,
     bg = def_bg,
     width = 70,
     height = 70,
     borderless = 1,
     borderwidth = 0,
     activebackground = "#FFFFFF",
     command = LogOut
)


IconLabel.grid(row = 0, column = 0, pady = (20, 10), padx = (0, 60), sticky = "w")
AddEntryButton.grid(row=0, column=2, padx=20)
ViewEntryButton.grid(row=0, column=3, padx=20)
EditEntryButton.grid(row=0, column=4, padx=20)

button_frame.grid(row=1, column=0, pady=20)

startup.grid_rowconfigure(0, weight=1)
startup.grid_columnconfigure(0, weight=1)

#homepageframe.grid(row = 0, column = 0, sticky = "nsew", padx = 40, pady = (20, 30))
homepageframe.grid_columnconfigure(0, weight=1)
homepageframe.grid_rowconfigure(3, weight=1)

todoframe.grid(row = 3, column = 0, columnspan = 3, sticky = "nsew")
todoframe.grid_columnconfigure(0, weight = 1)
todoframe.grid_rowconfigure(0, weight = 1)
todoLabel.grid(row = 0, column= 0, sticky = "n")



#STARTING THE PROGRAM
loginframe.place(relx=0.5, rely = 0.5, anchor = CENTER)
startup.mainloop()
