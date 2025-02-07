import pymysql
from dotenv import load_dotenv
import os
import hashlib
import logging
import traceback
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
            x_uid = os.getenv("X_USER_ID")
            if x_uid is not None:
                return int(x_uid)
            query_user_id = """
            SELECT id from t_users where status = 1
            """
            self.cursor.execute(query_user_id,())
            user_id = self.cursor.fetchone()
            return user_id['id']
        except Exception as e:
            print("Error: ", e)

    def get_user(self):
        try:
            x_uid = os.getenv("X_USER_ID")
            params = ()
            if x_uid is not None:
                query_user = """
                SELECT * from t_users where id = %s
                """
                params = (x_uid,)
            else:
                query_user = """
                SELECT * from t_users where status = 1
                """
            self.cursor.execute(query_user,params)
            user = self.cursor.fetchone()
            return user
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
            article = data['article']
            if len(article) == 0:
                print("article invalid: ", article)
                return False
            if 'minutes' not in data['post_time'] and 'seconds' not in data['post_time']:
                print("time invalid: ", data['post_time'])
                return False
            hash_object = hashlib.md5()
            hash_object.update(article.encode('utf-8'))
            post_hash = hash_object.hexdigest()
            print("post_hash: ", post_hash)
            insert_log_sql = """
            INSERT INTO t_big_user_post (username, social,post_id,post_time,post_hash) VALUES (%s,%s,%s,%s,%s)
            """
            self.cursor.execute(insert_log_sql,(data['username'],data['social'],data['post_id'],data['post_time'],post_hash))
            return True
        except Exception as e:
            print("Error: ", e)
            return False

    def save_reply_log(self, data):
        try:
            insert_log_sql = """
            INSERT INTO t_reply_log (uid, content_id,origin_post_url) VALUES (%s, %s,%s)
            """
            self.cursor.execute(insert_log_sql, (data['user_id'], data['content_id'], data['origin_post_url']))
            self.conn.commit()
        except:
            logging.error("save_reply_log",traceback.format_exc())
    def get_reply_list(self):
        try:
            
            query_big_user = """
            SELECT * from t_big_users where status = 1 and id not in (SELECT uid from t_reply_log where date(created_at)=curdate()) limit 3
            """
            query_reply_content = """
            SELECT * from t_reply_content order by id desc limit 1
            """
            self.cursor.execute(query_big_user)
            users = self.cursor.fetchall()
            self.cursor.execute(query_reply_content)
            content = self.cursor.fetchone()
            reply_list = []
            for user in users:
                reply_list.append({
                    "user_id": user['id'],
                    "user_name": user['username'],
                    "content": content['content'],
                    "content_id": content['id']
                })
            return reply_list
        except:
            logging.error("get_reply_list",traceback.format_exc())