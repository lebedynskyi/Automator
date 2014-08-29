"""
Copyright 2014 Vitalii Lebedynskyi
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import contextlib

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from tools import const

orm_base = declarative_base()


class User(orm_base):
    __tablename__ = 'vk_users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(id='%s', login='%s', password='%s', name='%s')>" % (
            self.name, self.login, self.password, self.name)


class DBConnection(object):
    def __init__(self):
        self.engine = create_engine(const.Global.DB_CONNECTION_URL, echo=True)

        orm_base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @contextlib.contextmanager
    def query(self, model, *args, **kwargs):
        session = kwargs.get('session') or self.Session()
        try:
            yield session.query(model, *args)
        finally:
            session.commit()
            session.close()