from Bot import Bot
from ConsoleUI import ConsoleUI


if __name__ == "__main__":
    print('Hello. I am your contact-assistant. What should I do with your contacts?')
    ui = ConsoleUI()  # Змінено, тепер використовуємо ConsoleUI замість Bot
    bot = Bot(ui)     # Передаємо об'єкт ConsoleUI у Bot
    bot.book.load("auto_save")
    commands = ['Add', 'Search', 'Edit', 'Load', 'Remove', 'Save', 'Congratulate', 'View', 'Exit']
    while True:
        action = input('Type help for list of commands or enter your command\n').strip().lower()
        if action == 'help':
            format_str = str('{:%s%d}' % ('^',20))
            bot.ui.show_available_commands(commands, format_str)

            action = input().strip().lower()
            bot.handle(action)
            if action in ['add', 'remove', 'edit']:
                bot.book.save("auto_save")
        else:
            bot.handle(action)
            if action in ['add', 'remove', 'edit']:
                bot.book.save("auto_save")
        if action == 'exit':
            break
