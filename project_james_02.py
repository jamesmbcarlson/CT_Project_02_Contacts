# James Carlson 
# Coding Temple - SE FT-144
# Module 3: Mini-Project | Contact Management System

import re
import os

# format constants
F_UNDERLINE = "\033[4m"
F_RED = "\033[91m"
F_YELLOW = "\033[93m"
F_GREEN = "\033[92m"
F_RESET = "\033[0m"

# dictionary key constants
K_NAME_FIRST = "name_first"
K_NAME_LAST = "name_last"
K_NAME_FULL = "name_full"
K_PHONE = "phone"
K_EMAIL = "email"
K_ADDRESS = "address"
K_NOTES = "notes"
K_GROUPS = "groups"

# default file for exporting, importing
DEFAULT_FILENAME = "contact_directories/my_contacts.txt"

total_contacts = 0
contacts_dictionary = {}
existing_groups = []

# nexted dictionary format:
#
# contacts_dictionary = {
#     "id_0001" : {
#         "name_last" : "", 
#         "name_first" : "",
#         "name_full" : "",     # added full name for searching purposes
#         "phone" : "",         # phone must be 10 digit value
#         "email" : "",         # email must contain a valid email format
#         "address" : "",       # address field does not have any specific requirements, as this field could hold a wide variety of information
#         "notes" : "",
#         "group" : []          # group holds a list of categorizing groups
#         },  
#     "id_0002" : {
#         # ... etc ...
#     },
# }

def menu_main():
    '''
    Display main menu and handle corresponding input, looping as long as the program is running.
    '''
    while True:
        # display main menu
        print(f"\n{F_UNDERLINE}Main Menu{F_RESET}")
        print(f"{F_YELLOW}1{F_RESET}. Add a new contact")
        print(f"{F_YELLOW}2{F_RESET}. Edit an existing contact")
        print(f"{F_YELLOW}3{F_RESET}. Delete a contact")
        print(f"{F_YELLOW}4{F_RESET}. Search for a contact")
        print(f"{F_YELLOW}5{F_RESET}. Display all contacts")
        print(f"{F_YELLOW}6{F_RESET}. Export contacts to a text file")
        print(f"{F_YELLOW}7{F_RESET}. Import contacts from a text file")
        print(f"{F_YELLOW}8{F_RESET}. Quit")

        # take and handle user selection
        menu_sel = input("\nPlease make a selection: ").casefold()
        print()

        if menu_sel.startswith("add") or menu_sel == "1":
            add_new_contact()
        elif menu_sel.startswith("edit") or menu_sel == "2":
            menu_search("edit")
        elif menu_sel.startswith("delete") or menu_sel == "3":
            menu_search("delete")
        elif menu_sel.startswith("search") or menu_sel == "4":
            menu_search("view")
        elif menu_sel.startswith("display") or menu_sel == "5":
            display_all_contacts()
        elif menu_sel.startswith("export") or menu_sel == "6":
            export_contacts()
        elif menu_sel.startswith("import") or menu_sel == "7":
            import_contacts()
        elif menu_sel.startswith("quit") or menu_sel == "8":
            print("Thank you for using the Contact Managment System!")
            break
        else:
            print("Invalid input. Please make a selection from the menu.")

def add_new_contact():
    '''
    Add new contact to contact dictionary using user input for details.
    '''
    # set id to number not yet in dictionary
    global total_contacts 
    total_contacts += 1
    contact_id = "id_" + str(total_contacts).zfill(4)

    print("Please fill out the following fields:") 

    # required fields
    name_first = validate_name("Contact's First Name: ")
    name_last = validate_name("Contact's Last Name: ")
    phone = validate_phone()
    email = validate_email()

    # optional fields
    address = input("Contact's Address: ") 
    notes = input("Enter any additional notes: ")
    groups = add_groups([])    
    
    contacts_dictionary.update({contact_id : {
        K_NAME_FIRST : name_first,
        K_NAME_LAST : name_last,
        K_NAME_FULL : f"{name_first} {name_last}",
        K_PHONE : phone,
        K_EMAIL : email,
        K_ADDRESS : address,
        K_NOTES : notes,
        K_GROUPS : groups
    }})

def validate_name(prompt):
    '''
    Check if name field is filled in. Otherwise prompt again for input.
    '''
    while True:
        name = input(prompt)
        # name fields can hold a combination of any characters [a-zA-Z0-9_] but they cannot be empty
        if re.match(r"^\w+", name):
            return name
        else:
            print("Invalid input. Please enter a name.")

def validate_phone():
    '''
    Check if phone number is ten digit number. Can include dashes, parentheses, and spaces.
    '''
    while True:
        phone = input("Contact's Phone Number: ")
        # phone number field must have a 10 digit value
        if re.match(r"\(?\d{3}-?\)?\s?\d{3}\s?-?\d{4}", phone):
            return phone
        else:
            print("Invalid input. Please enter a ten digit phone number.")

def validate_email():
    '''
    Check if email address is valid. Must include address, @ symbol, domain name, dot, and domain extension.
    '''
    while True:
        email = input("Contact's Email Address: ")
        # email address field must hold a valid email format
        if re.match(r"[A-Za-z0-9._+-]+@+[A-Za-z0-9.-]+\.+[A-z]{2,}", email):
            return email
        else:
            print("Invalid input. Please enter a valid email address.")

def add_groups(groups):
    '''
    Add categorizing groups that contacts can be sorted into.
    '''
    print("\nYou can group this contact to categorize them. For example: friends, family, work, etc.")

    # display any existing groups that have been used previously
    if len(existing_groups) > 0:
        print(f"Existing groups: {existing_groups}")

    print("This is an optional field. You can add multiple groups. Enter \"cancel\" to escape.")
    while True:
        group = input(f"Add a group this contact should be sorted by: ")

        # exit loop
        if group == "cancel":
            return groups
        
        # add categorizing group
        else:
            groups.append(group)
            if group not in existing_groups:
                existing_groups.append(group)

def menu_search(action):
    '''
    Handle searching for contact to edit, delete, or view.
    '''
    # exit function if dictionary is empty
    if is_dictionary_empty():
        return
    
    while True:
        # get search term for contact from user
        menu_input = input(f"Which contact would you like to {action}? ")

        # handle search cancel - return to main menu
        if menu_input == "cancel":
            break

        # ensure we are not searching for empty fields
        elif menu_input == "" or re.match(r"^\s+$", menu_input):
            print("Error. Cannot search for empty term")

        # search for contact to modify or view
        else:
            contact = search_for_contact(menu_input)
            if contact != None:
                if action == "edit":
                    edit_contact(contact)
                elif action == "delete":
                    delete_contact(contact)
                else:
                    display_contact(contact, False)
                # return to main menu after function call
                break

            # handle contact not found
            else:
                print("Enter a different search term or enter \"cancel\" to return to the main menu.")

def edit_contact(contact):
    '''
    Edit field for provided contact based on user selection.
    '''
    while True:
        name_full = contacts_dictionary[contact][K_NAME_FULL]
        display_contact(contact, True)
        field_input = input("Which field would you like to edit? ").casefold()

        # handle search cancel - return to main menu
        if field_input == "cancel":
            break

        # edit name field(s)
        elif field_input == "1" or "name" in field_input:
            name_first = validate_name("Contact's First Name: ")
            name_last = validate_name("Contact's Last Name: ")
            new_value = f"{name_first} {name_last}"

            # confirm edit for name fields
            confirm = edit_value(f"Are you sure you want to update {name_full} to {new_value} for your contact? (yes/no) ", 
                       contact, name_first=name_first, name_last=name_last, name_full=new_value)
            if confirm == True:
                print(f"Your contact information for {new_value} has been updated!")
            else:
                print(f"Your contact informmation for {name_full} has not been updated.")

            # return to main menu
            break
        
        # edit phone field
        elif field_input == "2" or field_input.startswith("phone"):
            new_value = validate_phone()

            # confirm edit for phone
            confirm = edit_value(f"Are you sure you want to update the phone number to {new_value} for {name_full}? (yes/no) ", 
                       contact, phone=new_value)
            edit_confirmation(confirm, name_full)

            # return to main menu
            break

        # edit email field
        elif field_input == "3" or "email" in field_input:
            new_value = validate_email()

            # confirm edit for email
            confirm = edit_value(f"Are you sure you want to update the email address to {new_value} for {name_full}? (yes/no) ", 
                       contact, email=new_value)
            edit_confirmation(confirm, name_full)

            # return to main menu
            break

        # edit address
        elif field_input == "4" or field_input.startswith("address"):
            new_value = input("Contact's Address: ")

            # confirm edit for address
            confirm = edit_value(f"Are you sure you want to update the phone number to {new_value} for {name_full}? (yes/no) ", 
                       contact, address=new_value)
            edit_confirmation(confirm, name_full)

            # return to main menu
            break

        # edit notes
        elif field_input == "5" or "notes" in field_input:
            while True:
                choice = input("Would you like to overwrite your current notes or add a new note? (overwrite/add) ").casefold()

                # overwrite note
                if choice == "overwrite":
                    new_note = input("Enter your new note: ")
                    confirm = edit_value(f"Are you sure you want to overwrite your old note? (yes/no) ", 
                       contact, notes=new_note)
                    edit_confirmation(confirm, name_full)
                    break

                # add note
                elif choice == "add":
                    new_note = contacts_dictionary[contact][K_NOTES] + " " + input("What note would you like to add? ")
                    contacts_dictionary[contact][K_NOTES] = new_note
                    edit_confirmation(True, name_full)
                    break

                # handle invalid input
                else:
                    print("Invalid input. Please enter either \"overwrite\" or \"add\"")
            break

        # edit groups
        elif field_input == "6" or "group" in field_input:
            
            # add group(s) to empty field
            if contacts_dictionary[contact][K_GROUPS] == []:
                contacts_dictionary[contact][K_GROUPS] = add_groups([])
                edit_confirmation(True, name_full)

            # if groups already populated, give option to add or remove groups
            else:
                while True:
                    choice = input("Would you like to add or remove a group? (add/remove) ")

                    # add group(s)
                    if choice == "add":
                        contacts_dictionary[contact][K_GROUPS] = add_groups(contacts_dictionary[contact][K_GROUPS])
                        edit_confirmation(True, name_full)
                        break

                    # remove group
                    elif choice == "remove":
                        while True:
                            print(f"{name_full}\nGroups: {contacts_dictionary[contact][K_GROUPS]}")
                            remove_choice = input("Which group would you like to remove? ")

                            if remove_choice.casefold() == "cancel":
                                break

                            # remove group if found
                            elif remove_choice in contacts_dictionary[contact][K_GROUPS]:
                                contacts_dictionary[contact][K_GROUPS].remove(remove_choice)
                                edit_confirmation(True, name_full)
                                break

                            # handle invalid input
                            else:
                                print("Invalid input. Groups are case sensitive. Enter \"cancel\" to escape.")

                        break

                    # handle invalid input
                    else:
                        print("Invalid input. Please enter \"add\" or \"remove\"")

            break

        # handle contact not found
        else:
            print("Invalid input. Enter a field to edit or enter \"cancel\" to return to the main menu.")

def edit_value(prompt, contact, **values):
    '''
    Confirm change to provided values.
    '''
    while True:
        confirm = input(prompt)
        if confirm == "yes" or confirm == "y":
            # assign passed in values to contact dictionary using kwargs
            for key, value in values.items():
                contacts_dictionary[contact][key] = value
            return True
        elif confirm == "no" or confirm == "n":
            return False
        else: 
            print("Invalid input. Please enter \"yes\" or \"no\"")

def edit_confirmation(confirm, name):
    '''
    Display confirmation message after editing value.
    '''
    if confirm == True:
        print(f"Your contact information for {name} has been updated!")
    else:
        print(f"Your contact informmation for {name} has not been updated.")

def delete_contact(contact):
    '''
    Removed passsed in contact from contacts dictionary.

    Deleted IDs are not replaced; they are gone forever ☠️
    '''
    # confirm deletion of contact
    name_to_delete = contacts_dictionary[contact][K_NAME_FULL]
    while True:
        confirm = input(f"{F_RED}Are you sure you want to delete \"{name_to_delete}\" from your contacts?{F_RESET} (yes/no) ")

        # delete contact
        if confirm == "yes" or confirm == "y":
            del contacts_dictionary[contact]
            print(f"\"{name_to_delete}\" has been removed from your contacts.")
            break

        # cancel deletion
        elif confirm == "no" or confirm == "n":
            print("No changes have been made to your contacts.")
            break

        # handle invalid input
        else:
            print("Invalid input. Choose either \"yes\" or \"no\"")

def search_for_contact(search_term):
    '''
    Loop through all fields in all contacts looking for given search term. Returns contact id if found. Otherwise returns None.
    '''
    # compare search term with all values in dictionary
    for contact in contacts_dictionary:
        for field in contacts_dictionary[contact]:
            if search_term.casefold() in str(contacts_dictionary[contact][field]).casefold():
                print(f"{F_YELLOW}Found the following contact:{F_RESET}")
                display_contact(contact, False)
                confirm_input = input("Is this the contact you are looking for? (yes/no): ").casefold()
                if confirm_input == "yes" or confirm_input == "y":
                    return contact
                # otherwise, keep searching!
                else:
                    break
    # if no one found:
    print(f"Contact not found with search term \"{search_term}\"")
    return None

def display_contact(contact, is_numbered):
    '''
    Display single contact with passed-in id number. If is_numbered is True, numbers all fields sequentially.
    '''
    if is_numbered == True:
        print(f"{F_YELLOW}1{F_RESET} - ", end="")
    print(f"{F_GREEN}Name: {contacts_dictionary[contact][K_NAME_FULL]}{F_RESET}")
    if is_numbered == True:
        print(f"{F_YELLOW}2{F_RESET} - ", end="")
    print(f"Phone: {contacts_dictionary[contact][K_PHONE]}")
    if is_numbered == True:
        print(f"{F_YELLOW}3{F_RESET} - ", end="")
    print(f"Email: {contacts_dictionary[contact][K_EMAIL]}")
    if is_numbered == True:
        print(f"{F_YELLOW}4{F_RESET} - ", end="")
    print(f"Address: {contacts_dictionary[contact][K_ADDRESS]}")
    if is_numbered == True:
        print(f"{F_YELLOW}5{F_RESET} - ", end="")
    print(f"Notes: {contacts_dictionary[contact][K_NOTES]}")
    if is_numbered == True:
        print(f"{F_YELLOW}6{F_RESET} - ", end="")
    print(f"Groups: {contacts_dictionary[contact][K_GROUPS]}")
    print()

def display_all_contacts():
    '''
    Display all contacts, looping through entire contact dictionary.
    '''
    # exit function if dictionary is empty
    if is_dictionary_empty():
        return
    
    for contact in contacts_dictionary:
        display_contact(contact, False)

def export_contacts():
    '''
    Export contacts to text file.
    '''
    # exit function if dictionary is empty
    if is_dictionary_empty():
        return
    
    # warn for overwrite
    if os.path.isfile(DEFAULT_FILENAME):
        while True:
            print(f"{F_RED}Warning!{F_RESET} A file already exists at \"{DEFAULT_FILENAME}\"\
                \n{F_RED}Exporting your contacts will overwrite this file.{F_RESET}")
            confirm = input("Would you like to overwrite your current contacts file? (yes/no) ")
            if confirm == "yes" or confirm == "y":
                break
            elif confirm == "no" or confirm == "n":
                print("Your contacts will not be exported.")
                return
            else:
                print("Invalid input. Please enter \"yes\" or \"no\"")

    try:
        # makes a new directory
        os.makedirs("contact_directories", exist_ok=True)

        # writing to our text file
        with open(DEFAULT_FILENAME, "w") as file:
            for contact in contacts_dictionary:
                file.write(f"{contact} : {contacts_dictionary[contact]}\n")
    except PermissionError:
        print(f"You don't have permission to write to file \"{DEFAULT_FILENAME}\"")
        print("Your contacts have not been exported.")
    except IOError:
        print("An IOError has occured while writing to this file.")
        print("Your contacts have not been exported.")
    except Exception as e:
        print(f"Error: {e}")
        print("Your contacts have not been exported.")
    else:
        print(f"Your contacts have been exported to file: \"{DEFAULT_FILENAME}\"")

def import_contacts():
    '''
    Import contacts from text file.
    '''

    # warn for overwrite
    if contacts_dictionary != {}:
        while True:
            print(f"{F_RED}Warning! Importing contact file will overwrite your current contacts.{F_RESET}")
            confirm = input("Would you like to overwrite your current list of contacts? (yes/no) ")
            if confirm == "yes" or confirm == "y":
                break
            elif confirm == "no" or confirm == "n":
                print("Your contacts will not be imported.")
                return
            else:
                print("Invalid input. Please enter \"yes\" or \"no\"")

    # reset contacts_dictionary
    contacts_dictionary.clear()
    global total_contacts
    total_contacts = 0
    existing_groups.clear()

    # read from file and fill in dictionary
    try:
        with open(DEFAULT_FILENAME, "r") as file:
            contacts = file.readlines()
            for contact in contacts:
                imp_id = re.match(r"id_\d+", contact).group(0)
                contacts_dictionary[imp_id] = {}

                # update number used to determine new ids so that new contacts do not overwrite previous contacts
                id_num = int(re.match(r"id_(\d+)", imp_id).group(1))
                if id_num > total_contacts:
                    total_contacts = id_num

                # extract groups - the list creates a format that must be handled differently
                temp_group = re.search(r", 'groups': \[.*\]", contact)
                if temp_group:            
                    parsed_content = contact.replace(temp_group.group(), "")
                else:
                    parsed_content = contact.replace(", 'groups': []", "")
                
                # parse text and assign dictionary key, value pairs
                contact_contents = re.search(r"{(.*)}", parsed_content).group(1).split(", ")
                for item in contact_contents:
                    pair = item.split(": ")
                    contacts_dictionary[imp_id][re.search(r"\'(.*)\'", pair[0]).group(1)] = re.search(r"\'(.*)\'", pair[1]).group(1)
                    # TO-DO: using quotes within notes or any other field messes this up... so I gotta figure out how to handle that

                # reinsert groups
                contacts_dictionary[imp_id][K_GROUPS] = []
                if temp_group:
                    parsed_list = re.search(r"\[(.*)\]", temp_group.group()).group(1).split(", ")

                    # ignore empty lists with only empty strings
                    if len(parsed_list) > 0:
                        for item in parsed_list:
                            if item != '':
                                group = re.search(r"\'(.*)\'", item).group(1)
                                contacts_dictionary[imp_id][K_GROUPS].append(group)

                                # update list of existing groups
                                if group not in existing_groups:
                                    existing_groups.append(group)
                
    except FileNotFoundError:
        print("This file could not be found. Import failed.")
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("Your contacts have been imported!")

def is_dictionary_empty():
    '''
    Determine if dictionary is empty. Return True if the dictionary is empty. Else return False.
    '''
    if contacts_dictionary == {}:
        print("Your address book is empty. Add some contacts.")
        return True
    else:
        return False

print("\nWelcome to the Contact Management System!")
menu_main()