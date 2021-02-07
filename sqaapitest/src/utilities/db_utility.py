import pymysql
from sqaapitest.src.utilities.credentialsutility import CredentialsUtility
import logging as LOG

class DbUtility(object):

    def __init__(self):
        cred_helper = CredentialsUtility()
        self.cred = cred_helper.get_db_credentials()
        self.host = 'localhost'
        self.socket = '/home/kiran/.config/Local/run/wkrjst3U9/mysql/mysqld.sock'

    def create_connection(self):
        connection = pymysql.connect(host=self.host, user=self.cred['db_user'],
                                     password=self.cred['db_password'],
                                     unix_socket=self.socket)

        return connection

    def execute_select(self, sql):
        conn = self.create_connection()
        try:
            LOG.debug(f"Executing : {sql}")
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchall()
            cur.close()
        except Exception as e:
            raise Exception(f"Failed running sql: {sql} \n Error: {str(e)}")
        finally:
            conn.close()
        return rs_dict