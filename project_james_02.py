# James Carlson 
# Coding Temple - SE FT-144
# Module 3: Mini-Project | Contact Management System

import re
import os

'''
TO-DO:

3.Menu Actions:
- Exporting contacts to a text file in a structured format.

5. Error Handling:
- Apply error handling using try, except, else, and finally blocks to manage unexpected issues that may arise during execution.

6. GitHub Repository:
- Create a clean and interactive README.md file in your GitHub repository.
- Include clear instructions on how to run the application and explanations of its features.
- Provide examples and screenshots, if possible, to enhance user understanding.
- Include a link to your GitHub repository in your project documentation.

7. Optional Bonus Points
- Contact Categories (Bonus): Implement the ability to categorize contacts into groups (e.g., friends, family, work). Each contact can belong to one or more categories.
- Contact Search (Bonus): Enhance the contact search functionality to allow users to search for contacts by name, phone number, email address, or additional information.
- Contact Sorting (Bonus): Implement sorting options to display contacts alphabetically by name or based on other criteria.
- Backup and Restore (Bonus): Add features to create automatic backups of contact data and the ability to restore data from a backup file.
- Custom Contact Fields (Bonus): Allow users to define custom fields for contacts (e.g., birthdays, anniversaries) and store this information.
'''

# format constants
F_UNDERLINE = "\033[4m"
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

DEFAULT_FILENAME = "contact_directories/my_contacts.txt"

total_contacts = 0
contacts_dictionary = {}
existing_groups = []

# nexted dictionary format
# contacts_dictionary = {
#     "id_0001" : {
#         "name_last" : "", # * no field should be required? but if the entry is entirely empty, delete the entry?
#         "name_first" : "",
#         "name_full" : "",
#         "phone" : "",
#         "email" : "",
#         "address" : "", # address? does that include city, state, zip code? We could go on for a while here...
#         "group" : [], # keep running list of existing groups to both display to users and to compare against
#         "notes" : ""
#         },  # <-- if we allow users to add custom categories, how can we include that in new contacts, existing contacts, imported contacts...?? Food for thought
#     "id_0002" : {
#         # and so forth
#     },
# }

def menu_main():
    '''
    Display main menu and handle corresponding input, looping as long as the program is running.
    '''
    while True:
        # display main menu
        print(f"\n{F_UNDERLINE}Main Menu{F_RESET}")
        print("1. Add a new contact")   # <-- auto backup??v
        print("2. Edit an existing contact") # <-- custom contact fields here?
        print("3. Delete a contact")
        print("4. Search for a contact") # <-- enhance search: search by name, phone number, email... anything else?
        print("5. Display all contacts") # <-- include sorting option here somewhere?
        print("6. Export contacts to a text file")
        print("7. Import contacts from a text file") # make mention of auto backup here?
        print("8. Quit")

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

def menu_search(action):
    '''
    Handle searching for contact to modify or view.
    '''
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

def edit_value(prompt, contact, **values):
    '''
    Confirm change to provided values.
    '''
    while True:
        confirm = input(prompt)
        if confirm == "yes" or confirm == "y":
            for key, value in values:
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
                       contact, K_NAME_FIRST=name_first, K_NAME_LAST=name_last, K_NAME_FULL=new_value)
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
                       contact, K_PHONE=new_value)
            edit_confirmation(confirm, name_full)

            # return to main menu
            break

        # edit email field
        elif field_input == "3" or "email" in field_input:
            new_value = validate_email()

            # confirm edit for email
            confirm = edit_value(f"Are you sure you want to update the email address to {new_value} for {name_full}? (yes/no) ", 
                       contact, K_EMAIL=new_value)
            edit_confirmation(confirm, name_full)

            # return to main menu
            break

        # edit address
        elif field_input == "4" or field_input.startswith("address"):
            new_value = input("Contact's Address: ")

            # confirm edit for address
            confirm = edit_value(f"Are you sure you want to update the phone number to {new_value} for {name_full}? (yes/no) ", 
                       contact, K_ADDRESS=new_value)
            edit_confirmation(confirm, name_full)

            # return to main menu
            break

        # edit notes
        elif field_input == "5" or "notes" in field_input:
            while True:
                choice = input("Would you like to overwrite your current nodes or add a new note? (overwrite/add) ").casefold()

                # overwrite note
                if choice == "overwrite":
                    new_note = input("Enter your new note: ")
                    confirm = edit_value(f"Are you sure you want to overwrite your old note? (yes/no) ", 
                       contact, K_NOTES=new_note)
                    edit_confirmation(confirm, name_full)
                    break

                # add note
                elif choice == "add":
                    new_note = contacts_dictionary[contact][K_NOTES] + "\n" + input("What note would you like to add? ")
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


        # TO-DO: any custom fields?
        # TO-DO: add field??    # 9 - Add New Field

        # handle contact not found
        else:
            print("Invalid input. Enter a field to edit or enter \"cancel\" to return to the main menu.")

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
        K_NAME_FULL : f"{name_first} {name_last}",  # added full name for searching purposes
        K_PHONE : phone,
        K_EMAIL : email,
        K_ADDRESS : address,
        K_GROUPS : groups,
        K_NOTES : notes
    }})

def validate_name(prompt):
    '''
    Check if name field is filled in. Otherwise prompt again for input.
    '''
    while True:
        name = input(prompt)
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
        if re.match(r"[A-Za-z0-9._+-]+@+[A-Za-z0-9.-]+\.+[A-z]{2,}", email):
            return email
        else:
            print("Invalid input. Please enter a valid email address.")

def add_groups(groups):
        print("\nYou can group this contact to categorize them. For example: friends, family, work, etc.")
        if len(existing_groups) > 0:
            print(f"Existing groups: {existing_groups}")
        print("This is an optional field. You can add multiple groups. Enter \"cancel\" to escape.")
        while True:
            group = input(f"Add a group this contact should be sorted by: ")
            if group == "cancel":
                return groups
            else:
                groups.append(group)
                if group not in existing_groups:
                    existing_groups.append(group)

def delete_contact(contact):
    '''
    Removed passsed in contact from contacts dictionary.

    Deleted IDs are not replaced; they are gone forever ☠️
    '''
    name_to_delete = contacts_dictionary[contact][K_NAME_FULL]
    while True:
        confirm = input(f"Are you sure you want to delete \"{name_to_delete}\" from your contacts? (yes/no) ")
        if confirm == "yes" or confirm == "y":
            del contacts_dictionary[contact]
            print(f"\"{name_to_delete}\" has been removed from your contacts.")
            break
        elif confirm == "no" or confirm == "n":
            print("No changes have been made to your contacts.")
            break
        else:
            print("Invalid input.")

def search_for_contact(search_term):
    '''
    Loop through all fields in all contacts looking for given search term. Returns contact id if found. Otherwise returns None.
    '''
    for contact in contacts_dictionary:
        for field in contacts_dictionary[contact]:
            if search_term.casefold() in str(contacts_dictionary[contact][field]).casefold():
                print("Found the following contact:")
                display_contact(contact, False)
                confirm_input = input("Is this the contact you are looking for? (yes/no): ").casefold()
                if confirm_input == "yes" or confirm_input == "y":
                    return contact
                # otherwise, keep searching!
    # if no one found:
    print(f"Contact not found with search term \"{search_term}\"")
    return None

def display_contact(contact, is_numbered):
    '''
    Display single contact with passed-in id number.
    '''
    if is_numbered == True:
        print("1 - ", end="")
    print(f"Name: {contacts_dictionary[contact][K_NAME_FULL]}")
    if is_numbered == True:
        print("2 - ", end="")
    print(f"Phone: {contacts_dictionary[contact][K_PHONE]}")
    if is_numbered == True:
        print("3 - ", end="")
    print(f"Email: {contacts_dictionary[contact][K_EMAIL]}")
    if is_numbered == True:
        print("4 - ", end="")
    print(f"Address: {contacts_dictionary[contact][K_ADDRESS]}")
    if is_numbered == True:
        print("5 - ", end="")
    print(f"Notes: {contacts_dictionary[contact][K_NOTES]}")
    if is_numbered == True:
        print("6 - ", end="")
    print(f"Groups: {contacts_dictionary[contact][K_GROUPS]}")
    # TO-DO: print custom fields
    print()

def display_all_contacts():
    '''
    Display all contacts, looping through entire contact dictionary.
    '''
    for contact in contacts_dictionary:
        display_contact(contact, False)

    # for debugging! TO-DO: Delete me!
    print(contacts_dictionary)

def export_contacts():
    '''
    Export contacts to text file.
    '''
    
    # TO-DO: allow naming of files? - if we do this, we also need to take input in import to select file :/
    DEFAULT_FILENAME = "contact_directories/my_contacts.txt"

    # warn for overwrite
    if os.path.isfile(DEFAULT_FILENAME):
        while True:
            print(f"Warning! A file already exists at \"{DEFAULT_FILENAME}\"\nExporting your contacts will overwrite this file.")
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
    except Exception as e:
        print(f"Error: {e}")
    else:
        print(f"Your contacts have been exported to file: \"{DEFAULT_FILENAME}\"")

def import_contacts():
    '''
    Import contacts from text file.
    '''

    # warn for overwrite
    if contacts_dictionary != {}:
        while True:
            print(f"Warning! Importing contact file will overwrite your current contacts.")
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

    # try:
    with open(DEFAULT_FILENAME, "r") as file:
        contacts = file.readlines()
        for contact in contacts:
            print(contact.strip())
            imp_id = re.match(r"id_\d+", contact).group(0)
            contacts_dictionary[imp_id] = {}

            # extract groups - the list creates a format that must be handled differently
            temp_group = re.search(r"'groups': \[.*\], ", contact)
            print("temp_group", temp_group.group())
            parsed_content = contact.replace(temp_group.group(), "")
            print("parsed_content", parsed_content)

            # parse text and assign dictionary key, value pairs
            contact_contents = re.search(r"{(.*)}", parsed_content).group(1).split(", ")
            print(contact_contents)
            for item in contact_contents:
                pair = item.split(": ")
                contacts_dictionary[imp_id][re.search(r"\'(.*)\'", pair[0]).group(1)] = re.search(r"\'(.*)\'", pair[1]).group(1)
                # TO-DO: using quotes within notes or any other field messes this up... so I gotta figure out how to handle that

            # reinsert groups
            contacts_dictionary[imp_id][K_GROUPS] = []
            parsed_list = re.search(r"\[(.*)\]", temp_group.group()).group(1).split(", ")
            for item in parsed_list:
                contacts_dictionary[imp_id][K_GROUPS].append(re.search(r"\'(.*)\'", item).group(1))
            



            # TO-DO: DELETE THIS DEBUG LINE
            print(contacts_dictionary[imp_id])
    # except Exception as e:
    #     print(f"Error: {e}")
    # else:
    #     print("Your contacts have been imported!")
    
    # reset count - wait hold on this could still potentially create overwrites # TO-DO: reconsider how this whole thing works
    global total_contacts
    total_contacts = len(contacts_dictionary)
    # I think I just need to take in the highest id number and set total contacts to that T0-DO! I'm tired and I'm going to bed now


print("\nWelcome to the Contact Management System!")
menu_main()