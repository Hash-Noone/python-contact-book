class Contact:
    def __init__(self, name, phone_number, email, address="", birthday="", notes="", favorite = False ):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birthday = birthday
        self.notes = notes
        self.favorite = favorite

    def toggle_favorite(self):
        self.favorite = not self.favorite
