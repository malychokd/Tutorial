from typing import List

from sqlalchemy.orm import Session

from dz11.database.models import Contact
from dz11.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(name=body.name)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact or None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact .name = body.name
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact or None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact