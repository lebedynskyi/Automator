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

from unittest import TestCase

from tools.http_utils import UrlBuilder


class TestHttpBuilder(TestCase):
    def test_constructor_http(self):
        builder = UrlBuilder("http://google.com")
        self.assertEqual(builder.url_scheme, "http://")
        self.assertEqual(builder.base, "google.com")

    def test_constructor_https(self):
        builder = UrlBuilder("https://google.com")
        self.assertEqual(builder.url_scheme, "https://")
        self.assertEqual(builder.base, "google.com")

        builder = UrlBuilder("https://google.com/")
        self.assertEqual(builder.url_scheme, "https://")
        self.assertEqual(builder.base, "google.com")

    def test_append_path(self):
        builder = UrlBuilder("http://google.com")
        builder.append_path("test/path/test")
        self.assertEqual(builder.path_parts, ["test", "path", "test"])

        builder.append_path("/one/two/test/")
        self.assertEqual(builder.path_parts, ["test", "path", "test",
                                              "one", "two", "test"])

    def test_set_arguments(self):
        args = {"empty": None, "not_empty": "value", "int": 12, None: None}
        builder = UrlBuilder("http://google.com")
        builder.add_arguments(args=args)

        builder_arguments = builder.arguments
        self.assertIn("not_empty", builder_arguments)
        self.assertIn("int", builder_arguments)

        self.assertNotIn("empty", builder_arguments)
        self.assertNotIn(None, builder_arguments)

        self.assertEqual(builder_arguments["not_empty"], "value")
        self.assertEqual(builder_arguments["int"], 12)

    def test_set_scheme(self):
        builder = UrlBuilder("http://google.com")
        builder.scheme("http://")
        self.assertEqual(builder.url_scheme, "http://")

        builder.scheme("https://")
        self.assertEqual(builder.url_scheme, "https://")

        builder.scheme("file://")
        self.assertEqual(builder.url_scheme, "file://")

    def test_build_with_args(self):
        url = "http://google.com"
        args = {"key": "value", "key_int": 12, "empty": None}
        path = "/Some/test///Path//"

        builder = UrlBuilder(url)
        builder.add_arguments(args)
        builder.append_path(path)
        builder.scheme("https://")

        final_url = "https://google.com/Some/test/Path?key=value&key_int=12"
        final_url2 = "https://google.com/Some/test/Path?key_int=12&key=value"

        result = builder.build()

        try:
            self.assertEqual(result, final_url)
        except AssertionError:
            self.assertEqual(result, final_url2)

    def test_build_without_args(self):
        url = "http://google.com"
        path = "/Some/test///Path//"

        builder = UrlBuilder(url)
        builder.append_path(path)
        builder.scheme("https://")

        final_url = "https://google.com/Some/test/Path"
        self.assertEqual(builder.build(), final_url)

    def test_build_without_path(self):
        url = "http://google.com"
        args = {"key": "value", "key_int": 12, "empty": None}

        builder = UrlBuilder(url)
        builder.add_arguments(args)
        builder.scheme("https://")

        final_url = "https://google.com?key=value&key_int=12"
        final_url2 = "https://google.com?key_int=12&key=value"

        result = builder.build()
        try:
            self.assertEqual(result, final_url)
        except AssertionError:
            self.assertEqual(result, final_url2)

    def test_gen_path(self):
        url = "http://google.com"
        path = "//test/test//test//"
        builder = UrlBuilder(url)
        builder.append_path(path)
        builder.append_path("more/more2")
        expected_result = "test/test/test/more/more2"
        self.assertEqual(builder.gen_path(), expected_result)

    def test_gen_args(self):
        args = {"encoded": "normal", "not_encoded": "http://Hello"}
        url = "http://google.com"
        builder = UrlBuilder(url)
        builder.add_arguments(args)

        result_args = "encoded=normal&not_encoded=http%3A%2F%2FHello"
        result_args2 = "not_encoded=http%3A%2F%2FHello&encoded=normal"

        generated_args = builder.gen_args()
        try:
            self.assertEqual(generated_args, result_args)
        except AssertionError:
            self.assertEqual(generated_args, result_args2)