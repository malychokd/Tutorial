import json
from mongoengine import Document, StringField, ListField, ReferenceField, connect

uri = "mongodb+srv://dmalychok:<password>@dmalychok.jkhjofs.mongodb.net/?retryWrites=true&w=majority"

connect(db='dmalychok', host=uri)

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

# Функція для завантаження авторів з JSON-файлу та збереження їх у колекції authors
def load_authors_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

def load_quotes_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                quote = Quote(
                    tags=quote_data['tags'],
                    author=author,
                    quote=quote_data['quote']
                )
                quote.save()
            else:
                print(f"Автор '{author_name}' не знайдений.")


def main():
    
    while True:
        command = input('Введіть команду: ')
        if command == 'exit':
            break
        elif command == 'load':
            load_authors_from_json('authors.json')
            load_quotes_from_json('quotes.json')
        elif command.lower().startswith('name:'):
            author_name = command.split(':')[1].strip()
            author = Author.objects(fullname=author_name).first()
            if author:
                author_quotes = Quote.objects(author=author)
                for quote in author_quotes:
                    print(quote.quote)
            else:
                print(f"Автор {author_name} не знайдений.")
        elif command.startswith('tag:'):
            tag_name = command.split(':')[1].strip()
            tag_quotes = Quote.objects(tags=tag_name)
            for quote in tag_quotes:
                print(quote.quote)
        elif command.startswith('tags:'):
            tag_names = command.split(':')[1].strip().split(',')
            tag_quotes = Quote.objects(tags__in=tag_names)
            for quote in tag_quotes:
                print(quote.quote)
        else:
            print('Невідома команда')


if __name__ == '__main__':
    main()

