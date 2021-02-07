
from sqaapitest.src.utilities.genericutilities import generate_random_email_and_password
from sqaapitest.src.utilities.requestutility import RequestUtility
class CustomerHelper(object):

    def __init__(self):
        self.request_utility = RequestUtility()

    def create_customer(self, email=None, password=None, **kwargs):

        if not email:
            ep = generate_random_email_and_password()
            email = ep['email']
        if not password:
            password = 'Password1'

        payload = dict()
        payload['email'] = email
        payload['password'] = password
        payload.update(kwargs)

        create_cust_json = self.request_utility.post('customers', payload=payload, expected_status_code=201)
        return create_cust_json