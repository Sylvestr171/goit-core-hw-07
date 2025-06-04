from random import choice
from pathlib import Path
from classes import AddressBook,CastomError,Record

#Декоратор для обробки помилки ValueError, FileNotFoundError у функціях add_contact, change_contact
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct name and phone please."
        except FileNotFoundError:
            return "How can I help you?"
        # except AttributeError:
        #     return "No birthday on this week"
        except CastomError as e:
            return e
    return inner

#Функція розбору введеного користувачем рядку на команду та її аргументи. 
@input_error
def parse_input(user_input:str) -> tuple[str,*tuple[str,...]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

#Функція отриманн контакту Команда: "add John 1234567890"
@input_error
def add_contact(args:list[str], contacts:AddressBook) -> str:
    name, phone, *_ = args
    name=name.lower().capitalize()
    record = contacts.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        contacts.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

#Функція зміни контакту  Команда: "change John 0987654321"
@input_error
def change_contact(args:list[str], book:AddressBook) -> str:
    name, old_phone, new_phone = args
    if name.lower().capitalize() not in book.keys():
        massage = 'Contact is missing, please add it (add <name> <phone_namer>)! '
    else: 
        book[name.lower().capitalize()].edit_phone(old_phone, new_phone)
        massage = 'Contact updated.'
    return massage

#Функція показати контакти Команда: "phone John"
def show_phone(args:list[str], contacts:AddressBook) -> str:
    name = args[0].lower().capitalize()
    return contacts.get(name, 'The name is missing')

#Функція виведення всієї адресної книги Команда: "all"
def show_all(book:AddressBook) -> str:

    return '\n'.join(f"{key} => {value}" for key, value in book.items())

#функція для вибору рандомної фрази для відповіді на hello
@input_error
def get_random_phrase():
        current_dir = Path(__file__).parent
        with open(current_dir / "hello.txt", "r", encoding="utf-8") as file:
            phrase = file.readlines()
            return choice(phrase).strip()

@input_error
def add_birthday(args, book:AddressBook):
    name, birthday, *_ = args
    name=name.lower().capitalize()
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if birthday:
        record.add_birthday(birthday)
    return message

@input_error
def show_birthday(args, book):
    name = args[0].lower().capitalize()
    result=book.get(name, None)
    if result != None:
        if result.birthday != None:
            return result.birthday
        else:
            raise CastomError("Дата відсутня")
    else:
        raise CastomError("Контакт відсутній")

@input_error
def birthdays(book):
    return book.get_upcoming_birthdays()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        match command:
            case "close" | "exit":
                print("Good bye!")
                break
            
            case "hello":
                print(get_random_phrase())
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(show_all(book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(birthdays(book))
            case "help" | "?":
                print("""The bot helps to work with the contact book.
                        Commands and functions:
                        "close" | "exit" - exit the program
                        "hello" - display a greeting
                        "add <name> <phone_namer>" - add a phone number to the address book
                        "change <name> <phone_namer>" - change the phone number in the address book
                        "add-birthday <name> <DD.MM.YYYY>" - add a birthday to the address book
                        "show-birthday <name>" - show birthday
                        "phone <name>" - show the number
                        "all" - show the entire address book
                        "birthdays" - show date for congratulation
                        "help" | "?" - show this help""")             
            case _:
                print("Invalid command.\nFor help enter: ?, help")

if __name__ == "__main__":
    main()


#  Будь-яка команда, яка не відповідає вищезазначеним форматам, буде вважатися нами невірною, і бот буде виводити повідомлення "Invalid command."
     