import datetime
import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Filmwork:

    id: uuid.UUID
    title: str
    description: str = ''
    creation_date: datetime = None
    certificate: str = ''
    rating: float = field(default=0.0)
    type: str = ''
    created_at: datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime = field(default_factory=datetime.datetime.now)
    file_path: str = None
    # table = "film_work"


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str
    description: str = field(default=None)
    created_at: datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime = field(default_factory=datetime.datetime.now)
    # table = 'ganre'


@dataclass(frozen=True)
class Person:
    id: uuid.UUID
    full_name: str
    created_at: datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime = field(default_factory=datetime.datetime.now)
    # table = 'person'


@dataclass(frozen=True)
class FilmworkGenre:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime = field(default_factory=datetime.datetime.now)


@dataclass(frozen=True)
class FilmworkPerson:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime = field(default_factory=datetime.datetime.now)
