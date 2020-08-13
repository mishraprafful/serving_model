import unittest
from flask import Flask, request, Response


class BasicTests(unittest.TestCase):

    # setup and teardown
    def setUp(self):

        # setting required environment variables

        global application
        from application import app
        self.application = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    # tests
    def test_service_up(self):

        url = '/'

        response = self.application.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
