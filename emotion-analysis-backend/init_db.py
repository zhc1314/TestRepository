import pymysql

def init_database():
    # 连接 MySQL
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='0755',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    try:
        # 读取 SQL 文件
        with open('init.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割并执行 SQL 语句
        statements = sql_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    conn.commit()
                except Exception as e:
                    print(f"执行语句时出错: {e}")
                    print(f"语句内容: {statement[:100]}...")
        
        print("数据库初始化成功!")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    init_database()