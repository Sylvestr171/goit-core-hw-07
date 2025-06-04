from collections import UserDict
from datetime import datetime, date, timedelta

#клас для кастомних помилок
class CastomError(Exception):
    def __init__(self, message="Custom Error"):
        self.message = message
        super().__init__(self.message)

# Базовий клас для полів запису.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Ім'я не може бути порожнім.")
        super().__init__(value)


# Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, value):
        if len(value)==10 and value.isdigit():
            super().__init__(value)
        else:
            # raise ValueError(f"{ValueError}\nНе вірний формат номера")
            raise CastomError('Не вірний формат номера')
    
    def __eq__(self, other):
        eq = (self.value == other.value)
        return eq
    
    def __repr__(self): #оскільки помилки усував коли вже познайомився з repr додав його щоб не танцювати з бубном при виводі об'єкта
        return f"{self}"
    
class Birthday(Field):
    def __init__(self, value):
        try:
            # datetime.strptime(value, "%d.%m.%Y")
            super().__init__(datetime.strptime(value, "%d.%m.%Y").date())
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

# Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
   
    def add_phone(self, phone: str):
        if Phone(phone) not in self.phones:
            self.phones.append(Phone(phone))
        else:
            raise CastomError (f'{phone} is already present in the notebook for {self.name}')

    def remove_phone(self, phone):
        if Phone(phone) in self.phones:
            self.phones.remove(Phone(phone))
        else:
            raise CastomError (f'{phone} відсутній в {self.name}')

    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone):
            raise CastomError('Is not such number for contact')
        self.add_phone(new_phone)
        self.remove_phone(old_phone)
    
        

    def find_phone(self, phone_for_search): 
        for item in self.phones:
            if item == Phone(phone_for_search):
                return item
    
    def add_birthday(self, b_date):
        self.birthday = Birthday(b_date)
        return self.birthday
    
    def __str__(self):
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

    def add_record(self, value):
        key = value.name.value
        value = value
        self.data[key] = value

    def find(self, search_value):
        return self.data.get(search_value, None)
    
    def delete(self, delete_value):
        if delete_value in self.data.keys():
            del self.data[delete_value]
    
    @staticmethod
    def find_next_weekday(start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)
    
    
    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday

    # def get_upcoming_birthdays(self, users, days=7):
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for key, value in self.data.items():
            
            birthday_this_year = value.birthday.value.replace(year=today.year)
                
            if birthday_this_year < today:
                birthday_this_year = value.birthday.value.replace(year=today.year+1)

            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = self.adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append({"name": value.name.value, "birthday": str(birthday_this_year)})

        return upcoming_birthdays
    
    def __str__(self):
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
    print(f"{john}")

    john.edit_phone("1234567890", "1111111111")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()