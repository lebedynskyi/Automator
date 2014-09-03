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

import json
import logging

from tools import http_utils

VK_API_HEADERS = {"Accept-Encoding": "utf-8",
                  "Accept": "json",
                  "User-Agent": "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy "
                                "Nexus Build/IMM76B) AppleWebKit/535.19 "
                                "(KHTML, like Gecko) Chrome/18.0.1025.133 "
                                "Mobile Safari/535.19",
                  "Content-Type": "application/x-www-form-urlencoded"}


VK_API_URL = "https://api.vk.com/method/"
VK_API_VERSION = "5.24"

UNKNOWN_ERROR = 0
CAPTCHA_ERROR = 1
TOKEN_ERROR = 2

LOG = logging.getLogger(__name__)


class CaptchaRequiredException(BaseException):
    pass


class TokenExpiredException(BaseException):
    pass


class ApiRequest(object):
    def __init__(self, context, vk_user):
        self.context = context
        self.vk_user = vk_user

    def do_request(self, m, handle_token=True, handle_captcha=True, **args):
        url_builder = http_utils.UrlBuilder(VK_API_URL)
        url_builder.append_path(m)
        url_builder.add_arguments(args)
        url_builder.add_arguments({"access_token": self.vk_user.last_token,
                                   "v": VK_API_VERSION})
        return self._do_request(url_builder.build(), handle_token,
                                handle_captcha)

    def _do_request(self, url, handle_token, handle_captcha):
        LOG.debug("Request api, url - %s" % url)
        bytes_answer = http_utils.do_get(url, VK_API_HEADERS)
        string_answer = bytes_answer.decode(encoding='UTF-8')
        obj = json.loads(string_answer)
        if "response" in obj:
            return obj["response"]

        error = self._get_error(obj)
        if error == UNKNOWN_ERROR:
            LOG.warning("Api request error %s" % obj)

    def _get_error(self, obj):
        return UNKNOWN_ERROR


def community_search():
    pass
