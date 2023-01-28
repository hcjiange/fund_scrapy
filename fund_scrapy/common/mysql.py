import pymysql


class Mysql(object):
    config = None
    conn = None
    cursor = None

    def __init__(self, config):
        config["cursorclass"] = pymysql.cursors.DictCursor
        self.config = config
        self.connect()

    def __del__(self):
        self.close()

    def connect(self):
        self.conn = pymysql.connect(**self.config)
        self.cursor = self.conn.cursor()
        print("database is linking...")

    def close(self):
        self.cursor.close()
        self.conn.close()
        self.conn = None
        self.cursor = None
        print("database is close!")

    # 执行单条sql
    def exec(self, sql, params=()):
        result = 0
        try:
            # 连接断开时，重新连接
            if self.conn is None:
                self.connect()
            # 执行sql语句
            result = self.cursor.execute(sql, params)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 关闭数据库连接
            self.close()
            # 如果发生错误则回滚
            self.conn.rollback()
        return result

    # 执行单条sql
    def exec_all(self, sql_list, params=()):
        result = 0
        try:
            # 连接断开时，重新连接
            if self.conn is None:
                self.connect()
            # 执行sql语句
            for sql in sql_list:
                res = self.cursor.execute(sql, params)
                if res is not None:
                    result += 1
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 关闭数据库连接
            self.close()
            # 如果发生错误则回滚
            self.conn.rollback()
        return result

    # 获取一条记录
    def get_one(self, sql, params=()):
        result = None
        try:
            # 连接断开时，重新连接
            if self.conn is None:
                self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
        return result

    # 获取多条条记录
    def get_many(self, sql, params=()):
        list_data = ()
        try:
            # 连接断开时，重新连接
            if self.conn is None:
                self.connect()
            self.cursor.execute(sql, params)
            list_data = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return list_data
