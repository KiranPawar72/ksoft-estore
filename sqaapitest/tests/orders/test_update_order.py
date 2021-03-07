

from sqaapitest.src.helpers.orders_helper import OrdersHelper
from sqaapitest.src.utilities.wooAPIUtility import WooAPIUtility
from sqaapitest.src.utilities.genericutilities import generate_random_string
import pytest

pytestmark = [pytest.mark.orders, pytest.mark.regression]

# Parametrization
@pytest.mark.parametrize("new_status",
                         [
                            pytest.param('cancelled', marks=pytest.mark.tcid55),
                            pytest.param('completed', marks=pytest.mark.tcid56),
                            pytest.param('on-hold', marks=pytest.mark.tcid57)
                         ])
def test_update_order_status(new_status):

    # create new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    cur_status = order_json['status']
    assert cur_status != new_status, f"Current status of the order is already  {new_status}." \
                                     f"Unable to run test."

    # update the status
    order_id = order_json['id']
    payload = {'status': new_status}
    rs_update = order_helper.call_update_an_order(order_id, payload)

    # get order information
    new_order_info = order_helper.call_retrieve_an_order(order_id)

    # verify the new order status is what was updated
    assert new_order_info['status'] == new_status, f"Updated order status to '{new_status}', " \
                            f"but order is still '{new_order_info['status']}'"

@pytest.mark.tcid58
def test_update_order_status_to_random_string():

    new_status = 'abcdef'
    # create new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    cur_status = order_json['status']
    assert cur_status != new_status, f"Current status of the order is already  {new_status}." \
                                     f"Unable to run test."

    # update the status
    order_id = order_json['id']
    payload = {'status': new_status}
    rs_api = WooAPIUtility().put(f"orders/{order_id}", params=payload, expected_status_code=400)

    assert rs_api['code'] == 'rest_invalid_param', f"Updated order staatus to random string did not have" \
                            f"correct code in response. Expected: 'rest_invalid_param' Actual: {rs_api['code']}"
    assert rs_api['message'] == 'Invalid parameter(s): status', f"Update order status to random" \
                f"string did not have correct message in response. Expected: 'Invalid parameter(s): status' " \
                f"Actual: {rs_api['message']}"


@pytest.mark.tcid59
def test_update_order_customer_note():

    # create a order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    order_id = order_json['id']

    # update the status
    rand_string = generate_random_string(40)
    payload = {'customer_note': rand_string}
    rs_update = order_helper.call_update_an_order(order_id, payload)

    # get order information
    new_order_info = order_helper.call_retrieve_an_order(order_id)
    assert new_order_info['customer_note'] == rand_string, f"Update order's 'customer note' field" \
                            f"failed. Expected: {rand_string}, Actual: {new_order_info['customer_note']}"

