from datetime import datetime

class Field:
    def __init__(self, value=None):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not self.validate(value):
            raise ValueError("Invalid value for field")
        self.value = value

    def validate(self, value):
        return True


class Phone(Field):
    def validate(self, value):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            return False
        return True


class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = None

        if birthday:
            try:
                self.birthday = datetime.strptime(birthday, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid birthday format (use YYYY-MM-DD)")

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.now()
        next_birthday = datetime(today.year, self.birthday.month, self.birthday.day)

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.month, self.birthday.day)

        days_left = (next_birthday - today).days
        return days_left
    
    def __str__(self):
        phone_str = f"Phone: {self.phone}\n" if self.phone else ""
        birthday_str = f"Birthday: {self.birthday.strftime('%Y-%m-%d')}" if self.birthday else ""
        return f"\nName: {self.name}\n{phone_str}{birthday_str}"


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def find_contacts_with_birthday(self):
        return [contact for contact in self.contacts if contact.birthday]

    def __iter__(self):
        return iter(self.contacts)

# test
contact1 = Record("John Doe", "1234567890", "1990-05-15")
contact2 = Record("Bob Johnson", birthday="1985-08-20")

address_book = AddressBook()
address_book.add_contact(contact1)
address_book.add_contact(contact2)

for contact in address_book.find_contacts_with_birthday():
    print(contact)
    days_left = contact.days_to_birthday()
    if days_left is not None:
        print(f"{contact.name}: {days_left} days until their next birthday")
