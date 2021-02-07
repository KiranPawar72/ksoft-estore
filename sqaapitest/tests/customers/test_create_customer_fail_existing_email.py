
import pytest
from sqaapitest.src.dao.customers_dao import CustomersDao
from sqaapitest.src.utilities.requestutility import RequestUtility

@pytest.mark.customers
@pytest.mark.tcid3
def test_create_cust_fail_existing_email():
    # Get existing customer email from db
    cust_dao = CustomersDao()
    existing_cust = cust_dao.get_random_cust_from_db()
    existing_cust_email = existing_cust[0]['user_email']

    # Call the api
    req_helper = RequestUtility()
    payload = {'email' : existing_cust_email, 'password' : 'password1'}
    cust_api_info = req_helper.post(endpoint='customers', payload=payload, expected_status_code=400)

    assert cust_api_info['code'] == 'registration-error-email-exists', f"Create customer with" \
        f"existing user error code is not correct. Expected: 'registration-error-email-exists' and" \
        f"Actual: {cust_api_info['code']}"

    assert cust_api_info['message'] == 'An account is already registered with your email address. <a href="#" class="showlogin">Please log in.</a>', \
        f"Create customer with existing user error message is not correct." \
        f"Expected: 'An account is already registered with your email address. <a href=\"#\" class=\"showlogin\">Please log in.</a>'"  \
        f"and Actual: {cust_api_info['message']}"

