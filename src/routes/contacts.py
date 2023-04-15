from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], name="Return all contacts")
async def get_contacts(db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(db, current_user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, name="Return contact by id")
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_id(db, current_user, contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/search_by_lastname/{contact_lastname}", response_model=List[ContactResponse], name="Return contact by lastname")
async def get_contact_by_lastname(lastname: str, db: Session = Depends(get_db),
                                  current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contact_by_lastname(db, current_user, lastname)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/search_by_firstname/{contact_firstname}", response_model=List[ContactResponse], name="Return contact by firstname")
async def get_contact_by_firstname(firstname: str, db: Session = Depends(get_db),
                                   current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contact_by_firstname(db, current_user, firstname)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/next_week_birthday/", response_model=List[ContactResponse], name="Return all contacts who have birthday next 7 days")
async def get_contacts(db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_next_week_birthday_contacts(db, current_user)
    return contacts


@router.post("/", response_model=ContactResponse, name="Create contact", status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(db, current_user, body.email)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')
    contact = await repository_contacts.create(db, current_user, body)
    return contact


@router.put("/{contact_id}", name="Update contact by id", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update(db, current_user, contact_id, body)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", name="Delete contact by id", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove(db, current_user, contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
