import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class UserWord(SqlAlchemyBase):
    __tablename__ = 'users_words'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    word_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("words.id"))
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)