from sqlalchemy import (
    Column, TEXT, Integer, String, MetaData, Table, ForeignKey, UniqueConstraint
)


metadata = MetaData()


user_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('login', String(255), nullable=False, unique=True),
    Column('password', String(255), nullable=False),
    Column('name', String(255), nullable=False, default=''),
    Column('surname', String(255), nullable=False, default=''),
    Column('age', Integer, nullable=True),
    Column('gender', String(255), nullable=False, default=''),
    Column('hobbies', TEXT, nullable=False, default=''),
    Column('city', String(255), nullable=False, default=''),
)


user_friend = Table(
    'user_friends',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('users.id')),
    Column('friend_id', ForeignKey('users.id')),
    UniqueConstraint('user_id', 'friend_id')
)
