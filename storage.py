"""Load and save contacts as JSON."""

import json
import os
import tempfile

from contact import Contact

# Store the file next to the program so it works from any working directory.
CONTACTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.json")


def load_contacts():
    """Return the saved contacts, or an empty list if none/unreadable."""
    if not os.path.exists(CONTACTS_FILE):
        return []

    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read contacts file; starting empty.")
        return []

    contacts = []
    for item in data:
        try:
            contacts.append(Contact.from_dict(item))
        except (KeyError, ValueError, TypeError, AttributeError) as error:
            # Skip a bad record rather than losing the whole file.
            print(f"Warning: skipped an invalid saved contact ({error!r}).")
    return contacts


def save_contacts(contacts):
    """Write contacts to disk.

    Writes to a temp file first and then swaps it in, so a crash mid-write
    can't corrupt the existing contacts file.
    """
    data = [contact.to_dict() for contact in contacts]
    directory = os.path.dirname(CONTACTS_FILE)
    fd, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(temp_path, CONTACTS_FILE)
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise
