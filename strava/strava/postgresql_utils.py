import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geography

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    avatar = Column(String)
    location = Column(String)
    #uploaded_images = TODO
    num_following = Column(Integer)
    num_followers = Column(Integer)
    #following = TODO
    #followers = TODO
    activities = relationship('Activity', back_populates='user')

# CURRENTLY UNUSED
class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_by = Column(Integer) # TODO link to user table
    data = Column(String)

# CURRENTLY UNUSED
class Club(Base):
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)
    club_name = Column(String)
    club_location = Column(String)
    #club_members = Column() # TODO
    club_num_members = Column(Integer)

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='activities')
    name = Column(String)
    path = Column(Geography('LINESTRING'))
