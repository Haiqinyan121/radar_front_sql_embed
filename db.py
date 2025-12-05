import pymysql

def safe_execute(func):
    """装饰器：统一处理数据库异常"""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except pymysql.MySQLError as e:
            print(f"数据库错误: {e}")
            return None
    return wrapper

class MySQLHelper:
    @safe_execute
    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def _execute(self, sql, params=None):
        """私有方法：执行SQL并提交"""
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
        self.conn.commit()
        return cursor.rowcount

    def insert(self, table, data):
        """插入单条数据"""
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({keys}) VALUES ({values})"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            return cursor.lastrowid  # 返回新插入的主键ID

    def update(self, table, data, where="1=1"):
        """更新数据"""
        set_clause = ', '.join([f"{k}=%s" for k in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        self._execute(sql, tuple(data.values()))

    def delete(self, table, where="1=1", params=None):
        """删除数据"""
        sql = f"DELETE FROM {table} WHERE {where}"
        self._execute(sql, params or ())

    def query(self, sql, params=None):
        """通用查询"""
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def close(self):
        """关闭连接"""
        self.conn.close()


# 初始化连接
db = MySQLHelper('localhost', 'root', 'root', 'hmbld')


# 示例插入数据
#user_id = db.insert('heart_rate', {'record_time': 1234567890, 'heart_rate': 75.5})

# 查询数据
data = db.query("SELECT * FROM heart_rate LIMIT 10")
print(data)

# 关闭连接
db.close()