import pika
import json
from faker import Faker
from models import Contact
from mongoengine import connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# Створення черги для відправки
channel.queue_declare(queue='email_queue')

def main():
    # Генерація фейкових контактів та надсилання їх до черги
    fake = Faker()
    for _ in range(10):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            sent=False
        )
        contact.save()
        message = {
            'contact_id': str(contact.id)
        }
        channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))

    print(" [x] Sent messages")

    # Закриваємо підключення до RabbitMQ
    connection.close()

if __name__ == '__main__':
    main()