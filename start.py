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

import argparse
import logging
import logging.config

from app import core, stat
from app.core import ConfigHolder
from tools import check_utils
from tools import const


logging.basicConfig(level=logging.NOTSET)


def process_arguments():
    parser = argparse.ArgumentParser(description="Automator")
    parser.add_argument("-c", "--command", dest="command", required=True,
                        help="Determines what app should do."
                             "Should be one of %s, %s, %s" % (
                            const.AppType.RUN_FETCHER,
                            const.AppType.RUN_POSTER,
                            const.AppType.RUN_STAT))
    return parser.parse_args()


def process_command(context):
    app = None
    command = context.user_arguments.command
    if command == const.AppType.RUN_STAT:
        app = stat.Stat(context)
    if command == const.AppType.RUN_POSTER:
        pass
    if command == const.AppType.RUN_FETCHER:
        pass

    if app is None:
        raise ValueError("Unknown command %s" % command)
    else:
        app.do_work()


def do_start():
    check_utils.check_app_files()
    configurations = ConfigHolder(const.Global.CONFIGS_PATH)
    check_utils.check_config(configurations)

    logging.config.fileConfig(const.Global.LOGGER_PATH)

    user_arguments = process_arguments()
    context = core.Context(configurations, user_arguments)
    process_command(context)


if __name__ == "__main__":
    do_start()