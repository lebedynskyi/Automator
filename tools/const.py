"""
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
import os


class Global(object):
    NAME = ".vk_automator"
    DATA_PATH = os.path.join(os.path.expanduser("~/"), NAME)

    DB_NAME = "automator"
    DB_CONNECTION_URL = "sqlite:///%s:" % os.path.join(DATA_PATH,
                                                           DB_NAME)

    CONFIG_NAME = "configs.ini"
    CONFIGS_PATH = os.path.join(DATA_PATH, CONFIG_NAME)

    LOGGER_NAME = "logger.ini"
    LOGGER_PATH = os.path.join(DATA_PATH, LOGGER_NAME)


class AppType(object):
    RUN_FETCHER = "fetcher"
    RUN_STAT = "stat"
    RUN_POSTER = "poster"