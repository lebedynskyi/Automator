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

import urllib.parse


class UrlBuilder(object):
    def __init__(self, base_url):
        self.path_parts = []
        self.arguments = dict()

        if base_url.startswith("http://"):
            self.url_scheme = "http://"
            self.base = base_url.replace("http://", "")
        elif base_url.startswith("https://"):
            self.url_scheme = "https://"
            self.base = base_url.replace("https://", "")
        else:
            self.url_scheme = "http://"
            self.base = base_url

        if self.base.endswith("/"):
            self.base = self.base[:-1]

    def scheme(self, url_schem):
        self.url_scheme = url_schem

    def append_path(self, path):
        parts = [v for v in path.split("/") if v]
        self.path_parts.extend(parts)

    def add_arguments(self, args):
        arguments = {k: v for k, v in args.items() if k and v}
        self.arguments.update(arguments)

    def build(self):
        url_pattern = ""
        if self.url_scheme:
            url_pattern += "{scheme}"
        if self.base:
            url_pattern += "{base}"
        if self.path_parts:
            url_pattern += "/{path}"
        if self.arguments:
            url_pattern += "?{args}"
        return url_pattern.format(scheme=self.url_scheme,
                                  base=self.base,
                                  path=self.gen_path(),
                                  args=self.gen_args())

    def gen_path(self):
        return "/".join(self.path_parts)

    def gen_args(self):
        return urllib.parse.urlencode(self.arguments)
