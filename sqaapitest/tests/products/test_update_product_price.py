
from sqaapitest.src.helpers.products_helper import ProductHelper
from sqaapitest.src.dao.products_dao import Products_DAO
import pytest
import random

@pytest.mark.tcid61
def test_update_product_regular_price_should_update_price():
    """
    Verifies updating the 'regular_price' field should automatically update the 'price' field.
    """
    # create helper objects and get random product fromm db
    product_helper = ProductHelper()
    product_dao = Products_DAO()

    # for this test the 'sale_price' of the product must be empty. If product has sale_price, updating the 'regular_price'
    # does not update the 'price'. So get a bunch of products and loop until you find one  that is not on saale.
    # If the list are on sale then take random one and update the sale price
    rand_products = product_dao.get_random_product_from_db(3)
    for product in rand_products:
        product_id = product['ID']
        product_data = product_helper.call_retrieve_product(product_id)
        if product_data['on_sale']:
            continue
        else:
            break
    else:
        # take a random product and make it not on sale by setting sale_price=''
        test_product = random.choice(rand_products)
        product_id = test_product['ID']
        product_helper.call_update_a_product(product_id, {'sale_price': ''})

    # Make the update to 'regular_price'
    new_price = str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))
    payload = dict()
    payload['regular_price'] = new_price
    rs_update = product_helper.call_update_a_product(product_id, payload=payload)

    # verify the response has the 'price' and 'regular_price' has updated and 'sale_price' is not updated
    assert rs_update['price'] == new_price, f"Update product api call response. Updating the 'regular_price' did not" \
                                            f"update the 'price' field. price field actual value{rs_update['price']}," \
                                            f"but expected: {new_price}"

    assert rs_update['regular_price'] == new_price, f"Update product api call response. Updating the 'regular_price' did not" \
                                                    f"update in the response. Actual response 'regular_price': {rs_update['regular_price']}," \
                                                    f"but expected: {new_price}"

    # get the product after the update and verify response
    rs_product = product_helper.call_retrieve_product(product_id)
    assert rs_update['price'] == new_price, f"Update product api call response. Updating the 'regular_price' did not" \
                                            f"update the 'price' field. price field actual value{rs_update['price']}," \
                                            f"but expected: {new_price}"

    assert rs_update['regular_price'] == new_price, f"Update product api call response. Updating the 'regular_price' did not" \
                                              f"update in the response. Actual response 'regular_price': {rs_update['regular_price']}," \
                                              f"but expected: {new_price}"

@pytest.mark.tcid63
@pytest.mark.tcid64
def test_update_product_sale_price_should_update_on_sale():
    """
    Two test case.
    First case update the 'sale_price > 0' and verify the field changes to 'on_sale=True'.
    Second case update the 'sale_price=""' and verify the field changes to 'on_sale=False'.
    """

    # create helper object
    product_helper = ProductHelper()

    # create product for the tests and verify the product has on_sale=False
    regular_price = str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))
    payload = dict()
    payload['name'] = 'Kiran_72'
    payload['type'] = "simple"
    payload['regular_price'] = regular_price
    product_info = product_helper.call_create_product(payload)
    product_id = product_info['id']
    assert not product_info['on_sale'], f"Newly created product should not have 'on_sale=True', Product_id:{product_id}"
    assert not product_info['sale_price'], f"Newly created product should not have value for 'sale_price' filed."

    # tcid-63 now update the 'sale_price' and verify the 'on_sale' is set to True
    sale_price = str(float(regular_price) * .72)
    rs_updated = product_helper.call_update_a_product(product_id, {'sale_price': str(sale_price)})
    assert rs_updated['sale_price'] == sale_price, f"Response sale_price of product not updated, Actual sale_price: {rs_updated['sale_price']}" \
                                                   f" Expected sale_price: {sale_price}"
    product_after_update = product_helper.call_retrieve_product(product_id)
    assert product_after_update['on_sale'], f"Updated 'sale_price' of product, but the 'on_sale' did not set to 'True'." \
                                            f"Product id : {product_id}"

    # tcid-64 now update the sale_price to empty string and  verify the 'on_sale' is set to False
    rs_updated = product_helper.call_update_a_product(product_id, {'sale_price' : ''})
    assert rs_updated['sale_price'] == '', f"Response 'sale_price' of product Actual sale_price: {rs_updated['sale_price']}" \
                                            f" Expected sale_price: ''"
    assert rs_updated['on_sale'] == False, f"Response 'on_sale' of product Actual on_sale: {rs_updated['on_sale']}" \
                                    f" Expected on_sale: False"
    product_after_update = product_helper.call_retrieve_product(product_id)
    assert not product_after_update['on_sale'], f"Updated 'sale_price=""' of product, but the 'on_sale' did not set to 'False'." \
                                                f"Product id: {product_id}"

@pytest.mark.tcid65
def test_update_product_sale_price():
    """
    Verify that sale_price of product gets updated
    """
    # get a product from db that is not on sale
    product_helper = ProductHelper()
    product_dao = Products_DAO()
    rand_product = product_dao.get_random_products_that_are_not_on_sale(1)
    product_id = rand_product[0]['ID']

    # first check 'on_sale' status is False to start with
    product_info = product_helper.call_retrieve_product(product_id)
    assert not product_info['on_sale'], f"Getting test data with 'on_sale=False' but got 'True'. Unable to use this product for test."

    # update the sale_price of the product and verify response
    sale_price = float(product_info['regular_price']) * 0.72 # sale is 72% of original
    payload = dict()
    payload['sale_price'] = str(sale_price)
    rs_update = product_helper.call_update_a_product(product_id, payload=payload)
    assert rs_update['sale_price'] == str(sale_price), f"sale_price is not updated in response." \
                                                  f"Product id: {product_id}, Actual sale_price:{rs_update['sale_price']}," \
                                                  f"Expected sale_price: {sale_price}."

    # verify product sale_price field updated
    after_update = product_helper.call_retrieve_product(product_id)
    assert after_update['sale_price'] == str(sale_price), f"Product 'sale_price' value did not update." \
                                                          f"Product id: {product_id}, Actual sale_price:{after_update['sale_price']}, Expected sale_price:{sale_price}"
