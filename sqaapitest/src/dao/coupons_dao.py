
from sqaapitest.src.utilities.db_utility import DbUtility

class Coupons_DAO(object):

    def __init__(self):
        self.db_helper = DbUtility()

    def get_coupon_by_id(self, coupon_id):
        sql = f"SELECT * FROM local.wp_posts WHERE ID = {coupon_id};"
        return self.db_helper.execute_select(sql)