import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import numpy as np
from datetime import datetime

# Define the Student class
class Student:
    def __init__(self, name, student_id, password, email, phone_number):
        self.id = student_id
        self.name = name
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.feedback = None  # Added feedback attribute

    def __repr__(self):
        return (f"Student(id={self.id}, name={self.name}, email={self.email}, "
                f"phone_number={self.phone_number})")

# Define the Admin class
class Admin:
    def __init__(self, username, password, email, phone_number):
        self.username = username
        self.password = password
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return (f"Admin(username={self.username}, email={self.email}, "
                f"phone_number={self.phone_number})")

# Define the Grievance class
class Grievance:
    def __init__(self, student_id, grievance_type, description, college_name):
        self.student_id = student_id
        self.grievance_type = grievance_type
        self.description = description
        self.college_name = college_name
        self.status = 'Pending'
        self.submitted_at = datetime.now()
        self.resolved_at = None
        self.feedback = None

    def update_status(self, new_status):
        if new_status not in ['Pending', 'In Progress', 'Resolved']:
            raise ValueError("Invalid status")
        self.status = new_status
        if new_status == 'Resolved':
            self.resolved_at = datetime.now()

    def add_feedback(self, feedback):
        self.feedback = feedback

    def __repr__(self):
        return (f"Grievance(student_id={self.student_id}, type={self.grievance_type}, "
                f"status={self.status}, college_name={self.college_name}, feedback={self.feedback})")

# Define the StudentGrievanceCell class
class StudentGrievanceCell:
    def __init__(self):
        self.grievances = []
        self.students = []
        self.admins = []
        self.existing_ids = set()

    def generate_student_id(self):
        while True:
            student_id = np.random.randint(100000, 999999)  # Generate a 6-digit ID
            if student_id not in self.existing_ids:
                self.existing_ids.add(student_id)
                return student_id

    def register_student(self, name, password, email, phone_number):
        student_id = self.generate_student_id()
        student = Student(name, student_id, password, email, phone_number)
        self.students.append(student)
        return student_id

    def register_admin(self, username, password, email, phone_number):
        admin = Admin(username, password, email, phone_number)
        self.admins.append(admin)
        return admin

    def authenticate_student(self, student_id, password):
        for student in self.students:
            if student.id == student_id and student.password == password:
                return student
        return None

    def authenticate_admin(self, username, password):
        for admin in self.admins:
            if admin.username == username and admin.password == password:
                return admin
        return None

    def view_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def submit_grievance(self, student_id, grievance_type, description, college_name):
        student = self.view_student(student_id)
        if not student:
            raise ValueError("Invalid student ID")
        grievance = Grievance(student_id, grievance_type, description, college_name)
        self.grievances.append(grievance)
        return grievance

    def view_grievances_by_student(self, student_id):
        return [g for g in self.grievances if g.student_id == student_id]

    def update_grievance_status(self, student_id, new_status, college_name):
        grievances = self.view_grievances_by_student(student_id)
        if not grievances:
            raise ValueError("No grievances found for this student ID")
        for grievance in grievances:
            if grievance.college_name != college_name:
                raise ValueError("College name does not match")
            grievance.update_status(new_status)
        return True

    def update_grievance_feedback(self, student_id, feedback, college_name):
        grievances = self.view_grievances_by_student(student_id)
        if not grievances:
            raise ValueError("No grievances found for this student ID")
        for grievance in grievances:
            if grievance.college_name != college_name:
                raise ValueError("College name does not match")
            grievance.add_feedback(feedback)
        return True

    def list_grievances(self, status=None):
        if status:
            return [g for g in self.grievances if g.status == status]
        return self.grievances

    def generate_report(self):
        report = {
            'total_grievances': len(self.grievances),
            'pending': len(self.list_grievances('Pending')),
            'in_progress': len(self.list_grievances('In Progress')),
            'resolved': len(self.list_grievances('Resolved')),
        }
        return report

# Define the GUI Application class
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Grievance Redressal System")
        self.geometry("490x300")  # Increased window size

        self.cell = StudentGrievanceCell()
        self.logged_in_student = None
        self.logged_in_admin = None

        # Register a default admin (only for the initial run)
        if not self.cell.admins:
            self.cell.register_admin('admin', 'adminpassword', 'admin@example.com', '1234567890')

        self.frames = {}
        for F in (MainMenu, StudentMenu, AdminMenu, StudentLoggedInMenu, AdminLoggedInMenu):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_cell(self):
        return self.cell

    def set_logged_in_student(self, student):
        self.logged_in_student = student

    def get_logged_in_student(self):
        return self.logged_in_student

    def set_logged_in_admin(self, admin):
        self.logged_in_admin = admin

    def get_logged_in_admin(self):
        return self.logged_in_admin

# Define the frames
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#f0f8ff')  # Light blue background

        tk.Label(self, text="--- Main Menu ---", font=("Arial", 20), bg='#f0f8ff').pack(pady=20)

        tk.Button(self, text="Student", command=lambda: controller.show_frame("StudentMenu"), bg='#add8e6', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Admin", command=lambda: controller.show_frame("AdminMenu"), bg='#add8e6', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Exit", command=self.quit, bg='#ff6347', font=("Arial", 14)).pack(pady=10)

class StudentMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#e6ffe6')  # Light green background

        tk.Label(self, text="--- Student Grievance Redressal Cell ---", font=("Arial", 20), bg='#e6ffe6').pack(pady=20)

        tk.Button(self, text="Register New Student", command=self.register_student, bg='#90ee90', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Login", command=self.login, bg='#90ee90', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("MainMenu"), bg='#ff6347', font=("Arial", 14)).pack(pady=10)

    def register_student(self):
        name = simpledialog.askstring("Register", "Enter Student Name:")
        password = simpledialog.askstring("Register", "Enter Password:")
        email = self.get_text_input("Register", "Enter Email:")
        phone_number = simpledialog.askstring("Register", "Enter Phone Number:")
        if name and password and email and phone_number:
            student_id = self.controller.get_cell().register_student(name, password, email, phone_number)
            messagebox.showinfo("Registration", f"Student registered successfully. ID: {student_id}")

    def login(self):
        student_id = simpledialog.askinteger("Login", "Enter Student ID:")
        password = simpledialog.askstring("Login", "Enter Password:")
        student = self.controller.get_cell().authenticate_student(student_id, password)
        if student:
            self.controller.set_logged_in_student(student)
            self.controller.show_frame("StudentLoggedInMenu")
        else:
            messagebox.showerror("Login", "Invalid ID or password.")

    def get_text_input(self, title, prompt):
        """ Opens a dialog for multi-line text input with scrollbars. """
        dialog = tk.Toplevel(self)
        dialog.title(title)

        tk.Label(dialog, text=prompt).pack(pady=5)

        text_widget = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=60, height=4)
        text_widget.pack(padx=10, pady=10)

        def submit():
            dialog.result = text_widget.get("1.0", tk.END).strip()
            dialog.destroy()

        tk.Button(dialog, text="Submit", command=submit).pack(pady=5)

        dialog.wait_window()
        return getattr(dialog, 'result', '')

class AdminMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#ffe6e6')  # Light pink background

        tk.Label(self, text="--- Admin Menu ---", font=("Arial", 18), bg='#ffe6e6').pack(pady=20)

        tk.Button(self, text="Register New Admin", command=self.register_admin, bg='#ffb6c1', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Login", command=self.login, bg='#ffb6c1', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("MainMenu"), bg='#ff6347', font=("Arial", 14)).pack(pady=10)

    def register_admin(self):
        username = simpledialog.askstring("Register", "Enter Admin Username:")
        password = simpledialog.askstring("Register", "Enter Password:")
        email = self.get_text_input("Register", "Enter Email:")
        phone_number = simpledialog.askstring("Register", "Enter Phone Number:")
        if username and password and email and phone_number:
            admin = self.controller.get_cell().register_admin(username, password, email, phone_number)
            messagebox.showinfo("Registration", f"Admin registered successfully. Username: {admin.username}")

    def login(self):
        username = simpledialog.askstring("Login", "Enter Admin Username:")
        password = simpledialog.askstring("Login", "Enter Password:")
        admin = self.controller.get_cell().authenticate_admin(username, password)
        if admin:
            self.controller.set_logged_in_admin(admin)
            self.controller.show_frame("AdminLoggedInMenu")
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def get_text_input(self, title, prompt):
        """ Opens a dialog for multi-line text input with scrollbars. """
        dialog = tk.Toplevel(self)
        dialog.title(title)

        tk.Label(dialog, text=prompt).pack(pady=5)

        text_widget = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=60, height=4)
        text_widget.pack(padx=10, pady=10)

        def submit():
            dialog.result = text_widget.get("1.0", tk.END).strip()
            dialog.destroy()

        tk.Button(dialog, text="Submit", command=submit).pack(pady=5)

        dialog.wait_window()
        return getattr(dialog, 'result', '')

class StudentLoggedInMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#e6f9ff')  # Light cyan background

        tk.Label(self, text="--- Student Logged In Menu ---", font=("Arial", 18), bg='#e6f9ff').pack(pady=20)

        tk.Button(self, text="Submit Grievance", command=self.submit_grievance, bg='#b0e0e6', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="View My Details", command=self.view_details, bg='#b0e0e6', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Update Feedback", command=self.update_feedback, bg='#b0e0e6', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout, bg='#ff6347', font=("Arial", 14)).pack(pady=10)

    def submit_grievance(self):
        student_id = self.controller.get_logged_in_student().id
        grievance_type = simpledialog.askstring("Submit Grievance", "Enter Grievance Type(Academic/Health/Library/Other):")
        description = self.get_text_input("Submit Grievance", "Enter Description:")
        college_name = simpledialog.askstring("Submit Grievance", "Enter College Name:")
        if grievance_type and description and college_name:
            grievance = self.controller.get_cell().submit_grievance(student_id, grievance_type, description, college_name)
            messagebox.showinfo("Grievance Submitted", "Grievance submitted successfully.")

    def get_text_input(self, title, prompt):
        """ Opens a dialog for multi-line text input with scrollbars. """
        dialog = tk.Toplevel(self)
        dialog.title(title)

        tk.Label(dialog, text=prompt).pack(pady=5)

        text_widget = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=60, height=10)
        text_widget.pack(padx=10, pady=10)

        def submit():
            dialog.result = text_widget.get("1.0", tk.END).strip()
            dialog.destroy()

        tk.Button(dialog, text="Submit", command=submit).pack(pady=5)

        dialog.wait_window()
        return getattr(dialog, 'result', '')

    def view_details(self):
        student = self.controller.get_logged_in_student()
        grievances = self.controller.get_cell().view_grievances_by_student(student.id)
        grievance_details = "\n".join(f"Grievance Type: {g.grievance_type}\nDescription: {g.description}\nStatus: {g.status}\nCollege: {g.college_name}\nFeedback: {g.feedback if g.feedback else 'None'}\n" for g in grievances)
        details = (f"Name: {student.name}\n"
                   f"ID: {student.id}\n"
                   f"Email: {student.email}\n"
                   f"Phone Number: {student.phone_number}\n\n"
                   f"Grievances:\n{grievance_details}")
        messagebox.showinfo("Student Details", details)

    def update_feedback(self):
        student = self.controller.get_logged_in_student()
        grievances = self.controller.get_cell().view_grievances_by_student(student.id)
        if not grievances:
            messagebox.showinfo("No Grievances", "You have no grievances to provide feedback for.")
            return

        grievance_type = simpledialog.askstring("Update Feedback", "Enter Grievance Type to Update Feedback(Academic/Health/Library/Other):")
        for grievance in grievances:
            if grievance.grievance_type == grievance_type:
                new_feedback = self.get_text_input("Update Feedback", "Enter New Feedback:")
                if new_feedback:
                    self.controller.get_cell().update_grievance_feedback(student.id, new_feedback, grievance.college_name)
                    messagebox.showinfo("Feedback Updated", "Feedback updated successfully.")
                return

        messagebox.showerror("Error", "No grievance found with the given type.")

    def logout(self):
        self.controller.set_logged_in_student(None)
        self.controller.show_frame("MainMenu")

class AdminLoggedInMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#fff5e6')  # Light peach background

        tk.Label(self, text="--- Admin Logged In Menu ---", font=("Arial", 18), bg='#fff5e6').pack(pady=20)

        tk.Button(self, text="Update Grievance Status", command=self.update_grievance_status, bg='#ffd700', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="View Grievances", command=self.view_grievances, bg='#ffd700', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Generate Report", command=self.generate_report, bg='#ffd700', font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout, bg='#ff6347', font=("Arial", 14)).pack(pady=10)

    def update_grievance_status(self):
        student_id = simpledialog.askinteger("Update Status", "Enter Student ID:")
        new_status = simpledialog.askstring("Update Status", "Enter New Status (Pending, In Progress, Resolved):")
        college_name = simpledialog.askstring("Update Status", "Enter College Name:")
        if student_id and new_status and college_name:
            try:
                self.controller.get_cell().update_grievance_status(student_id, new_status, college_name)
                messagebox.showinfo("Status Updated", "Grievance status updated successfully.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def view_grievances(self):
        grievances = self.controller.get_cell().list_grievances()
        grievances_details = "\n".join(f"Student ID: {g.student_id}\nType: {g.grievance_type}\nDescription: {g.description}\nStatus: {g.status}\nCollege: {g.college_name}\nFeedback: {g.feedback if g.feedback else 'None'}\n" for g in grievances)
        messagebox.showinfo("Grievances", grievances_details if grievances else "No grievances found.")

    def generate_report(self):
        report = self.controller.get_cell().generate_report()
        report_details = (f"Total Grievances: {report['total_grievances']}\n"
                          f"Pending: {report['pending']}\n"
                          f"In Progress: {report['in_progress']}\n"
                          f"Resolved: {report['resolved']}")
        messagebox.showinfo("Report", report_details)

    def logout(self):
        self.controller.set_logged_in_admin(None)
        self.controller.show_frame("MainMenu")

# Run the application
if __name__ == "__main__":
    app = Application()
    app.mainloop()


