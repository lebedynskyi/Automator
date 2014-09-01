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

from tools import http_utils

VK_API_HEADERS = {"Accept-Encoding": "utf-8",
                  "Accept": "json",
                  "User-Agent": "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy "
                                "Nexus Build/IMM76B) AppleWebKit/535.19 "
                                "(KHTML, like Gecko) Chrome/18.0.1025.133 "
                                "Mobile Safari/535.19"}


VK_API_URL = "https://api.vk.com/method/"
METHOD_COMMUNITY_SEARCH = "groups.search"


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
        return self._do_request(url_builder, handle_token, handle_captcha)

    def _do_request(self, url_builder, handle_token, handle_captcha):
        url_builder.add_arguments({"access_token": self.vk_user})
        http_response = http_utils.do_get(url_builder.build(), VK_API_HEADERS)
        print(http_response)