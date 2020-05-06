import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase, create_session
from config import domain


#  Класс файла
class Files(SqlAlchemyBase):
    __tablename__ = 'files'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    filename = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    upload_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                    default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    #  Перевод в словарь, сериализер не удобный, легче сделать руками
    def to_dict(self):
        return {'id': self.id, 'filename': self.filename, 'comment': self.comment, 'upload_date': self.upload_date,
                'is_private': self.is_private, 'user_id': self.user_id,
                'username': self.user.login, 'download_link': f'http://{domain}/download?id={self.id}'}


#  Получения объекта файла по id
def get_file_class(file_id):
    session = create_session()
    file = session.query(Files).get(file_id)
    return file
