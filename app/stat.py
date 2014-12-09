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

from prettytable import PrettyTable

from app.core import CoreApp
from tools import vk_api


LOG = logging.getLogger()


def print_info(resp):
    table = PrettyTable(["Members", "Name", "url"])
    table.align["Members"] = "l"
    table.align["Name"] = "l"
    table.align["url"] = "l"
    print("%s pages were found" % len(resp))
    for group in resp:
        count = group["members_count"] if "members_count" in group else 0
        name = group["name"][:50]
        url = group["screen_name"]
        table.add_row([count, name, url])

    print(table)


class Stat(CoreApp):
    def __init__(self, context):
        super().__init__(context)
        self.vk_api = None

    def do_work(self):
        self.vk_user = self.get_user_from_db()

        if not self.vk_user:
            self.vk_user = self.fetch_new_user()
            self.save_user(self.vk_user)

        self.vk_api = vk_api.ApiRequest(self.context, self.vk_user)

        try:
            self.manage_stat()
        except KeyboardInterrupt:
            LOG.info("Stat module is finished.")

    def manage_stat(self):
        while 1:
            query = input('Enter a name of public (q for exit): ').strip()
            if query.lower() == 'q':
                raise KeyboardInterrupt()

            if len(query) == 0:
                print("Wrong query, try again")
                continue

            try:
                resp = self.vk_api.do_request("execute.searchGroups", q=query)

                if not resp:
                    print("Nothing to show")
                    continue

                resp = sorted(resp, key=lambda k: k['members_count'])

                try:
                    print_info(resp)
                except:
                    LOG.warning("Cannot print table. Response:")
                    print(resp)
            except BaseException as e:
                print("Error is happened")
                LOG.exception(e)