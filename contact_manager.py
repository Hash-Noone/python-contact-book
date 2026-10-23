"""Business logic for managing a list of contacts (no input/print here)."""

from contact import Contact


class ContactManager:
    """Holds the contact list and provides add/update/delete/search."""

    def __init__(self, contacts=None):
        self.contacts = contacts if contacts is not None else []

    def add_contact(self, contact):
        """Add a Contact instance to the list."""
        if not isinstance(contact, Contact):
            raise ValueError("Only Contact instances can be added.")
        self.contacts.append(contact)

    def update_contact(self, old_contact, **changes):
        """Replace a contact with an updated copy.

        `changes` may contain any Contact field (name, phone_number, email,
        address, birthday, notes, favorite). The new Contact is built, and
        therefore validated, before anything is replaced, so a bad value
        leaves the original untouched.
        """
        index = self._index_of(old_contact)
        fields = {
            "name": old_contact.name,
            "phone_number": old_contact.phone_number,
            "email": old_contact.email,
            "address": old_contact.address,
            "birthday": old_contact.birthday,
            "notes": old_contact.notes,
            "favorite": old_contact.favorite,
        }
        fields.update(changes)
        self.contacts[index] = Contact(**fields)  # raises ValueError if invalid

    def toggle_favorite(self, contact):
        """Flip the favorite flag on a contact in the list."""
        self._index_of(contact)  # raises if not present
        contact.toggle_favorite()

    def delete_contact(self, contact):
        """Remove a contact from the list."""
        self.contacts.pop(self._index_of(contact))

    def search(self, query):
        """Return contacts whose name contains `query` (case-insensitive)."""
        query = query.strip().lower()
        return [c for c in self.contacts if query in c.name.lower()]

    def _index_of(self, contact):
        """Find a contact by identity; raise if it isn't in the list."""
        for i, existing in enumerate(self.contacts):
            if existing is contact:
                return i
        raise ValueError("Contact not found in the list.")
