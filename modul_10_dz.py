from collections import UserDict

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter contact name"
    return wrapper

def hello_command(params):
    return "How can I help you?"

@input_error
def add_command(params):
    name, phone = params.split(' ')
    record = address_book.search_record(name)
    record.add_phone(phone)
    return f"Contact {name} added"

@input_error
def change_command(params):
    name, phone, new_phone = params.split(' ')
    record = address_book.search_record(name)
    record.edit_phone(phone, new_phone)
    return f"Phone number for {name} changed"

@input_error
def phone_command(params):
    name = params.strip()
    return address_book.search_records(name)
    #name = params.strip()
    #return contacts[name]

def show_all_command(params):
    return address_book.show_all_records()
    #if not contacts:
    #    return "Contact list is empty"
    #else:
    #    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        del self.data[name]

    def search_record(self, search_criteria):
        for record in self.data.values():
            if search_criteria.lower() in record.name.value.lower():
                return record
        record = Record(search_criteria)
        self.add_record(record)
        return record

    def search_records(self, search_criteria):
        results = []
        for record in self.data.values():
            if search_criteria.lower() in record.name.value.lower():
                results.append(record)
        return results
    
    def show_all_records(self):
        results = ''
        for record in self.data.values():
            results += "\n"+f"{record.name.value}:"+"".join(f" {phone.value}" for phone in record.phones)
        if not results:
            results = "Contact list is empty"
        return results    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

def main():
    commands = {
        'hello': hello_command,
        'add': add_command,
        'change': change_command,
        'phone': phone_command,
        'show all': show_all_command,
    }

    while True:
        user_input = input("> ").lower()
        if user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        
        for command, handler in commands.items():
            if user_input.startswith(command):
                params = user_input[len(command):].strip()
                result = handler(params)
                print(result)
                break
        else:
            print("Unknown command")

#contacts = {}
address_book = AddressBook()

if __name__ == "__main__":
    main()
