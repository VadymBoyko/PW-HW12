from datetime import datetime, timedelta

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(db: Session, user: User):
    contacts = db.query(Contact).join(User).filter(User.id == user.id)
    return contacts


async def get_contact_by_id(db: Session, user: User, contact_id: int):
    contact = db.query(Contact).join(User).filter(and_(Contact.id == contact_id, User.id == user.id)).first()
    return contact


async def get_next_week_birthday_contacts(db: Session, user: User):
    today = datetime.today()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).join(User).filter(
        and_(
            func.to_char(Contact.birthday, 'MM-DD') >= func.to_char(today, 'MM-DD'),
            func.to_char(Contact.birthday, 'MM-DD') <= func.to_char(next_week, 'MM-DD'),
            User.id == user.id
        )
    ).all()
    return contacts


async def get_contact_by_email(db: Session, user: User, email: str):
    contact = db.query(Contact).join(User).filter(
        and_(Contact.email.ilike(email),
             User.id == user.id)).first()
    return contact


async def get_contact_by_firstname(db: Session, user: User, firstname: str):
    contacts = db.query(Contact).join(User).filter(
        and_(Contact.firstname.ilike(firstname),
             User.id == user.id)).first()
    return contacts


async def get_contact_by_lastname(db: Session, user: User, lastname: str):
    contacts = db.query(Contact).join(User).filter(
        and_(Contact.lastname.ilike(lastname),
             User.id == user.id)).first()
    return contacts


async def create(db: Session, user: User, body: ContactModel):
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(db: Session, user: User, contact_id: int, body: ContactModel):
    contact = await get_contact_by_id(db, user, contact_id)
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.notes = body.notes
        db.commit()
    return contact


async def remove(db: Session, user: User, contact_id: int):
    contact = await get_contact_by_id(db, user, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
