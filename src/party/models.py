from datetime import datetime

from src.auth.models import user

from sqlalchemy import Table, Column, TIMESTAMP, String, Integer, MetaData, ForeignKey, PrimaryKeyConstraint

metadata = MetaData()

party = Table(
    'party',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('date', TIMESTAMP, nullable=False),
    Column('owner_id', Integer, ForeignKey(user.c.id, ondelete="CASCADE")),
)

user_party = Table(
    'user_party',
    metadata,
    Column('user_id', Integer, ForeignKey(user.c.id, ondelete="CASCADE")),
    Column('party_id', Integer, ForeignKey(party.c.id, ondelete="CASCADE")),
    PrimaryKeyConstraint('user_id', 'party_id'),
)
