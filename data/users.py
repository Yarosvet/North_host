import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase, create_session
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


#  Класс пользователя
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    files = orm.relation("Files", back_populates='user')

    #  Первая установка пароля
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    #  Проверка пароля
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    #  Изменение пароля
    def change_password(self, id_to_update, password):
        session = create_session()
        try:
            session.query(User).filter(User.id == id_to_update). \
                update({User.hashed_password: generate_password_hash(password)}, synchronize_session=False)
            session.commit()
            self.hashed_password = generate_password_hash(password)
        except Exception as exc:
            session.rollback()
            return str(exc)
        return False
