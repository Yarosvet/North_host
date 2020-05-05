import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase, create_session
from config import domain


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
    downloaded = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user = orm.relation('User')

    def increment_download(self):
        self.downloaded += 1
        session = create_session()
        session.query(Files).filter(Files.id == self.id). \
            update({Files.downloaded: self.downloaded}, synchronize_session=False)
        session.commit()

    def to_dict(self):
        return {'id': self.id, 'filename': self.filename, 'comment': self.comment, 'upload_date': self.upload_date,
                'is_private': self.is_private, 'user_id': self.user_id, 'downloaded': self.downloaded,
                'username': self.user.login, 'download_link': f'http://{domain}/download?id={self.id}'}


def get_file_class(file_id):
    session = create_session()
    file = session.query(Files).get(file_id)
    return file
