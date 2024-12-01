import aiomysql


class Database:
    def __init__(self):
        self.pool = None
        self.userNeedRatings = []

    async def connect(self):
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                user='linebot',
                password='',
                db='student_info',
                host='localhost',
                charset='utf8',
                minsize=1,
                maxsize=10,
                autocommit=True
            )
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;")
            print("MySQL connection pool is created")

    async def get_connection(self):
        if not self.pool:
            await self.connect()
        return await self.pool.acquire()

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            print("MySQL connection pool is closed")
            self.pool = None


    async def get_all_users_info(self, table_name):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # Safely construct the query
                query = f"SELECT * FROM `{table_name}`"
                try:
                    await cursor.execute(query)
                    records = await cursor.fetchall()
                    return records
                except aiomysql.Error as err:
                    print(f"錯誤：{err}")
                    return []


    async def get_user_info(self, user_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                query = "SELECT * FROM info WHERE line_id = %s"
                try:
                    await cursor.execute(query, (user_id,))
                    records = await cursor.fetchall()
                    if not records:
                        return None
                    return records[0]

                except aiomysql.Error as err:
                    print(f"錯誤：{err}")
                    return None

    async def insert_data(self, table_name, data):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                try:
                    await cursor.execute(query, list(data.values()))
                    await conn.commit()
                except aiomysql.Error as err:
                    print(f"Error: {err}")
                    await conn.rollback()
     

    async def select_data(self, table_name, key, value, field=''):
        indices = {
            'department': 0,
            'student_id': 1,
            'identity': 2,
            'last_used': 3,
            'name': 4,
            'line_id': 5,
            'mode': 6,
            'nationality': 7,
            'frequency': 8,
            'last_message': 9
        }
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = f"SELECT * FROM {table_name} WHERE {key} = %s"
                try:
                    await cursor.execute(query, (value,))
                    records = await cursor.fetchall()
                    if not records:
                        res = None
                    else:
                        res = records[0]
                    if field:
                        return res[indices[field]]
                    return res
                except aiomysql.Error as err:
                    print(f"Error: {err}")

    async def update_data(self, table_name, key, value, new_data):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                columns = ', '.join([f"{k} = %s" for k in new_data.keys()])
                query = f"UPDATE {table_name} SET {columns} WHERE {key} = %s"
                try:
                    await cursor.execute(query, list(new_data.values()) + [value])
                    await conn.commit()
                except aiomysql.Error as err:
                    print(f"Error: {err}")
                    await conn.rollback()
    
    async def increment_column(self, table_name, key, value, column_name):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:  # 使用 DictCursor 返回结果为字典形式
                
                update_query = f"UPDATE {table_name} SET {column_name} = {column_name} + 1 WHERE {key} = %s"
                select_query = f"SELECT * FROM {table_name} WHERE {key} = %s"  

                try:
                    await cursor.execute(update_query, (value,))
                    await conn.commit()

                    await cursor.execute(select_query, (value,))
                    result = await cursor.fetchone()


                    return result if result else None
                except aiomysql.Error as err:
                    print(f"Error: {err}")
                    await conn.rollback()
                    return None

    async def add_rating_record(self, line_id, score):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    # 從 info 表中取得使用者名稱
                    await cursor.execute("SELECT name FROM info WHERE line_id = %s", (line_id,))
                    user_info = await cursor.fetchone()
                    
                    # 如果找不到使用者名稱，則返回 None
                    if not user_info:
                        return None

                    # 插入 rating_record 表
                    insert_query = """
                        INSERT INTO rating_record (name, score) 
                        VALUES (%s, %s)
                    """
                    await cursor.execute(insert_query, (user_info['name'], score))
                    
                    # 提交變更
                    await conn.commit()
                    return user_info

                except aiomysql.Error as err:
                    print(f"Error: {err}")
                    await conn.rollback()
                    return False

                    


    async def delete_data(self, table_name, key, value):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = f"DELETE FROM {table_name} WHERE {key} = %s"
                try:
                    await cursor.execute(query, (value,))
                    await conn.commit()
                except aiomysql.Error as err:
                    print(f"Error: {err}")
                    await conn.rollback()

    async def update_data_and_get_info(self, table_name, key, value, new_data):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    # Start a transaction
                    await conn.begin()

                    # Construct the SQL query for updating the data
                    columns = ', '.join([f"{k} = %s" for k in new_data.keys()])
                    update_query = f"UPDATE {table_name} SET {columns} WHERE {key} = %s"

                    # Execute the update query
                    await cursor.execute(update_query, list(new_data.values()) + [value])

                    # After the update, retrieve the updated record
                    select_query = f"SELECT * FROM {table_name} WHERE {key} = %s"
                    await cursor.execute(select_query, (value,))
                    updated_record = await cursor.fetchone()

                    if not updated_record:
                        await conn.rollback()
                        return None

                    # Convert the updated record to a dictionary
                    columns_query = f"SHOW COLUMNS FROM {table_name}"
                    await cursor.execute(columns_query)
                    column_names = [row[0] for row in await cursor.fetchall()]

                    updated_info = dict(zip(column_names, updated_record))

                    # Commit the transaction
                    await conn.commit()
                    return updated_info

                except aiomysql.Error as err:
                    print(f"Error: {err}")
                    await conn.rollback()
                    return None
