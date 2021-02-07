
from sqaapitest.src.helpers.products_helper import ProductHelper
from sqaapitest.src.dao.products_dao import Products_DAO
import pytest
from datetime import datetime, timedelta

@pytest.mark.regression
class TestListProductsWithFilter(object):

    @pytest.mark.tcid51
    def test_list_products_with_filter_after(self):
        # create data
        x_days_from_today = 30
        _after_created_date = datetime.now().replace(microsecond=0) - timedelta(days=x_days_from_today)
        after_created_date = _after_created_date.isoformat()

        #tmp_date = datetime.now() - timedelta(days=x_days_from_today)
        #after_created_date = tmp_date.strftime('%Y-%M-%dT%H:%m:%S')

        # make the call
        payload = dict()
        payload['after'] = after_created_date
        rs_api = ProductHelper().call_list_products(payload)
        assert rs_api, f"Empty response for 'list products with filter"

        # get data from db
        db_products = Products_DAO().get_products_created_after_given_date(after_created_date)

        # verify response
        assert len(rs_api) == len(db_products), f"List products with filter 'after' returned unexpected number of products." \
                                        f"Expected:  {len(db_products)}, Actual: {len(rs_api)}"
        ids_in_api = [i['id'] for i in rs_api]
        ids_in_db = [i['ID'] for i in db_products]

        ids_diff = list(set(ids_in_api) - set(ids_in_db))
        assert not ids_diff, f"List products with filter, Products ids in response mismatch in db."

