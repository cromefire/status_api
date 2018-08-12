import unittest
# noinspection PyProtectedMember
from importlib._bootstrap_external import SourceFileLoader
from os.path import dirname, join
from importlib.util import spec_from_file_location, module_from_spec
from time import sleep


class TestCase(unittest.TestCase):
    def import_wsgi(self):
        app_spec = spec_from_file_location(
            "status_api.app",
            loader=SourceFileLoader(
                "status_api.app",
                join(dirname(__file__), "../src/status_api/app.wsgi")
            )
        )
        app = module_from_spec(app_spec)
        app_spec.loader.exec_module(app)
        return app.application

    def test_wsgi_import(self):
        self.import_wsgi()

    def test_wsgi_call(self):
        app = self.import_wsgi()

        status = {"done": False}

        def start_response(*args):
            print("Got response")
            status["done"] = True

        app({
            "wsgi.url_scheme": "/notfound",
            "SERVER_NAME": "unittest",
            "SERVER_PORT": "8080",
            "REQUEST_METHOD": "GET"
        }, start_response)

        for i in range(60):
            sleep(1)
            if status["done"]:
                return

        self.fail("Server did not return a response (timeout)")


if __name__ == '__main__':
    unittest.main()
