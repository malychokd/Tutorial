from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from dz11.database.db import get_db
from dz11.schemas import ContactModel, ContactResponse
from dz11.repository import contacts as repository_contacts

# router = APIRouter(prefix='/contacts', contacts=["contacts"])
router = APIRouter(prefix='/contacts')


# @router.get("/", response_model=List[ContactResponse])
# async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     contact = await repository_contacts.get_contacts(skip, limit, db)
#     return contact

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, name: str or None = None, surname: str or None = None, email: str or None = None, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contacts(skip, limit, name, surname, email, db)
    return contact


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/birthdays/", response_model=List[ContactResponse])
async def upcoming_birthdays(db: Session = Depends(get_db)):
    contact = await repository_contacts.upcoming_birthdays(db)
    return contact
