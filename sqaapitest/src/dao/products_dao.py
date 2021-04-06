
from sqaapitest.src.utilities.db_utility import DbUtility
import random

class Products_DAO(object):

    def __init__(self):
        self.db_helper = DbUtility()

    def get_random_product_from_db(self, qty=1):
        sql = 'SELECT * FROM local.wp_posts WHERE post_type = "product" LIMIT 5000;'
        rs_sql = self.db_helper.execute_select(sql)
        return random.sample(rs_sql, int(qty))

    def get_product_by_id(self, product_id):
        sql = f"SELECT * FROM local.wp_posts WHERE ID = {product_id};"
        return self.db_helper.execute_select(sql)

    def get_products_created_after_given_date(self, _date):
        sql = f'SELECT * FROM local.wp_posts WHERE post_type = "product" AND post_date > "{_date}" LIMIT 10000;'
        return self.db_helper.execute_select(sql)

    def get_random_products_that_are_not_on_sale(self, qty=1):
        sql = f'SELECT * FROM local.wp_posts WHERE post_type = "product" AND id NOT IN (SELECT post_id FROM local.wp_postmeta WHERE "meta_key" = "_sale_price");'
        rs_sql = self.db_helper.execute_select(sql)
        return random.sample(rs_sql, int(qty))

    def get_random_products_that_are_on_sale(self, qty=1):
        sql = f'SELECT * FROM local.wp_posts WHERE post_type = "product" AND id IN (SELECT post_id FROM local.wp_postmeta WHERE "meta_key" = "_sale_price");'
        rs_sql = self.db_helper.execute_select(sql)
        return random.sample(rs_sql, int(qty))
