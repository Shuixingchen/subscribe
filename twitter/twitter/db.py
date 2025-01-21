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
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True  # 启用自动提交
        )
        self.cursor = self.conn.cursor()
    def get_user_id(self):
        try:
            query_user_id = """
            SELECT id from t_users where status = 1
            """
            self.cursor.execute(query_user_id,())
            user_id = self.cursor.fetchone()
            return user_id['id']
        except Exception as e:
            print("Error: ", e)
    def get_big_user(self):
        try:
            query_big_post = """
            SELECT username from t_big_users where status = 1
            """
            self.cursor.execute(query_big_post,())
            big_users = self.cursor.fetchall()
            return big_users
        except Exception as e:
            print("Error: ", e)
    def save_big_user_post(self,data):
        try:
            insert_log_sql = """
            INSERT INTO t_big_user_post (username, social,post_id,post_time) VALUES (%s,%s,%s,%s)
            """
            self.cursor.execute(insert_log_sql,(data['username'],data['social'],data['post_id'],data['post_time']))
            return True
        except Exception as e:
            print("Error: ", e)
            return False