
import pytest
import logging as LOG
from sqaapitest.src.utilities.genericutilities import generate_random_email_and_password
from sqaapitest.src.helpers.customers_helper import CustomerHelper
from sqaapitest.src.dao.customers_dao import CustomersDao

@pytest.mark.customers
@pytest.mark.tcid1
def test_create_customer_only_email_password():
    # Create random name and email
    LOG.info("TEST: Create new customer with email and password only.")
    random_info = generate_random_email_and_password()
    email = random_info['email']
    password = random_info['password']

    # Create payload
    payload = {'email' : email, 'password' : password}

    # Make the call
    cust_obj = CustomerHelper()
    cust_api_info = cust_obj.create_customer(email=email, password=password)

    # Verify email and first name in the api response
    assert cust_api_info['email'] == email, f"Create customer api return wrong api. Email: {email}"
    assert cust_api_info['first_name'] == '', f"Create customer api returned value for first_name " \
                                             f"but it must be empty"

    # Verify customer is created in database
    cust_dao = CustomersDao()
    cust_dao_info = cust_dao.get_customer_by_email(email)

    # Verify customer api versus  db response
    id_in_api = cust_api_info['id']
    id_in_db = cust_dao_info[0]['ID']
    assert id_in_api == id_in_db, f"Create customer response 'id' is not same as 'ID' in database" \
                                 f"email: {email}"
