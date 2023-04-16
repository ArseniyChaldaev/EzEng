import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class UserTask(SqlAlchemyBase):
    __tablename__ = 'users_tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    task_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("tasks.id"))
    result = sqlalchemy.Column(sqlalchemy.Boolean)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)