import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

# Importing registration GUI
from registration import App as RegistrationGUI

customtkinter.set_appearance_mode("dark")  # Set appearance mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("EVENT PLANNER")  # Title of the form
        self.geometry("1090x519")  # dimensions of the form

        self.create_event_planner_GUI()
    
    '''function to logout user'''
    def logout_User(self):
        # Importing login GUI
        from login import App as LoginGUI
        mesg_answer = messagebox.askyesnocancel("Attention", "Are you sure you want to logout?")

        if mesg_answer:
            # Code to remove current GUI
            self.destroy()
            self.loginGUI = LoginGUI()  # created instance of registration GUI
            self.loginGUI.mainloop()  # this will run the GUI


       

    '''creating function to render in the creation of the event planner GUI'''
    def create_event_planner_GUI(self):

        '''functions for determine the hover in and out of a label'''
        def on_enter_label(label):
            label.configure(fg_color="gray", bg_color="#2b2b2b", corner_radius=5)  # Change background and border color on hover

        def on_leave_label(label):
            label.configure(fg_color="transparent", bg_color="transparent", corner_radius=5)  # Reset background and border color

        # Create a frame for the navigation (left column)
        form_frame_nav = customtkinter.CTkFrame(self, width=200, height=500)  # Set width and height
        form_frame_nav.grid(row=0, column=0, padx=(5, 5), pady=10, sticky="nsew")  # Reduced padx for left frame

        # Create a frame for the content (right column)
        form_frame_content = customtkinter.CTkFrame(self, width=900, height=500)  # Set width and height
        form_frame_content.grid(row=0, column=1, padx=(5, 5), pady=10, sticky="nsew")  # Reduced padx for right frame

        # Add vertically stacked labels in the navigation frame
        self.label_dashboard = customtkinter.CTkLabel(form_frame_nav, text="Dashboard", width=2, corner_radius=10)
        self.label_dashboard.pack(pady=(10, 0), padx=50)  # Add some vertical padding

        self.label_events = customtkinter.CTkLabel(form_frame_nav, text="Events", width=2, corner_radius=10)
        self.label_events.pack(pady=(5, 0), padx=50)  # Add some vertical padding

        self.label_another = customtkinter.CTkLabel(form_frame_nav, text="Another", width=2, corner_radius=10)
        self.label_another.pack(pady=(5, 0), padx=50)  # Add some vertical padding

         # Create a submit button
        self.submit_button = customtkinter.CTkButton(form_frame_nav, text="Logout",
                                                    width=100,command=self.logout_User)
        self.submit_button.pack(pady=(350, 0), padx=50)


        # Binding hover event to labels
        self.label_dashboard.bind("<Enter>", lambda event: on_enter_label(self.label_dashboard))
        self.label_dashboard.bind("<Leave>", lambda event: on_leave_label(self.label_dashboard))

        self.label_events.bind("<Enter>", lambda event: on_enter_label(self.label_events))
        self.label_events.bind("<Leave>", lambda event: on_leave_label(self.label_events))

        self.label_another.bind("<Enter>", lambda event: on_enter_label(self.label_another))
        self.label_another.bind("<Leave>", lambda event: on_leave_label(self.label_another))

        # Configure grid weights to make the columns expand proportionally
        self.grid_columnconfigure(0, weight=1)  # Left column (navigation)
        self.grid_columnconfigure(1, weight=4)  # Right column (content)

if __name__ == "__main__":
    app = App()
    app.mainloop()