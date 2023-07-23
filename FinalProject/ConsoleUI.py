class ConsoleUI:
    def show_contacts(self, contacts):
        # Виведення інформації про контакт
        for account in contacts:
                if account['birthday']:
                    birth = account['birthday'].strftime("%d/%m/%Y")
                    result = "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {', '.join(account['phones'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50
                    print(result)

    def show_note(self, note):
        # Виведення нотатки
        print(note)

    def show_available_commands(self, commands, format_str):
        # Виведення доступних команд
        for command in commands:
                print(format_str.format(command))
