from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=False)
    notes = Column(String)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', backref='contacts')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


    @hybrid_property
    def days_to_next_birthday(self):
        next_birthday = self.birthday.replace(year=datetime.today().year)
        if next_birthday < datetime.today():
            next_birthday = datetime(next_birthday.year + 1, next_birthday.month, next_birthday.day)
        count_days = (next_birthday - datetime.today()).days
        return count_days



