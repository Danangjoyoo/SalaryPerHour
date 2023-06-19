from typing import List
from sqlalchemy.sql.selectable import Select
from .connection import session
from .models import Base


def get_all(query: Select):
    with session() as sess:
        return sess.execute(query).all()

def get_scalar_all(query: Select):
    with session() as sess:
        return sess.execute(query).scalars().all()

def get_first(query: Select):
    with session() as sess:
        return sess.execute(query).first()

def execute(query: Select):
    with session() as sess:
        sess.execute(query)
        sess.commit()

def bulk_save(object_list: List[Base]):
    with session() as sess:
        sess.bulk_save_objects(object_list)
        sess.commit()