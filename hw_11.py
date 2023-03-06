from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    @staticmethod
    def valid_phone(phone):
        new_phone = str(phone).strip().removeprefix("+").replace(
            "(", "").replace(")", "").replace("-", "").replace(" ", "")
        try:
            new_phone = [str(int(i)) for i in new_phone]
        except ValueError:
            print("Phone number is not correct. Try again.")

        else:
            new_phone = "".join(new_phone)
            if len(new_phone) == 12:
                return f"+{new_phone}"
            elif len(new_phone) == 10:
                return f"+38{new_phone}"
            else:
                print("Phone number is wrong. Try again")

    def __init__(self, value):
        self._value = Phone.valid_phone(value)

    @Field.value.setter
    def value(self, value):
        self._value = Phone.valid_phone(value)


class Birthday(Field):
    @staticmethod
    def valid_date(year, month, day):
        try:
            birthday = datetime(year=year, month=month, day=day)
        except ValueError:
            print("Date is wrong")
        else:
            return str(birthday.date())

    def __init__(self, year, month, day):
        self.__birthday = self.valid_date(year, month, day)

    def __str__(self):
        return self.__birthday.strftime('%Y-%m-%d')

    def __repr__(self):
        return self.__birthday.strftime('%Y-%m-%d')

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, year, month, day):
        self.__birthday = self.valid_date(year, month, day)


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        if name in self.data:
            self.data.pop(name)

    def all_records(self):
        return {key: value.get_contact() for key, value in self.data.items()}

    def iterator(self):
        for record in self.data.values():
            yield record.get_contact()


class Record:

    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []
        if isinstance(phone, Phone):
            self.phones.append(phone)

    def add_phone(self, new_phone):
        new_phone = Phone(new_phone)
        if new_phone:
            self.phones.append(new_phone)

    def change_phone(self, old_phone, new_phone):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return "phone was changed"

    def remove_phone(self, old_phone):
        old_phone = Phone(old_phone)
        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
            else:
                print(f"This phone {old_phone} is exist in list")

    def days_to_birthday(self):
        today = datetime.now().date()
        current_year = today.year

        if self.birthday is not None:
            birthday_date = datetime(current_year, self.birthday.month,
                                     self.birthday.day).date()
            delta = birthday_date - today
            if delta.days >= 0:
                return f'Left to birthday {delta.days} days.'
            else:
                next_birthday = datetime(current_year + 1,
                                         self.birthday.month,
                                         self.birthday.day).date()
                delta = next_birthday - today
                return f"Birthday will be through {delta.days} days."

    def add_birthday(self, year, month, day):
        self.birthday = Birthday.valid_date(year, month, day)

    def get_contact(self):
        phones = ", ".join([str(ph) for ph in self.phones])
        return {
            "name": str(self.name.value),
            "phone": phones,
            "birthday": self.birthday,
        }


if __name__ == "__main__":

    name_1 = Name("Sem")
    phone_1 = Phone("098-454-58-96")
    record_1 = Record(name_1, phone_1)
    record_1.add_phone("067-897-78-78")
    record_1.change_phone("067-897-78-78", "095-111-0000")

    name_2 = Name("Bill")
    phone_2 = Phone("(067)0000000")
    record_2 = Record(name_2, phone_2)
    record_2.add_phone("555-888-99-66")
    record_2.add_phone("000-777-11-22")

    contacts = AddressBook()
    contacts.add_record(record_1)
    contacts.add_record(record_2)

    record_1.add_birthday(1987, 8, 12)
    print(contacts.all_records())
