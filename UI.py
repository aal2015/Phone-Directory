from tkinter import *
from tkinter import ttk
import pickle
from functools import partial
from linked_list import LinkedList
from data import contact_list

# Beige
BACKGROUND_COLOR = "#F5F5F5"


class PhoneDirectoryInterface():
    def __init__(self, *args, **kwargs):

        infile = open('data.py', 'r')
        new_dict = pickle.load(infile)
        infile.close()

        self.window = Tk()
        # self.window.minsize(width=300, height=500)

        self.window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
        self.linkedList = LinkedList()
        self.addedToPage = []
        self.contact_detail_list = []
        self.contact_list_page()

        self.window.mainloop()

    def addScroll(self):
        # Create A Main frame
        main_frame = Frame(self.window)
        main_frame.pack(fill=BOTH, expand=1)
        self.addedToPage.append(main_frame)

        # Create A Canvas
        my_canvas = Canvas(main_frame, bg=BACKGROUND_COLOR)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.addedToPage.append(my_canvas)

        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        self.addedToPage.append(my_scrollbar)

        # Configure The Canvas
        my_canvas.configure(yscrollcomman=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas
        second_frame = Frame(my_canvas)

        # Add that New frame To a Window In The Canvas
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        return second_frame

    def pack_forget_function(self):
        for item in self.addedToPage:
            item.pack_forget()
        self.addedToPage = []

    # ---------------------------- Contact List Page ------------------------------- #

    def contact_list_page(self):
        self.pack_forget_function()
        self.contact_detail_list = []

        application_title = Label(text="Contacts", font=("Arial", 28, "bold"), bg=BACKGROUND_COLOR)
        application_title.pack(side=TOP)
        self.addedToPage.append(application_title)

        second_frame = self.addScroll()

        if self.linkedList.return_head() is None:
            for contact in contact_list:
                self.linkedList.insert(name=contact["name"], address=contact["address"], contact_number=contact["contact_number"])

        i = 0
        temp = self.linkedList.return_head()
        while temp is not None:
            name_Button = Button(second_frame, text=temp.name, font=("Arial", 12, "bold"), command=partial(self.contact_detail_page, i), relief=FLAT, anchor="e", bg=BACKGROUND_COLOR)
            name_Button.pack(anchor='w')
            self.addedToPage.append(name_Button)

            self.contact_detail_list.append({"name": temp.name, "address": temp.address, "contact_number": temp.contact_number})
            temp = temp.next
            i += 1

        addContact = Button(text="Add Contact", font=("Arial", 10, "bold"), command=self.add_contact_page, relief=FLAT, bg=BACKGROUND_COLOR)
        addContact.pack(padx=10, pady=10)
        self.addedToPage.append(addContact)

    def save_changes(self):
        pass

    # -------------------------- Display Contact Detail----------------------------- #

    def contact_detail_page(self, index):
        self.pack_forget_function()

        title = Label(text="Contact Information", font=("Arial", 28, "bold"), bg=BACKGROUND_COLOR)
        title.pack(side=TOP)
        self.addedToPage.append(title)

        name, address, contact_number = self.contact_detail_list[index]["name"], self.contact_detail_list[index]["address"], self.contact_detail_list[index]["contact_number"]

        name_frame = Frame(self.window)
        name_frame.pack(anchor="w")
        name_label = Label(name_frame, text="Name ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        name_label.pack(anchor='w', side=LEFT)
        name_output = Label(name_frame, text=name, font=("Arial", 12), anchor="e", bg=BACKGROUND_COLOR)
        name_output.pack(anchor='w', side=LEFT)
        self.addedToPage.extend([name_frame, name_label, name_output])

        address_frame = Frame(self.window)
        address_frame.pack(anchor="w")
        address_label = Label(address_frame, text="Address ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        address_label.pack(anchor='w', side=LEFT)
        address_output = Label(address_frame, text=address, font=("Arial", 12), anchor="e", bg=BACKGROUND_COLOR)
        address_output.pack(anchor='w', side=LEFT)
        self.addedToPage.extend([address_frame, address_label, address_output])

        contact_number_frame = Frame(self.window)
        contact_number_frame.pack(anchor="w")
        contact_number_label = Label(contact_number_frame, text="Contact Number ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        contact_number_label.pack(anchor='w', side=LEFT)
        contact_number_output = Label(contact_number_frame, text=contact_number, font=("Arial", 12), anchor="e", bg=BACKGROUND_COLOR)
        contact_number_output.pack(anchor='w', side=LEFT)
        self.addedToPage.extend([contact_number_frame, contact_number_label, contact_number_output])

        edit_button = Button(text="Edit", font=("Arial", 12, "bold"), command=lambda: self.edit_contact_page(name,address,contact_number), relief=FLAT, bg=BACKGROUND_COLOR)
        edit_button.pack()
        delete_button = Button(text="Delete", font=("Arial", 12, "bold"), command=lambda: self.delete_contact(name,address,contact_number), relief=FLAT, bg=BACKGROUND_COLOR)
        delete_button.pack()
        back_button = Button(text="Back", font=("Arial", 12, "bold"), command=self.contact_list_page, relief=FLAT, bg=BACKGROUND_COLOR)
        back_button.pack()
        self.addedToPage.extend([edit_button, delete_button, back_button])


    def delete_contact(self, name, address, contact_number):
        self.linkedList.delete_node(name, address, contact_number)
        self.contact_list_page()

    # ----------------------------- Edit Contact Page ------------------------------ #

    def edit_contact_page(self, name, address, contact_number):
        self.pack_forget_function()
        entry_length = 80
        previous_record = [name, address, contact_number]

        title = Label(text="Edit Contact", font=("Arial", 28, "bold"), bg=BACKGROUND_COLOR)
        title.pack(side=TOP)
        self.addedToPage.append(title)

        name_frame = Frame(self.window)
        name_frame.pack(anchor="w")
        name_label = Label(name_frame, text="Name ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        name_label.pack(anchor='w', side=LEFT)
        name_input = Entry(name_frame, width=(entry_length + 3))
        name_input.insert(END,name)
        name_input.pack(side=LEFT)
        self.addedToPage.extend([name_frame, name_label, name_input])

        address_frame = Frame(self.window)
        address_frame.pack(anchor="w")
        address_label = Label(address_frame, text="Address ", font=("Arial", 12, "bold"), anchor="e",
                              bg=BACKGROUND_COLOR)
        address_label.pack(anchor='w', side=LEFT)
        address_input = Entry(address_frame, width=entry_length)
        address_input.insert(END, address)
        address_input.pack(side=LEFT)
        self.addedToPage.extend([address_frame, address_label, address_input])

        contact_number_frame = Frame(self.window)
        contact_number_frame.pack(anchor="w")
        contact_number_label = Label(contact_number_frame, text="Contact Number ", font=("Arial", 12, "bold"),
                                     anchor="e", bg=BACKGROUND_COLOR)
        contact_number_label.pack(anchor='w', side=LEFT)
        contact_number_input = Entry(contact_number_frame, width=(entry_length - 10))
        contact_number_input.insert(END, contact_number)
        contact_number_input.pack(side=LEFT)
        self.addedToPage.extend([contact_number_frame, contact_number_label, contact_number_input])

        update_button = Button(text="Update", font=("Arial", 12, "bold"), command=lambda: self.update_contact(previous_record[0], previous_record[1], previous_record[2], name_input.get(), address_input.get(), contact_number_input.get()), relief=FLAT, bg=BACKGROUND_COLOR)
        update_button.pack()
        cancel_button = Button(text="Cancel", font=("Arial", 12, "bold"), command=self.contact_list_page, relief=FLAT, bg=BACKGROUND_COLOR)
        cancel_button.pack()
        self.addedToPage.extend([update_button, cancel_button])

    def update_contact(self, prev_name, prev_address, prev_contact_number, name, address, contact_number):
        self.linkedList.update(prev_name, prev_address, prev_contact_number, name, address, contact_number)
        self.contact_list_page()

    # ----------------------------- Add Contact Page ------------------------------- #
    def add_contact_page(self):
        self.pack_forget_function()
        entry_length = 80

        title = Label(text="Add Contact", font=("Arial", 28, "bold"), bg=BACKGROUND_COLOR)
        title.pack(side=TOP)
        self.addedToPage.append(title)

        name_frame = Frame(self.window)
        name_frame.pack(anchor="w")
        name_label = Label(name_frame, text="Name ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        name_label.pack(anchor='w', side=LEFT)
        name_input = Entry(name_frame, width=(entry_length + 3))
        name_input.pack(side=LEFT)
        self.addedToPage.extend([name_frame, name_label, name_input])

        address_frame = Frame(self.window)
        address_frame.pack(anchor="w")
        address_label = Label(address_frame, text="Address ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        address_label.pack(anchor='w', side=LEFT)
        address_input = Entry(address_frame, width=entry_length)
        address_input.pack(side=LEFT)
        self.addedToPage.extend([address_frame, address_label, address_input])

        contact_number_frame = Frame(self.window)
        contact_number_frame.pack(anchor="w")
        contact_number_label = Label(contact_number_frame, text="Contact Number ", font=("Arial", 12, "bold"), anchor="e", bg=BACKGROUND_COLOR)
        contact_number_label.pack(anchor='w', side=LEFT)
        contact_number_input = Entry(contact_number_frame, width=(entry_length - 10))
        contact_number_input.pack(side=LEFT)
        self.addedToPage.extend([contact_number_frame, contact_number_label, contact_number_input])

        add_button = Button(text="Add", font=("Arial", 12, "bold"), command=lambda: self.add_contact(name_input.get(),address_input.get(),contact_number_input.get()), relief=FLAT, bg=BACKGROUND_COLOR)
        add_button.pack()
        back_button = Button(text="Back", font=("Arial", 12, "bold"), command=self.contact_list_page, relief=FLAT, bg=BACKGROUND_COLOR)
        back_button.pack()
        self.addedToPage.extend([add_button,back_button])

    def add_contact(self, name, address, contact_number):
        self.linkedList.insert(name=name, address=address, contact_number=contact_number)
        self.contact_list_page()