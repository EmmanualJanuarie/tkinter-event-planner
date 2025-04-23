from tkinter import messagebox
import re

import re #Importing regular expression to check for numbers in text and other purposes
'''Creating functions for form validation'''

def is_none(text):
    return text is None

#detect if user enters a number instead of text
def is_Number(text):
    if re.search(r'[0-9]', text): # checks to see if the text is a number
        messagebox.showwarning("Warning", "First or last name field(s) can't contain numbers!")

def is_Number(text1, text2):
    if re.search(r'[0-9]', text1) or re.search(r'[0-9]', text2): # checks to see if the text is a number
        messagebox.showwarning("Warning", "First or last name field(s) can't contain numbers!")

#detect if user leaves input blank
def is_blank(text):
    if is_none(text):#Checks to see if the input is blank
       messagebox.showwarning("Input Error", "Input Field(s) cant be blank!")

def is_blank(text1, text2, text3, text4, text5):
    # Check if any of the inputs are None or empty
    if text1 is None or text2 is None or text3 is None or text4 is None or text5 is None or \
       (isinstance(text1, str) and text1.strip() == "") or \
       (isinstance(text2, str) and text2.strip() == "") or \
       (isinstance(text3, str) and text3.strip() == "") or \
       (isinstance(text4, str) and text4.strip() == "") or \
       (isinstance(text5, str) and text5.strip() == ""):
        messagebox.showwarning("Input Error", "Input Field(s) can't be blank!")
        return True  # Indicate that there was an empty input
    return False  # All inputs are valid

#detect if users does not enter the correct password requirements
def is_required_password(password_text):
    # Define the regex pattern
    # This pattern matches any character that is not a letter, digit, space, or the allowed special characters (@, _, -)
    pattern = r'[^a-zA-Z0-9 @]'

    if len(password_text) < 8: #checking if password text contains more than 8 chracters
       messagebox.showwarning("Warning", "Password must be greater than 8 characters!")
    elif not re.search(r'\d', password_text): #checking if password text contains numbers
        messagebox.showwarning("Warning", "Password must contains numbers!")
    elif not re.search(pattern, password_text):
        messagebox.showwarning("Warning", "Password must contain special characters (allowed '@')")
    elif not re.search(r'[A-Z]', password_text):
        messagebox.showwarning("Warning", "Password must atleast contain two or more upercase chatacters")
    else:
        return password_text
    
def is_required_password(password_text1, password_text2):
    # Define the regex pattern for allowed characters
    pattern = r'[^a-zA-Z0-9@]'

    # Check if both passwords are at least 8 characters long
    if len(password_text1) < 8 or len(password_text2) < 8:
        messagebox.showwarning("Warning", "Password must be greater than 8 characters!")
        return None

    # Check if both passwords contain at least one digit
    if not re.search(r'\d', password_text1) or not re.search(r'\d', password_text2):
        messagebox.showwarning("Warning", "Password must contain numbers!")
        return None

    # Check if both passwords contain only allowed characters
    if re.search(pattern, password_text1) or re.search(pattern, password_text2):
        messagebox.showwarning("Warning", "Password must only contain letters, numbers, and '@' as a special character.")
        return None

    # Check if both passwords contain at least one uppercase character
    if len(re.findall(r'[A-Z]', password_text1)) < 1 or len(re.findall(r'[A-Z]', password_text2)) < 1:
        messagebox.showwarning("Warning", "Password must contain at least one uppercase character.")
        return None

    # If all checks pass, return the passwords
    return password_text1, password_text2


#Detect is user does not enter the correct email requirements
def is_required_email(email_text):
    if not re.search(r'@', email_text): #Checks if the email contains a @ symbol
     messagebox.showwarning("Warning", "Email must contain an @ symbol") 
    elif len(email_text) < 15: #checking if password text contains more than 8 chracters
       messagebox.showwarning("Warning", "Email must be greater than 15 characters!")
    else:
        return email_text

def is_email_domained(email_text):
    domains = ["gmail.com", "hotmail.com", "org.za", "co.za", "gov.za"]
    # Check if the email contains any of the specified domains
    if not any(domain in email_text for domain in domains):
        messagebox.showwarning("Warning", "Please enter a valid domain.")
        return False  # Indicate that the email is not valid
    return True  # Indicate that the email is valid


#checking to see if password matches
def is_password_match(password_text1, password_text2):
    if not(password_text1 == password_text2):
        messagebox.showwarning("Password Error", "Passwords Does not match!")