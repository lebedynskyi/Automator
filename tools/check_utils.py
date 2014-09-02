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

import logging
import os

from tools import const
from tools.file_utils import copyfile

LOG = logging.getLogger(__name__)

REQUIRED_CONFIGS = ("user_login",
                    "user_pass",
                    "auth_scope",
                    "app_id")


def check_app_files():
    LOG.info("Checking app folder")
    if not os.path.exists(const.Global.DATA_PATH):
        app_data_path = const.Global.DATA_PATH
        LOG.debug("Creating folder %s" % app_data_path)

        os.makedirs(app_data_path)

    if not os.path.exists(const.Global.CONFIGS_PATH):
        local_config = os.path.join("files", const.Global.CONFIG_NAME)
        dist_config = const.Global.CONFIGS_PATH
        LOG.debug("Copying file from %s to %s" % (local_config, dist_config))

        copyfile(local_config, dist_config)

    if not os.path.exists(const.Global.LOGGER_PATH):
        local_app_logger = os.path.join("files", const.Global.LOGGER_NAME)
        dist_app_logger = const.Global.LOGGER_PATH
        LOG.debug("Copying file from %s to %s" % (local_app_logger,
                                                  dist_app_logger))

        copyfile(local_app_logger, dist_app_logger)


def check_config(config):
    for key in REQUIRED_CONFIGS:
        if not config.get_value(key):
            raise LookupError("Missing config %s" % key)