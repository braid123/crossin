import mysql.connector
from .. import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnx.cursor(buffered=True)

class Sql:

    @classmethod
    def insert_sina_comment(cls, id, post_id, comment, refer, like_counts):
        sql = 'INSERT INTO sinacomment (`id`, `post_id`, `comment`, `refer`,`like_counts`)' \
              ' VALUES (%(id)s, %(post_id)s, %(comment)s, %(refer)s,%(like_counts)s)'
        value = {
            'id': id,
            'post_id': post_id,
            'comment': comment,
            'refer': refer,
            'like_counts': like_counts
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_id(cls, id):
        sql = "SELECT EXISTS(SELECT 1 FROM sinacomment WHERE id=%(id)s)"
        value = {
            'id': id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]