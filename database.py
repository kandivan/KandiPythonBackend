from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from enum import Enum

Base = declarative_base()
class EventType(Enum):
    Invalid = 0
    Registration = 1
    Login = 2 
    Logout = 3
    RequestAiGeneration = 4
    CompleteAiGeneration = 5
    OpenDashboard = 6
    OpenProfile = 7

    
class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(8000))
    description = Column(String(8000))
    location = Column(String(8000))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    host_id = Column(Integer, ForeignKey('users.id'))
    session_id = Column(String(200))

class User(Base, UserMixin):
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(200), unique=True)
    password = Column(String(1000)) # This is a salty pass
    
    @property
    def is_active(self):
        return True
    def set_password(self, bcrypt: Bcrypt, password: str):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, bcrypt: Bcrypt, password: str):
        return bcrypt.check_password_hash(self.password, password)
    
class Payments(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    timestamp = Column(DateTime)

    
class Database:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/KandiStack')
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

