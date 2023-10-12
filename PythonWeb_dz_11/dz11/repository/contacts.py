from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from dz11.database.models import Contact
from dz11.schemas import ContactModel

from sqlalchemy import and_, or_, extract


async def get_contacts(skip: int, limit: int, name: str, surname: str, email: str, db: Session) -> List[Contact]:
    result = db.query(Contact)
    not_filtred = True
    if name:
        result = result.filter(Contact.name == name)
        not_filtred = False
    if surname:
        result = result.filter(Contact.surname == surname)
        not_filtred = False
    if email:
        result = result.filter(Contact.email == email)
        not_filtred = False
    if not_filtred:
        result = db.query(Contact).offset(skip).limit(limit).all()
    else:
        result = result.all()
    
    return result


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact or None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname=body.surname
        contact.email=body.email
        contact.phone=body.phone
        contact.birthday=body.birthday
        contact.description=body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact or None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def upcoming_birthdays(db: Session)-> List[Contact]:
    today = datetime.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        and_(
            extract('month', Contact.birthday) == today.month,
            extract('day', Contact.birthday) >= today.day,
            extract('day', Contact.birthday) <= end_date.day
        )
        ).all()
    return contacts
