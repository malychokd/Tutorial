import pika
import json
from models import Contact
from time import sleep

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

# Функція для імітації відправлення email
def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Sending email to {contact.email}...")
        contact.sent = True
        contact.save()

# Функція обробки повідомлення з черги
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    send_email(contact_id)
    print(f" [x] Processed message for contact ID: {contact_id}")

# Встановлюємо функцію обробки повідомлень для черги
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

if __name__ == '__main__':
    channel.start_consuming()
