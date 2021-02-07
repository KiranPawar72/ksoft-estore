

from sqaapitest.src.utilities.requestutility import RequestUtility
import logging as LOG

class ProductHelper(object):

    def __init__(self):
        self.requests_utility = RequestUtility()

    def get_product_by_id(self,product_id):
        return self.requests_utility.get(f"products/{product_id}")

    def call_create_product(self, payload):
        rs_api = self.requests_utility.post('products', payload=payload, expected_status_code=201)
        return rs_api

    def call_list_products(self, payload=None):
        max_pages = 1000
        all_products = []
        for i in range(1, max_pages + 1):
            LOG.debug(f"List products page number: {i}")

            if not 'per_page' in payload.keys():
                payload['per_page'] = 10

            # add the current page number to the call
            payload['page'] = i
            rs_api = self.requests_utility.get('products', payload=payload)

            # if there is no response in next page then stop loop
            if not rs_api:
                break
            else:
                all_products.extend(rs_api)
        else:
            raise Exception(f"Unable to find all products after {max_pages} pages")
        return all_products
