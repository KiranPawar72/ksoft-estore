from sqaapitest.src.configs.hosts_config import API_HOST
from sqaapitest.src.utilities.credentialsutility import CredentialsUtility
import requests
import json
import os
from requests_oauthlib import OAuth1
import logging as LOG

class RequestUtility(object):

    def __init__(self):
        wc_crede = CredentialsUtility.get_wc_api_keys()
        self.env = os.environ.get('ENV', 'test')
        self.baseurl = API_HOST[self.env]

        self.auth = OAuth1(wc_crede['wc_key'], wc_crede['wc_secret'])

    def assert_status_code(self):
        assert self.status_code == self.expected_status_code, f"Bad status code" \
        f"Expected: {self.expected_status_code}, Actual status code: {self.status_code}" \
        f"URL: {self.url}, Response: {self.rs_json}"

    def post(self, endpoint, payload=None, headers=None, expected_status_code=200):
        self.url = self.baseurl + endpoint
        if not headers:
            headers = {"Content-type" : "application/json"}
        rs_api = requests.post(url=self.url, data=json.dumps(payload), headers=headers, auth=self.auth)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()
        LOG.debug(f"POST API response : {self.rs_json}")
        return self.rs_json

    def get(self, endpoint, payload=None, headers=None, expected_status_code=200):
        self.url = self.baseurl + endpoint
        if not headers:
            headers = {"Content-type": "application/json"}
        rs_api = requests.get(url=self.url, data=json.dumps(payload), headers=headers, auth=self.auth)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()
        LOG.debug(f"GET API response : {self.rs_json}")
        return self.rs_json