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
    contacts[name] = phone
    return f"Contact {name} added"

@input_error
def change_command(params):
    name, phone = params.split(' ')
    contacts[name] = phone
    return f"Phone number for {name} changed"

@input_error
def phone_command(params):
    name = params.strip()
    return contacts[name]

def show_all_command(params):
    if not contacts:
        return "Contact list is empty"
    else:
        return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

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

contacts = {}

if __name__ == "__main__":
    main()
