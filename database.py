from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(8000))
    email = Column(String(8000))
    password = Column(String(8000))
    profile = relationship('Profile', uselist=False, back_populates='user')
    posts = relationship('Post', back_populates='author')
    
class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bio = Column(String(8000))
    location = Column(String(8000))
    user = relationship('User', back_populates='profile')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(8000))
    content = Column(String(8000))
    timestamp = Column(DateTime)
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String(8000))
    timestamp = Column(DateTime)
    post = relationship('Post', back_populates='comments')
    
class Database:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/PinzakTest')
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

