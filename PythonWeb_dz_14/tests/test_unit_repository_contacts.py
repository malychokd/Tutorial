import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dz11.database.models import Contact, User
from dz11.schemas import ContactModel, ContactResponse
from dz11.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    remove_contact,
    upcoming_birthdays,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.body = ContactModel(
            id=1,
            first_name='Denys',
            last_name='Malychok',
            email='d.malychok@ukr.net',
            phone='+380976250800',
            birthday=datetime.date(year=1988, month=8, day=11)
        )

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(note_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(note_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        contact = await create_contact(self.body, self.user, self.session)
        self.assertEqual(contact.first_name, self.body.first_name)
        self.assertEqual(contact.last_name, self.body.last_name)
        self.assertEqual(contact.email, self.body.email)
        self.assertEqual(contact.phone, self.body.phone)
        self.assertEqual(contact.birthday, self.body.birthday)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(note_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(note_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactResponse(
                id=1,
                first_name='Denys2',
                last_name='Malychok2',
                email='d.malychok2@ukr.net',
                phone='+380976250802',
                birthday=datetime.date(year=1988, month=8, day=11))
        self.session.query().filter().first.return_value = self.body
        result = await update_contact(note_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)

    
if __name__ == '__main__':
    unittest.main()
