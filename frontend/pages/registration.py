import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

customtkinter.set_appearance_mode("dark")  # Set appearance mode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CODE FOR MAIN WINDOW
        self.title("EVENT PLANNER") #Title of the form
        self.geometry("730x350") #dimensions of the form

        # Call the function to create the form and image
        self.create_registration_form()

    def create_registration_form(self):

        '''functions for determine the hover in and out of a label'''
        def on_enter_label(event):
            self.toLogin_lbl.configure(text_color="white")

        def on_leave_label(event):
            self.toLogin_lbl.configure(text_color="gray")

        # Create a frame for the form
        form_frame = customtkinter.CTkFrame(self, width=100)  # Set width and height
        form_frame.grid(row=0, column=1, padx=20, pady=20)


        form_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

         # Heading Label
        self.formTitle = customtkinter.CTkLabel(form_frame, text="Register", font=("", 25))
        self.formTitle.grid(row=0, columnspan=2, padx=10, pady=10)

        # Create labels and entry fields for user input
        self.first_name_input = customtkinter.CTkEntry(form_frame, placeholder_text="First Name" ,corner_radius=20,
                                                       border_width=0) #Setting the fistname input to the Frame
        self.first_name_input.grid(row=1, column=0, padx=10, pady=10)

        self.last_name_input = customtkinter.CTkEntry(form_frame, placeholder_text="Last Name" ,corner_radius=20, border_width=0,
                                                      border_color="gray") #Setting the fistname input to the Frame
        self.last_name_input.grid(row=1, column=1, padx=10, pady=5)

        self.email_input = customtkinter.CTkEntry(form_frame, placeholder_text="Email" ,corner_radius=20,
                                                  width=300, border_width=0) #Setting the fistname input to the Frame
        self.email_input.grid(row=2, columnspan=2, padx=10, pady=10)

        self.password_input = customtkinter.CTkEntry(form_frame, placeholder_text="Password" ,corner_radius=20,
                                                     show="*", width=300, border_width=0) #Setting the fistname input to the Frame
        self.password_input.grid(row=3,columnspan=2, padx=10, pady=10)

        self.con_password_input = customtkinter.CTkEntry(form_frame, placeholder_text="Confirm Password" ,corner_radius=20,
                                                     show="*", width=300, border_width=0) #Setting the fistname input to the Frame
        self.con_password_input.grid(row=4,columnspan=2, padx=10, pady=5)

        # Create a submit button
        self.submit_button = customtkinter.CTkButton(form_frame, text="Register",
                                                    width=300,command=self.submit_form)
        self.submit_button.grid(row=5, columnspan=2, pady=20)

        #Text to direct user to login form
        self.toLogin_lbl = customtkinter.CTkLabel(form_frame, text="Direct to Login", font=("", 12), text_color="gray", )
        self.toLogin_lbl.grid(row=5, columnspan=2, pady=(60, 0 ))

        

        #Binding hover event to loginlabel
        self.toLogin_lbl.bind("<Enter>", on_enter_label)
        self.toLogin_lbl.bind("<Leave>", on_leave_label)

        # Load and display an image
        self.display_image()

    def display_image(self):
        # Load an image using PIL
        image = Image.open("frontend/src/assests/eventplanner_img.png")  # Replace with your image path
        rounded_image = self.create_rounded_image(image, (310, 310), 5)  # Create rounded image
        self.photo = ImageTk.PhotoImage(rounded_image)

        # Create a label to display the image
        image_label = customtkinter.CTkLabel(self,image=self.photo, corner_radius=200)
        image_label.grid(row=0,column=0, padx=20, pady=20)

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
        # Logic to handle registration
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Here you can add logic to save the data or validate it
        messagebox.showinfo("Registration", f"Registered: {first_name} {last_name}, Email: {email}")

if __name__ == "__main__":
    app = App()
    app.mainloop()