from datetime import datetime

from sqlalchemy import MetaData, Table, Column, ForeignKey, TIMESTAMP, String, Integer, JSON

metadata = MetaData()

party = Table(
    "party",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("date", TIMESTAMP, nullable=False),
    Column("owner_id", Integer, ForeignKey("users.id")),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("register_at", TIMESTAMP, default=datetime.utcnow),
)
