# James Carlson 
# Coding Temple - SE FT-144
# Module 3: Mini-project | Contact Management System

'''
# CLI based app
# add, edit, delete, and search for contacts
# dictionaries, file handling, user input, error handling

1. User Interface (UI):
- Create a user-friendly command-line interface (CLI) for the Contact Management System.
- Display a welcoming message and provide a menu with the following options:

Welcome to the Contact Management System!

Menu:
1. Add a new contact
2. Edit an existing contact
3. Delete a contact
4. Search for a contact
5. Display all contacts
6. Export contacts to a text file
7. Quit

2. Contact Data Storage:
- Use nested dictionaries as the main data structure for storing contact information.
- Each contact should have a unique identifier (e.g., a phone number or email address) as the outer dictionary key.
- Store contact details within the inner dictionary, including:
- Name
- Phone number
- Email address
- Additional information (e.g., address, notes).

3.Menu Actions:
- Implement the following actions in response to menu selections:
- Adding a new contact with all relevant details.
- Editing an existing contact's information (name, phone number, email, etc.).
- Deleting a contact by searching for their unique identifier.
- Searching for a contact by their unique identifier and displaying their details.
- Displaying a list of all contacts with their unique identifiers.
- Exporting contacts to a text file in a structured format.

4. User Interaction:
- Utilize input() to enable users to select menu options and provide contact details.
- Implement input validation using regular expressions (regex) to ensure correct formatting of contact information.

5. Error Handling:
- Apply error handling using try, except, else, and finally blocks to manage unexpected issues that may arise during execution.

6. GitHub Repository:
- Create a GitHub repository for your project.
- Commit your code to the repository regularly.
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

contacts_dictionary = {}
# nexted dictionary format
# contacts_dictionary = {
#     "id_0001" : {
#         "name_last" : "", # * no field should be required? but if the entry is entirely empty, delete the entry?
#         "name first" : "",
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
    Display main menu and handle corresponding input.
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
            menu_edit()
        elif menu_sel.startswith("delete") or menu_sel == "3":
            menu_del()
        elif menu_sel.startswith("search") or menu_sel == "4":
            menu_search()
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

def menu_edit():    # <-- but I need a way to determine which contact to edit-- employ the search function?
    pass
def menu_del():     # <-- same^
    pass
def menu_search():  # so are these three ^^ all just calling the search function with different prompts?
    pass

def add_new_contact():
    '''
    Add new contact to contact dictionary using user input for details.
    '''
    # set id to number not yet in dictionary
    contact_id = "id_" + str(len(contacts_dictionary)+1).zfill(4)
    print("Please fill out the following fields. You can also skip a field by leaving it empty.") # should I include a way to cancel??
    name_first = input("Contact's First Name: ")
    name_last = input("Contact's Last Name: ")
    phone = input("Contact's Phone Number: ")
    email = input("Contact's Email Address: ")
    address = input("Contact's Address: ")
    # TO-DO: group = input(f"Add any groups this contact should be sorted by (family/friends): ")
    notes = input("Enter any additional notes: ")

    # TO-DO: check for entirely empty contact? warn user no contact has been/will be added

    contacts_dictionary.update({contact_id : {
        "name_first" : name_first,
        "name_last" : name_last,
        "phone" : phone,
        "email" : email,
        "address" : address,
        # TO-DO: groups!
        "notes" : notes
    }})
    
    
    
  
def edit_contact():         # <-- DELETE??
    pass
def delete_contact():       # <-- deleting is easy; question is, should that id number be put back into circulation?
    pass
def search_for_contact():   # <-- okay so this one will need to do some heavy lifting; return id?
    pass
def display_contact(contact):
    '''
    Display single contact with passed-in id number.
    '''
    print(f"Name: {contacts_dictionary[contact]["name_first"]} {contacts_dictionary[contact]["name_last"]}")
    print(f"Phone: {contacts_dictionary[contact]["phone"]}")
    print(f"Email: {contacts_dictionary[contact]["email"]}")
    print(f"Address: {contacts_dictionary[contact]["address"]}")
    # TO-DO: groups!
    print(f"Notes: {contacts_dictionary[contact]["notes"]}")

def display_all_contacts():
    '''
    Display all contacts, looping through entire contact dictionary.
    '''
    for contact in contacts_dictionary:
        display_contact(contact)

def export_contacts():      # <-- good thing I didn't just learn to do this today haha
    pass
def import_contacts():      # <-- you're a mad man, Jim
    pass



print("\nWelcome to the Contact Management System!")
menu_main()