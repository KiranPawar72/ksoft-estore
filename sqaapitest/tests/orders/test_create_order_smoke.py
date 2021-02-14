
from sqaapitest.src.dao.products_dao import Products_DAO
from sqaapitest.src.dao.orders_dao import OrdersDAO
from sqaapitest.src.helpers.orders_helper import OrdersHelper
import pytest

@pytest.mark.orders
@pytest.mark.smoke
@pytest.mark.tcid48
def test_create_paid_order_guest_user():
    product_dao = Products_DAO()
    order_helper = OrdersHelper()
    orders_dao = OrdersDAO()

    # get a product from db
    rand_product = product_dao.get_random_product_from_db(1)
    product_id = rand_product[0]['ID']

    # make the call
    info =  { "line_items": [
    {
      "product_id": product_id,
      "quantity": 1
    }
    ]}
    order_json = order_helper.create_order(additional_args=info)

    # verify response
    assert order_json, f"Create order response is empty."
    assert order_json['customer_id'] == 0, f"Create order as guest expected default customer_id=0" \
                    f"but got '{order_json['customer_id']}"
    assert len(order_json['line_items']) == 1, f"Expected only 1 item in order but " \
                    f"found '{len(order_json['line_items'])}'" \
                    f"Order id: {order_json['id']}."

    # verify db
    order_id = order_json['id']
    line_info = orders_dao.get_order_lines_by_order_id(order_id)
    assert line_info, f"Create order, line item not found in DB. Order id: {order_id}"

    line_items = [i for i in line_info if i['order_item_type'] == 'line_item']
    assert len(line_items), f"Expected 1 line item but found {len(line_items)}. Order id: {order_id}"

    line_id = line_items[0]['order_item_id']
    line_details = orders_dao.get_order_items_details(line_id)
    db_product_id = line_details['_product_id']
    assert str(db_product_id) == str(product_id), f"Create order 'product id' in db does not match in API." \
                        f"API product id: {product_id}, DB product id: {db_product_id}"


