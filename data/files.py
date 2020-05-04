import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase, create_session


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
        session.query(Files).filter(Files.id == int(self.id)). \
            update({Files.id: self.downloaded}, synchronize_session=False)
        session.commit()