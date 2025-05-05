import customtkinter
import sys
import os
from tkinter import messagebox
from customtkinter import CTkImage  # Import CTkImage
from PIL import Image, ImageTk, ImageDraw
sys.path.append(os.path.abspath("C:\\Users\\tallyta\\Documents\\GitHub\\tkinter-event-planner"))

#Importing registration GUI
from registration import App as RegistrationGUI

customtkinter.set_appearance_mode("dark")  # Set appearance mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("EVENT PLANNER") #Title of the form
        self.geometry("690x270") #dimensions of the form

        # Call the function to create the form and image
        self.create_login_form()

    '''creating a function to direct user to the registration form'''
    def toggleToRegistration(self, event):
        #Code to remove current GUI
        self.destroy()

        self.regGUI = RegistrationGUI()#created instance of registration Gui
        self.regGUI.mainloop()#this will run the GUI
    
    '''Creating function to drect user to event planner GUI'''
    
    def to_event_planner_section(self):
        from frontend.pages.eventplanner_section import App as eventPlannerGUI
        # Code to remove current GUI
        self.destroy()  # Corrected from destory() to destroy()

        self.event_planner_gui = eventPlannerGUI()  # Create instance of eventPlannerGUI
        self.event_planner_gui.mainloop()  # This will run the GUI
    
    '''Fabricated function to direct user to event planner form, if password matches database values'''
    def login_Authentication(self, email, password):  # Add self as the first parameter
        if email == "johndoe123@gmail.com" and password == "P@ssword123":
            messagebox.showwarning("Successful Login", "Directing you to main page")

            # ESTABLISHING CODE TO DIRECT TO EVENT PLANNER
            self.to_event_planner_section()  # Call the method on the current instance
            
        else:
            messagebox.showerror("Error Occurred", "Password or email does not exist!")

    def create_login_form(self):

        '''functions for determine the hover in and out of a label'''
        def on_enter_label(event):
            self.toRegistration_lbl.configure(text_color="white")

        def on_leave_label(event):
            self.toRegistration_lbl.configure(text_color="gray")

        # Create a frame for the form
        form_frame = customtkinter.CTkFrame(self, width=100)  # Set width and height
        form_frame.grid(row=0, column=0, padx=20, pady=20)


        form_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

         # Heading Label
        self.formTitle = customtkinter.CTkLabel(form_frame, text="Login", font=("", 25))
        self.formTitle.grid(row=0, columnspan=2, padx=10, pady=10)

        self.email_input = customtkinter.CTkEntry(form_frame, placeholder_text="Email" ,corner_radius=20,
                                                  width=300, border_width=0) #Setting the fistname input to the Frame
        self.email_input.grid(row=2, columnspan=2, padx=10, pady=10)

        self.password_input = customtkinter.CTkEntry(form_frame, placeholder_text="Password" ,corner_radius=20,
                                                     show="*", width=300, border_width=0) #Setting the fistname input to the Frame
        self.password_input.grid(row=3,columnspan=2, padx=10, pady=10)

        # Create a submit button
        self.submit_button = customtkinter.CTkButton(form_frame, text="Login",
                                                    width=300,command=self.submit_form)
        self.submit_button.grid(row=5, columnspan=2, pady=20)

        #Text to direct user to login form
        self.toRegistration_lbl = customtkinter.CTkLabel(form_frame, text="Don't have an Account? Register", font=("", 12), text_color="gray")
        self.toRegistration_lbl.grid(row=5, columnspan=2, pady=(60, 0 ))

        

        #Binding hover event to loginlabel
        self.toRegistration_lbl.bind("<Enter>", on_enter_label)
        self.toRegistration_lbl.bind("<Leave>", on_leave_label)

        # Bind the click event to the label
        self.toRegistration_lbl.bind("<Button-1>", self.toggleToRegistration)

        # Load and display an image
        self.display_image()

    def display_image(self):
        # Load an image using PIL
        image = Image.open("frontend/src/assests/eventplanner_img_login.png")  # Replace with your image path
        rounded_image = self.create_rounded_image(image, (270, 230), 5)  # Create rounded image
        
        # Convert the rounded PIL image to PhotoImage
        self.photo = ImageTk.PhotoImage(rounded_image)

        # Create a label to display the image
        image_label = customtkinter.CTkLabel(self, image=self.photo, corner_radius=200, text="")
        image_label.grid(row=0, column=1, padx=20, pady=20)
        
    '''Function creates rounded edge of image'''
    def create_rounded_image(self, image, size, corner_radius):
        image = image.resize(size, Image.LANCZOS)  # Resize image

        # Create a mask for rounded corners
        mask = Image.new("L", size, 0)  # Create a new mask
        draw = ImageDraw.Draw(mask)  # Create a drawing context
        draw.rounded_rectangle((0, 0, size[0], size[1]), radius=corner_radius, fill=255)  # Draw rounded rectangle

        # Apply the mask to the image
        rounded_image = Image.new("RGBA", size)  # Create a new image with alpha channel
        rounded_image.paste(image, (0, 0))  # Paste the original image
        rounded_image.putalpha(mask)  # Apply the mask

        return rounded_image

    def submit_form(self):
        from error.error_handeling import is_required_email, is_email_domained,is_required_password_login, is_blank_login
        # Logic to handle registration
        email = self.email_input.get()
        password = self.password_input.get()

        # Logic to handle registration
        is_blank_login(email) # Function | check if email is null
        is_blank_login(password) # Function | check if email is null

        is_email_domained(email) #Function | Checks if email has a domain
        is_required_email(email) #Function | Checks if email has required content
        
        is_required_password_login(password) #Function | Checks if password  has required content

        '''calling function to direct user to event planer Gui'''
        self.login_Authentication(email, password)

if __name__ == "__main__":
    app = App()
    app.mainloop()