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

VK_API_URL = "https://api.vk.com/method/"


class CaptchaRequiredException(BaseException):
    pass


class TokenExpiredException(BaseException):
    pass


class ApiRequest(object):
    def __init__(self, context, method, token_expired=True,
                 captcha_required=True, **kwargs):
        self.method = method
        self.handle_token_expired = token_expired
        self.handle_captcha_required = captcha_required
        self.arguments = kwargs
