
from sqaapitest.src.utilities.requestutility import RequestUtility
from sqaapitest.src.dao.products_dao import Products_DAO
from sqaapitest.src.helpers.products_helper import ProductHelper
import pytest

pytestmark = [pytest.mark.products]

@pytest.mark.tcid24
def test_list_all_products():
    # Make a call
    req_helper = RequestUtility()
    rs_api = req_helper.get(endpoint='products')
    assert rs_api, f"List all products endpoint returned nothing."


@pytest.mark.tcid25
def test_get_product_by_id():

    # Get product from db
    rand_product = Products_DAO().get_random_product_from_db(1)
    rand_product_id = rand_product[0]['ID']
    db_name = rand_product[0]['post_title']

    # Make a call
    product_helper = ProductHelper()
    rs_api  = product_helper.get_product_by_id(rand_product_id)
    api_name = rs_api['name']

    # Verify response
    assert db_name == api_name, f"Get product by id returned wrong product. Id: {rand_product_id}" \
                                f"Db_name: {db_name},Api_name: {api_name}"


















































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































