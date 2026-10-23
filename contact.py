"""Contact model and field validation."""

import re

# Phone: optional leading '+', then digits, spaces, parentheses or hyphens.
PHONE_PATTERN = re.compile(r"\+?[0-9][0-9 ()\-]*")

# Email: simplified RFC 5322 rules (local part + domain with a TLD).
LOCAL_PATTERN = re.compile(
    r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
)
DOMAIN_PATTERN = re.compile(
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}"
)


# --- Validators -------------------------------------------------------------
# Each validator returns the cleaned value or raises ValueError. They are
# public so the UI can re-prompt the user on a single bad field instead of
# making them retype the whole contact.

def validate_name(name):
    """Return the stripped name; it must be at least 2 characters."""
    name = str(name).strip()
    if len(name) < 2:
        raise ValueError("Name cannot be less than 2 characters.")
    return name


def validate_phone(phone_number):
    """Return the stripped phone number if it is well formed."""
    if not isinstance(phone_number, str):
        raise ValueError("Phone number must be text.")
    phone_number = phone_number.strip()
    if not PHONE_PATTERN.fullmatch(phone_number):
        raise ValueError(
            "Phone number may contain only digits, spaces, parentheses, "
            "hyphens, and a leading '+'."
        )
    digit_count = len(re.sub(r"\D", "", phone_number))
    if not 8 <= digit_count <= 15:
        raise ValueError("Phone number must contain between 8 and 15 digits.")
    if phone_number.count("(") != phone_number.count(")"):
        raise ValueError("Phone number parentheses must be balanced.")
    return phone_number


def validate_email(email):
    """Return the stripped email address if it is well formed."""
    if not isinstance(email, str):
        raise ValueError("Email address must be text.")
    email = email.strip()
    if len(email) > 254:
        raise ValueError("Email address is too long.")
    local_part, separator, domain = email.partition("@")
    if (
        not separator
        or len(local_part) > 64
        or not LOCAL_PATTERN.fullmatch(local_part)
        or not DOMAIN_PATTERN.fullmatch(domain)
    ):
        raise ValueError("Email address must have a valid local part and domain.")
    return email


# --- Model ------------------------------------------------------------------

class Contact:
    """A single contact. Required fields are validated on creation."""

    def __init__(self, name, phone_number, email,
                 address="", birthday="", notes="", favorite=False):
        self.name = validate_name(name)
        self.phone_number = validate_phone(phone_number)
        self.email = validate_email(email)
        self.address = address
        self.birthday = birthday  # free text, e.g. "1999-04-21"
        self.notes = notes
        self.favorite = bool(favorite)

    def toggle_favorite(self):
        """Flip the favorite flag."""
        self.favorite = not self.favorite

    def to_dict(self):
        """Serialize to a dict (used by storage.py)."""
        return {
            "Name": self.name,
            "Phone Number": self.phone_number,
            "Email": self.email,
            "Address": self.address,
            "Birthday": self.birthday,
            "Notes": self.notes,
            "Favorite": self.favorite,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Contact from a dict; optional keys fall back to defaults."""
        return cls(
            name=data["Name"],
            phone_number=data["Phone Number"],
            email=data["Email"],
            address=data.get("Address", ""),
            birthday=data.get("Birthday", ""),
            notes=data.get("Notes", ""),
            favorite=data.get("Favorite", False),
        )

    def __str__(self):
        star = "★ " if self.favorite else ""
        return f"{star}{self.name} (Phone: {self.phone_number}, Email: {self.email})"
