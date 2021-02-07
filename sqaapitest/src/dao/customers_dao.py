from sqaapitest.src.utilities.db_utility import DbUtility
import random

class CustomersDao(object):

    def __init__(self):
        self.db_helper = DbUtility()


    def get_customer_by_email(self, email):
        sql = f"SELECT * FROM local.wp_users WHERE user_email= '{email}';"
        rs_sql = self.db_helper.execute_select(sql)
        return rs_sql

    def get_all_customer_list(self):
        sql = f"SELECT * FROM local.wp_users;"
        rs_sql = self.db_helper.execute_select(sql)
        return rs_sql

    def  get_random_cust_from_db(self, qty=1):
        sql = f"SELECT * FROM local.wp_users ORDER BY id DESC LIMIT 5000;"
        rs_sql = self.db_helper.execute_select(sql)
        return random.sample(rs_sql, int(qty))