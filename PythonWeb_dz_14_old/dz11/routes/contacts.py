from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from dz11.database.db import get_db
from dz11.schemas import ContactModel, ContactResponse
from dz11.database.models import Contact, User
from dz11.repository import contacts as repository_contacts
from dz11.services.auth import auth_service

# router = APIRouter(prefix='/contacts', contacts=["contacts"])
router = APIRouter(prefix='/contacts')


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_new_contact function creates a new contact in the database.
        The function takes a ContactBase object as input, which is then used to create the new contact.
        The current_user variable is used to determine who created this contact.
    
    :param body: ContactBase: Get the data from the request body
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the user who is making the request
    :return: A contactbase object
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, current_user, db)

# @router.get("/", response_model=List[ContactResponse])
# async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     contact = await repository_contacts.get_contacts(skip, limit, db)
#     return contact

@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, name: str or None = None, surname: str or None = None, email: str or None = None, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_all_contacts function returns a list of contacts.
        The function takes in an optional skip and limit parameter to paginate the results.
        
    
    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contacts(skip, limit, name, surname, email, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contact


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact_by_id function returns a contact by its id.
        If the user is not logged in, an HTTP 401 Unauthorized error is returned.
        If the user does not have access to this contact, an HTTP 403 Forbidden error is returned.
        If no such contact exists with that id, an HTTP 404 Not Found error is returned.
    
    :param contact_id: int: Specify the contact id to be retrieved from the database
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object, which is a pydantic model
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ContactModel object containing the new values for the contact.
            - contact_id: An integer representing the id of an existing contact to be updated.
            - db (optional): A Session object used to connect to and query a database, defaults to None if not provided. 
                If no db is provided, one will be created using get_db().
    
    :param body: ContactModel: Pass the contact information in json format
    :param contact_id: int: Identify the contact to be updated
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is currently logged in
    :return: A contactmodel, which is the same as what we get from the create_contact function
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session, optional): A database session object for interacting with the database. Defaults to Depends(get_db).
            current_user (User, optional): The user currently logged in and making this request. Defaults to Depends(auth_service.get_current_user).
        Returns:
            Contact: A Contact object representing the deleted record in JSON format.
    
    :param contact_id: int: Identify the contact that is to be removed
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/birthdays/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def upcoming_birthdays(db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The upcoming_birthdays function returns a list of contacts with upcoming birthdays.
        The function takes in the current user and database as parameters, then uses the repository_contacts module to query for contacts with upcoming birthdays.
        If no contact is found, an HTTPException is raised.
    
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user from the database
    :return: A list of contacts and their birthdays
    :doc-author: Trelent
    """
    contact = await repository_contacts.upcoming_birthdays(current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contact

