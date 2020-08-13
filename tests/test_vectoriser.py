import json
import unittest
from flask import Flask, request, Response


class BasicTests(unittest.TestCase):

    # setup and teardown
    def setUp(self):

        # setting required environment variables

        global application, request_data
        from app.app import app
        self.application = app.test_client()

        with open("./tests/test_data/valid_request.json", 'r') as file:
            request_data = json.loads(file.read())

    # executed after each test
    def tearDown(self):
        pass

    # tests
    def test_invalid_headers(self):

        url = '/vectorise'
        headers = {}

        response = self.application.post(
            url, headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_invalid_request_01(self):

        url = '/vectorise'
        headers = {'content-type': 'application/json'}

        data = request_data.copy()
        del data[0]['image']

        response = self.application.post(
            url, headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(response.status_code, 402)

    def test_invalid_request_02(self):

        url = '/vectorise'
        headers = {'content-type': 'application/json'}

        data = request_data.copy()
        del data[0]['text']

        response = self.application.post(
            url, headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(response.status_code, 402)

    def test_invalid_request_03(self):

        url = '/vectorise'
        headers = {'content-type': 'application/json'}

        data = request_data.copy()
        data[0]['image'] = data[0]['image'][:-2]

        response = self.application.post(
            url, headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(response.status_code, 402)

    def test_invalid_request_04(self):

        url = '/vectorise'
        headers = {'content-type': 'application/json'}

        data = request_data.copy()
        data[0]['text'] = {"test": "value"}

        response = self.application.post(
            url, headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(response.status_code, 402)

    def test_valid_request_01(self):

        url = '/vectorise'
        headers = {'content-type': 'application/json'}

        data = request_data.copy()

        response = self.application.post(
            url, headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_request_02(self):

        url = '/vectorise'
        headers = {'content-type': 'application/json'}

        data = request_data.copy()
        data[0]['text'] = ""
        data[1]['image'] = ""

        response = self.application.post(
            url, headers=headers, data=json.dumps(data), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
