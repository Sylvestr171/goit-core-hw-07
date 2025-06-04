from collections import UserDict
from datetime import datetime, date, timedelta
from typing import Any, Union

#клас для кастомних помилок
class CastomError(Exception):
    def __init__(self, message :str ="Custom Error") -> None:
        self.message = message
        super().__init__(self.message)

# Базовий клас для полів запису.
class Field:
    def __init__(self, value :Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

# Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, value :str) -> None:
        if not value:
            raise ValueError("Ім'я не може бути порожнім.")
        super().__init__(value)


# Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, value :str) -> None:
        if len(value)==10 and value.isdigit():
            super().__init__(value)
        else:
            raise CastomError('Не вірний формат номера')
    
    def __eq__(self, other :object) -> bool:
        if not isinstance(other, Phone):
            return NotImplemented
        eq = (self.value == other.value)
        return eq
    
    def __repr__(self) -> str:
        return f"{self}"
    
class Birthday(Field):

    def __init__(self, value :str) -> None:
        try:
            # datetime.strptime(value, "%d.%m.%Y")
            value_in_date=(datetime.strptime(value, "%d.%m.%Y").date())
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value_in_date.strftime("%d.%m.%Y"))

# Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
class Record:
    def __init__(self, name :str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None
   
    def add_phone(self, phone :str) -> None:
        if Phone(phone) not in self.phones:
            self.phones.append(Phone(phone))
        else:
            raise CastomError (f'{phone} is already present in the notebook for {self.name}')

    def remove_phone(self, phone :str) -> None:
        if Phone(phone) in self.phones:
            self.phones.remove(Phone(phone))
        else:
            raise CastomError (f'{phone} відсутній в {self.name}')

    def edit_phone(self, old_phone :str, new_phone :str) -> None:
        if not self.find_phone(old_phone):
            raise CastomError('Is not such number for contact')
        self.add_phone(new_phone)
        self.remove_phone(old_phone)
    
    def find_phone(self, phone_for_search :str) -> Union[Phone, None]: 
        for item in self.phones:
            if item == Phone(phone_for_search):
                return item
    
    def add_birthday(self, b_date :str) -> Birthday:
        self.birthday = Birthday(b_date)
        return self.birthday
    
    def __str__(self) -> str:
        if self.birthday:
            birthday=self.birthday
        else:
            birthday='не відомо'
        if self.phones:
            phone='; '.join(p.value for p in self.phones)
        else: 
            phone='телефон відсутній' 

        return f"Contact name: {self.name.value}, phones: {phone}, birthday: {birthday}"

#Клас для зберігання та управління записами.
class AddressBook(UserDict):

    def add_record(self, value :Record) -> None:
        key = value.name.value
        value = value
        self.data[key] = value

    def find(self, search_value :str) -> Union[Record, None]:
        return self.data.get(search_value, None)
    
    def delete(self, delete_value :str) -> None:
        if delete_value in self.data.keys():
            del self.data[delete_value]
    
    @staticmethod
    def find_next_weekday(start_date :date, weekday :int) ->date:
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)
    
    
    def adjust_for_weekend(self, birthday :date) -> date:
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday

    # def get_upcoming_birthdays(self, users, days=7):
    def get_upcoming_birthdays(self, days :int =7) -> list[dict]:
        upcoming_birthdays = []
        today = date.today()

        for key, value in self.data.items():
            
            
            if value.birthday:
                date_format_date=datetime.strptime(value.birthday.value, "%d.%m.%Y").date()
            else: 
                continue

            birthday_this_year = date_format_date.replace(year=today.year)
                
            if birthday_this_year < today:
                birthday_this_year = date_format_date.replace(year=today.year+1)

            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = self.adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append({"name": value.name.value, "birthday": str(birthday_this_year)})

        return upcoming_birthdays
    
    def __str__(self) -> str:
        result = []
        for name, record in self.data.items():
            result.append(f"Address book {name}:\n {record}")
        return "\n".join(result)

def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    print(f'1){john_record}')
    john_record.add_phone("1234567890")
    print(f'2){john_record}')
    john_record.add_phone("5555555555")
    print(f'3){john_record}')

    ####
    ####
    ####
    john_record.add_birthday("07.06.2005")
    print(f'4){john_record}')
    ####
    ####
    ####

    # Додавання запису John до адресної книги
    book.add_record(john_record)
    print (book)


    ###
    ###
    ###
    print(f"UPKOMING METHOD: {book.get_upcoming_birthdays()}")
    ###
    ###
    ###
    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    if john is not None:
        print(f"{john}")

        john.edit_phone("1234567890", "1111111111")

        print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

        # Пошук конкретного телефону у записі John
        found_phone = john.find_phone("5555555555")
        print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555
    else: 
        raise AttributeError(f"book.find('John') return NONE")

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()