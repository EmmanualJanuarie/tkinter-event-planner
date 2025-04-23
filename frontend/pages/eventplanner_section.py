import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

#Importing registration GUI
from registration import App as RegistrationGUI

customtkinter.set_appearance_mode("dark")  # Set appearance mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("EVENT PLANNER") #Title of the form
        self.geometry("1090x570") #dimensions of the form

        self.create_event_planner_GUI()

    
    '''creating function to render in the creation of the event planner GUI'''
    def create_event_planner_GUI(self):
        # Create a frame for the header
        form_frame_header = customtkinter.CTkFrame(self, width=100, height=480)  # Set width and height
        form_frame_header.pack(padx=20, pady=20, fill='x')  # Use pack to stack vertically

        form_frame_header.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

        # Create a frame for the footer
        form_frame_footer = customtkinter.CTkFrame(self, width=200, height=40)  # Set width and height
        form_frame_footer.pack(padx=20, pady=(0,0), fill='x')  # Use pack to stack vertically



if __name__ == "__main__":
    app = App()
    app.mainloop()