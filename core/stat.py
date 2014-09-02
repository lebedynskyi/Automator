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

from core.core import CoreApp
from tools import console
from tools import vk_api

LOG = logging.getLogger(__name__)


class Stat(CoreApp):
    def start(self):
        super().start()

        try:
            self.do_work()
        except KeyboardInterrupt:
            LOG.info("Stat module is finished.")

    def do_work(self):
        while 1:
            user_input = console.read_input(
                'Enter of public name (q for exit): ').strip()
            if user_input.lower() == 'q':
                raise KeyboardInterrupt()

            if len(user_input) == 0:
                print("Wrong query, try again")
                continue

            try:
                vk_request = vk_api.ApiRequest(self.context, self.vk_user)
                info = vk_request.do_request(vk_api.METHOD_COMMUNITY_SEARCH,
                                             True, True, q=user_input,
                                             type="group",
                                             fields="members_count")
                self.print_info(info)
            except BaseException as e:
                print("Error is happened")
                LOG.exception(e)

    def print_info(self, info):
        print(info)