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

import configparser
import glob
import logging
import os

from core import db
from sqlalchemy.orm.exc import NoResultFound
from tools import vk_auth

LOG = logging.getLogger(__name__)


class Context(object):
    def __init__(self, config, user_arguments):
        self.user_arguments = user_arguments
        self.config = config


class ConfigHolder(object):
    def __init__(self, file):
        self.is_prepared = False
        self.all_configs = {}
        self.cached_configs = {}
        self.parser = configparser.ConfigParser()

        if file:
            if os.path.isdir(file):
                self.eat_folder(file)
            else:
                self.read_file_from_path(file)

    def eat_folder(self, path):
        for f in glob.glob(os.path.join(path, "*.ini")):
            self.read_file_from_path(f)

    def read_file_from_path(self, f):
        if os.path.exists(f):
            LOG.debug("Reading configs from %s" % f)
            self.parser.read(f)
        else:
            raise FileNotFoundError(f)

    def get_value(self, key, converter=str, default=None):
        """Returns required value, wrapped by converter.

        Method takes value from files and converts it to type provided
        by converter.

        :param converter: build in function, eg int, str, bool
        :param key: name of stored config
        :returns: value associated with specified key

        """

        if not self.is_prepared:
            self._prepare_configs()

        cached_key = (key, converter)
        if cached_key in self.cached_configs:
            return self.cached_configs[cached_key]

        try:
            str_value = self.all_configs[key]
            converted_value = converter(str_value)
            self.cached_configs[cached_key] = converted_value
            return converted_value if converted_value else default
        except:
            LOG.info("cannot read config %s, default = %s" % (key, default))
            return default

    def _prepare_configs(self):
        """Method extracts values from files to memory.

        This method do preparing with holder - extracts all key-values pairs
        from files with configs.

        """
        for section in self.parser.sections():
            for key, value in self.parser.items(section):
                self.all_configs[key] = value

        self.is_prepared = True


class CoreApp(object):
    def __init__(self, context):
        self.context = context
        self.db_connection = db.DBConnection()
        user_login = self.context.config.get_value("user_login", str)
        self.vk_user = self.check_user_in_db(user_login)
        if not self.vk_user:
            LOG.info("There is no users login DB with id %s" % user_login)
            self.refresh_user()

    def refresh_user(self):
        self.vk_user = self.fetch_new_user()


    def fetch_new_user(self):
        LOG.info("Fetching user ")
        login = self.context.config.get_value("user_login")
        password = self.context.config.get_value("user_pass")

        app_id = self.context.config.get_value("app_id")
        auth_scope = self.context.config.get_value("auth_scope")

        auth = vk_auth.Authenticator(login, password, app_id, auth_scope)
        token, user_id = auth.do_auth()
        LOG.info("Successfully authorized user\n\t"
                 "user_login=%s\n\t"
                 "user_id=%s\n\t"
                 "access_token=%s" % (login, user_id, token))
        return db.User(id=user_id, login=login, password=password,
                       last_token=token)

    def start(self):
        LOG.info(
            "Running with command -> %s" % self.context.user_arguments.command)

    def check_user_in_db(self, user_login):
        with self.db_connection.open_session() as sess:
            try:
                query = sess.query(db.User)
                return query.filter_by(login=user_login).one()
            except NoResultFound:
                return None
