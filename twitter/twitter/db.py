import pymysql
from dotenv import load_dotenv
import os
load_dotenv()

class Db:
    def __init__(self):
        host = os.getenv("MYSQL_HOST")
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')
        database = os.getenv('MYSQL_DATABASE')
        port = os.getenv('MYSQL_PORT')

        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=int(port),
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()
    def get_user_id(self):
        try:
            query_user_id = """
            SELECT id from t_users where status = 1
            """
            self.cursor.execute(query_user_id,())
            user_id = self.cursor.fetchone()
            # return user_id['id']
            return 4
        except Exception as e:
            print("Error: ", e)