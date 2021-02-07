
import pytest
from sqaapitest.src.utilities.requestutility import RequestUtility
import logging as LOG
from sqaapitest.src.dao.customers_dao import CustomersDao

@pytest.mark.customers
@pytest.mark.tcid2
def test_get_all_customers():
    req_helper = RequestUtility()
    rs_api = req_helper.get('customers')
    assert rs_api, f"Customer list is empty"

    # Get customer info in database
    cust_dao = CustomersDao()
    cust_dao_info = cust_dao.get_all_customer_list()

    # Verify number of customers in api response with database
    assert len(rs_api)+1 == len(cust_dao_info), f"Number of customers in api response: {len(rs_api)+1} " \
                                                f"and in database: {len(cust_dao_info)} are not equal "
