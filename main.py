"""Command-line interface for the Contact Manager.

This is the only module that talks to the user (input/print). Each menu
action collects input, asks ContactManager to make the change, and then
saves the whole list to disk straight away.
"""

from contact import (
    Contact,
    validate_email,
    validate_name,
    validate_phone,
)
from contact_manager import ContactManager
from storage import load_contacts, save_contacts


# --- Input helpers ----------------------------------------------------------

def prompt_valid(label, validator, default=None):
    """Ask until `validator` accepts the input.

    If `default` is given, a blank answer keeps it (used when updating).
    """
    while True:
        shown = f"{label} [{default}]: " if default is not None else f"{label}: "
        value = input(shown).strip()
        if not value and default is not None:
            return default
        try:
            return validator(value)
        except ValueError as error:
            print(f"  Invalid: {error}")


def prompt_yes_no(label, default=False):
    """Ask a y/n question; blank or anything else keeps `default`."""
    hint = "y" if default else "n"
    answer = input(f"{label} (y/n) [{hint}]: ").strip().lower()
    # Anything other than an explicit y or n keeps the default.
    return default if answer not in ("y", "n") else answer == "y"


def prompt_index(manager):
    """Show all contacts and ask for one. Returns a Contact, or None."""
    if not manager.contacts:
        print("No contacts available.")
        return None
    show_contacts(manager.contacts)
    raw = input("Enter contact number (blank to cancel): ").strip()
    if not raw:
        return None
    try:
        index = int(raw) - 1
    except ValueError:
        print("Please enter a valid number.")
        return None
    if 0 <= index < len(manager.contacts):
        return manager.contacts[index]
    print("Invalid contact number.")
    return None


def show_contacts(contacts):
    """Print a numbered list of contacts."""
    if not contacts:
        print("No contacts found.")
        return
    for i, contact in enumerate(contacts, start=1):
        print(f"{i}. {contact}")


# --- Menu actions -----------------------------------------------------------

def add_contact(manager):
    """Prompt for every field, then add and save the new contact."""
    name = prompt_valid("Enter contact name", validate_name)
    phone = prompt_valid("Enter phone number", validate_phone)
    email = prompt_valid("Enter email", validate_email)
    address = input("Enter address: ").strip()
    birthday = input("Enter birthday: ").strip()
    notes = input("Enter notes: ").strip()
    favorite = prompt_yes_no("Is favorite?")
    manager.add_contact(Contact(name, phone, email, address, birthday, notes, favorite))
    save_contacts(manager.contacts)
    print("Contact added successfully.")


def update_contact(manager):
    """Pick a contact and edit it; blank answers keep the current values."""
    contact = prompt_index(manager)
    if contact is None:
        return
    print("Enter new details (leave blank to keep the current value):")
    # Name, phone and email are re-prompted until valid, so update_contact
    # below only receives values that will pass Contact validation.
    manager.update_contact(
        contact,
        name=prompt_valid("Name", validate_name, contact.name),
        phone_number=prompt_valid("Phone Number", validate_phone, contact.phone_number),
        email=prompt_valid("Email", validate_email, contact.email),
        address=input(f"Address [{contact.address}]: ").strip() or contact.address,
        birthday=input(f"Birthday [{contact.birthday}]: ").strip() or contact.birthday,
        notes=input(f"Notes [{contact.notes}]: ").strip() or contact.notes,
        favorite=prompt_yes_no("Is favorite?", contact.favorite),
    )
    save_contacts(manager.contacts)
    print("Contact updated successfully.")


def view_contacts(manager):
    """Print every saved contact."""
    if not manager.contacts:
        print("No contacts available.")
        return
    print("Contacts:")
    show_contacts(manager.contacts)


def search_contacts(manager):
    """Print contacts whose name contains the search text."""
    query = input("Enter name to search: ")
    show_contacts(manager.search(query))


def toggle_favorite(manager):
    """Pick a contact and flip its favorite flag."""
    contact = prompt_index(manager)
    if contact is None:
        return
    manager.toggle_favorite(contact)
    save_contacts(manager.contacts)
    print("Favorite status updated.")


def delete_contact(manager):
    """Pick a contact and remove it."""
    contact = prompt_index(manager)
    if contact is None:
        return
    manager.delete_contact(contact)
    save_contacts(manager.contacts)
    print("Contact deleted.")


# --- Main loop --------------------------------------------------------------

MENU = """
===== Contact Manager =====
1. Add Contact
2. Update Contact
3. View Contacts
4. Search Contacts
5. Toggle Favorite
6. Delete Contact
7. Save and Exit"""

# Maps each menu choice to its handler. "7" (save and exit) is handled in
# main() because it ends the loop.
ACTIONS = {
    "1": add_contact,
    "2": update_contact,
    "3": view_contacts,
    "4": search_contacts,
    "5": toggle_favorite,
    "6": delete_contact,
}


def main():
    """Load saved contacts and run the menu until the user exits."""
    manager = ContactManager(load_contacts())

    while True:
        print(MENU)
        choice = input("Choose: ").strip()

        if choice == "7":
            save_contacts(manager.contacts)
            print("Contacts saved. Goodbye!")
            break

        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice.")
            continue
        action(manager)


if __name__ == "__main__":
    main()
