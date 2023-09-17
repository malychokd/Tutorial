from mongoengine import Document, StringField, BooleanField, connect

uri = "mongodb+srv://dmalychok:<password>@dmalychok.jkhjofs.mongodb.net/?retryWrites=true&w=majority"

connect(db='dmalychok', host=uri)

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)

    def to_dict(self):
        return {
            'id': str(self.id),
            'fullname': self.fullname,
            'email': self.email,
            'sent': self.sent
        }
