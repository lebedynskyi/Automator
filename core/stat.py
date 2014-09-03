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
            query = console.read_input(
                'Enter of public name (q for exit): ').strip()
            if query.lower() == 'q':
                raise KeyboardInterrupt()

            if len(query) == 0:
                print("Wrong query, try again")
                continue

            try:
                vk_request = vk_api.ApiRequest(self.context, self.vk_user)
                resp = vk_request.do_request("execute.searchGroups", q=query)

                if not resp:
                    print("Nothing to show")
                    continue

                try:
                    self.print_info(resp)
                except:
                    LOG.warning("Cannot print table")
                    print(resp)
            except BaseException as e:
                print("Error is happened")
                LOG.exception(e)

    def print_info(self, resp):
        table = PrettyTable(["Members", "Name", "url"])
        table.align["Members"] = "l"
        table.align["Name"] = "l"
        table.align["url"] = "l"
        print("%s groups was found" % len(resp))
        for group in resp:
            count = group["members_count"] if "members_count" in group else 0
            name = group["name"][:50]
            url = group["screen_name"]
            table.add_row([count, name, url])

        print(table)