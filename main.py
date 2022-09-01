from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for char in range(randint(8, 10))]
    password_list += [choice(symbols) for char in range(randint(2, 4))]
    password_list += [choice(numbers) for char in range(randint(2, 4))]
    password_list += [choice(numbers) for char in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = web_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="NO Data File Found")
    else:
        for index in data:
            if website in data:
                messagebox.showinfo(title=website,
                                    message=f"Email:  {data[index]['email']}\n\n Password:  {data[index]['password']}")
            else:
                messagebox.showwarning(title="Error", message=f"No details for the {website} exists")
    finally:
        web_entry.delete(0, END)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_entry.get()
    email = email_entry.get()
    password = pass_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Opps", message="Please don't leave any of the fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            web_entry.delete(0, END)
            pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=130, height=180)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(65, 90, image=logo_img)
canvas.grid(column=1, row=0)

web_label = Label(text="Website:")
web_label.grid(column=0, row=1)
web_label.config(padx=0, pady=2)

web_entry = Entry(width=25)
web_entry.grid(column=1, row=1)
web_entry.focus()

search_button = Button(text="Search", width=16, command=search_password)
search_button.grid(column=2, row=1)

email_label = Label(text="Email/Username: ")
email_label.grid(column=0, row=2)
email_label.config(padx=0, pady=2)

email_entry = Entry(width=45)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, 'kipkoechsomoe@gmail.com')

pass_label = Label(text="Password: ")
pass_label.grid(column=0, row=3)
pass_label.config(padx=0, pady=2)

pass_entry = Entry(width=25)
pass_entry.grid(row=3, column=1)

pass_button = Button(text="Generate Password", width=16, command=generate_password)
pass_button.grid(column=2, row=3)

add_button = Button(text="Add", width=38, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
