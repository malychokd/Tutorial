from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from dz11.database.models import Contact, User
from dz11.schemas import ContactModel

from sqlalchemy import and_, or_, extract


async def get_contacts(skip: int, limit: int, name: str, surname: str, email: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts.
    
    :param skip: int: Skip the first n contacts in the list
    :param limit: int: Limit the number of contacts returned
    :param name: str: Filter the contacts by name
    :param surname: str: Filter the contacts by surname
    :param email: str: Filter the contacts by email
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    result = db.query(Contact).filter(Contact.user_id == user.id)
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
        result = db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()
    else:
        result = result.all()
    
    return result


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function returns a contact from the database.
        Args:
            contact_id (int): The id of the contact to be returned.
            user (User): The user who owns the requested Contact object.
            db (Session): A database session for querying and updating data in a relational database.
    
    :param contact_id: int: Specify the id of the contact that we want to get
    :param user: User: Get the user id from the logged in user
    :param db: Session: Access the database
    :return: The first contact in the database that matches a user's id and a contact_id
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactModel: Receive the request body
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact or None:
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated Contact object to be stored in the database.
            user (User): The current logged-in user, used for authorization purposes.
            db (Session): A connection to our SQLite3 database, used for querying and updating data.
    
    :param contact_id: int: Identify the contact that we want to update
    :param body: ContactModel: Get the new contact information from the request body
    :param user: User: Get the user id of the logged in user
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        contact.name = body.name
        contact.surname=body.surname
        contact.email=body.email
        contact.phone=body.phone
        contact.birthday=body.birthday
        contact.description=body.description
        contact.user_id=user.id
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session)  -> Contact or None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who owns the contacts list.
            db (Session): A connection to our database, used for querying and deleting data.
        Returns: 
            Contact or None: If successful, returns a Contact object representing the deleted record; otherwise returns None.
    
    :param contact_id: int: Identify the contact that is to be removed
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A contact object or none
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def upcoming_birthdays(user: User, db: Session)-> List[Contact]:
    """
    The upcoming_birthdays function returns a list of contacts whose birthdays are within the next 7 days.
        Args:
            user (User): The user who owns the contacts.
            db (Session): A database session to query for upcoming birthdays.
    
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts whose birthday is within the next 7 days
    :doc-author: Trelent
    """
    today = datetime.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        and_(
            extract('month', Contact.birthday) == today.month,
            extract('day', Contact.birthday) >= today.day,
            extract('day', Contact.birthday) <= end_date.day,
            Contact.user_id == user.id)
        ).all()
    return contacts
