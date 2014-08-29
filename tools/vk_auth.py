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
import html.parser
import http.cookiejar
import urllib.request
import urllib.parse

AUTH_URL = "http://oauth.vk.com/oauth/authorize?" \
           "redirect_uri=http://oauth.vk.com/blank.html&" \
           "response_type=token&client_id=%s&scope=%s&display=wap"

LOG = logging.getLogger(__name__)


class Authenticator(object):
    def __init__(self, login, password, app_id, scope):
        self.app_id = app_id
        self.scope = scope
        self.login = login
        self.password = password

        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
            urllib.request.HTTPRedirectHandler())

    def do_auth(self):
        doc, url = self._auth_user()
        if urllib.parse.urlparse(url).path != "/blank.html":
            # Need to give access to requested scope
            url = self._give_access(doc, self.opener)
        if urllib.parse.urlparse(url).path != "/blank.html":
            raise RuntimeError("Expected success here")
        answer = dict(split_key_value(kv_pair) for kv_pair in
                      urllib.parse.urlparse(url).fragment.split("&"))
        if "access_token" not in answer or "user_id" not in answer:
            raise RuntimeError("Missing some values in answer")
        return answer["access_token"], answer["user_id"]

    def _auth_user(self):
        url = AUTH_URL % (self.app_id, self.scope)
        response = self.opener.open(url)
        doc = response.read().decode(encoding='UTF-8')
        parser = FormParser()
        parser.feed(doc)
        parser.close()

        if not parser.form_parsed \
                or parser.url is None \
                or "pass" not in parser.params \
                or "email" not in parser.params:
            raise RuntimeError("Something wrong")

        parser.params["email"] = self.login
        parser.params["pass"] = self.password
        if parser.method.upper() == "POST":
            request_data = urllib.parse.urlencode(parser.params).encode(
                "utf-8")
            response = self.opener.open(parser.url, request_data)
        else:
            raise NotImplementedError("Method '%s'" % parser.method)
        return response.read(), response.geturl()

    # Permission request form
    def _give_access(self, doc, opener):
        parser = FormParser()
        parser.feed(doc.decode(encoding='UTF-8'))
        parser.close()
        if not parser.form_parsed or parser.url is None:
            raise RuntimeError("Something wrong")
        if parser.method.upper() == "POST":
            request_data = urllib.parse.urlencode(parser.params).encode(
                "utf-8")
            response = opener.open(parser.url, request_data)
        else:
            raise NotImplementedError("Method '%s'" % parser.method)
        return response.geturl()


class FormParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = "GET"

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "form":
            if self.form_parsed:
                raise RuntimeError("Second form on page")
            if self.in_form:
                raise RuntimeError("Already in form")
            self.in_form = True
        if not self.in_form:
            return
        attrs = dict((name.lower(), value) for name, value in attrs)
        if tag == "form":
            self.url = attrs["action"]
            if "method" in attrs:
                self.method = attrs["method"]
        elif tag == "input" and "type" in attrs and "name" in attrs:
            if attrs["type"] in ["hidden", "text", "password"]:
                self.params[attrs["name"]] = attrs[
                    "value"] if "value" in attrs else ""

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "form":
            if not self.in_form:
                raise RuntimeError("Unexpected end of <form>")
            self.in_form = False
            self.form_parsed = True


def split_key_value(kv_pair):
    kv = kv_pair.split("=")
    return kv[0], kv[1]