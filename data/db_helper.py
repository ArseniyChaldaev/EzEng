from typing import Optional, Type

from sqlalchemy import func

from constants import DB_PATH
from data import db_session
from data.schedules import Schedule
from data.tasks import Task
from data.users import User
from data.users_tasks import UserTask
from data.users_words import UserWord
from data.words import Word


class Database:
    def __init__(self):
        db_session.global_init(DB_PATH)
        self.db = db_session.create_session()

    def save_user(self, chat) -> User:
        user = self.db.query(User).filter_by(id=chat.id).first()
        if user:
            user.first_name = chat.first_name
            user.last_name = chat.last_name
            user.username = chat.username
        else:
            user = User(
                id=chat.id,
                first_name=chat.first_name,
                last_name=chat.last_name,
                username=chat.username
            )
            self.db.add(user)
        self.db.commit()

        return user

    def get_users(self) -> list[Type[User]]:
        return self.db.query(User).all()

    def get_task(self, user_id, theme, difficult) -> Optional[Task]:
        subquery = self.db.query(UserTask.id).filter_by(user_id=user_id)
        query = self.db.query(Task).filter(Task.theme == theme and
                                           Task.difficult == difficult and
                                           Task.id.not_in(subquery))

        return query.order_by(func.random()).first()

    def save_user_task(self, user_id, task_id) -> UserTask:
        user_task = UserTask(
            user_id=user_id,
            task_id=task_id
        )
        self.db.add(user_task)
        self.db.commit()

        return user_task

    def get_word(self, user_id) -> Optional[Word]:
        subquery = self.db.query(UserWord.id).filter_by(user_id=user_id)
        return self.db.query(Word).filter(Word.id.not_in(subquery)).order_by(func.random()).first()

    def save_user_word(self, user_id, word_id) -> UserWord:
        user_word = UserWord(
            user_id=user_id,
            word_id=word_id
        )
        self.db.add(user_word)
        self.db.commit()

        return user_word

    def save_schedule(self, user_id: int, hour: int) -> Schedule:
        sch = self.db.query(Schedule).filter_by(id=user_id).first()
        if sch:
            sch.hour = hour
        else:
            sch = Schedule(user_id=user_id, hour=hour)
            self.db.add(sch)
        self.db.add(sch)
        self.db.commit()

        return sch

    def get_schedules_by_hour(self, hour: int) -> list[Type[Schedule]]:
        return self.db.query(Schedule).filter_by(hour=hour).all()
