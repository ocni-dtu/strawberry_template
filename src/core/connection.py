from typing import Generator

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from .config import settings


def create_postgres_engine():
    return create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        pool_pre_ping=True,
        pool_size=settings.POSTGRES_POOL_SIZE,
        max_overflow=settings.POSTGRES_MAX_OVERFLOW,
        # connect_args={"ssl": settings.POSTGRES_SSL},
    )


def get_local_session():
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=create_postgres_engine(),
        class_=Session,
        expire_on_commit=False,
    )


def get_db() -> Generator:
    with get_local_session()() as session:
        yield session
