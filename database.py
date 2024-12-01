import aiomysql
import asyncio

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn =aiomysql.connect(
                user='root',
                password='!yuntang9213',
                db='student',
                host='localhost',
                charset='utf8'
            )
            print("MySQL is connected")


    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass  # We don't close the connection here

    async def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    async def get_user_info(self, user_id):
        await self.connect()
        return await self.select_data('info', 'line_id', user_id)

    async def insert_data(self, table_name, data):
        await self.connect()
        try:
            async with self.conn.cursor() as cursor:
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                await cursor.execute(query, list(data.values()))
                await self.conn.commit()
                # print("Data inserted successfully")
        except aiomysql.Error as err:
            print(f"Error: {err}")
            await self.conn.rollback()

    async def select_data(self, table_name, key, value, field=''):
        await self.connect()
        indices = {
            'department': 0,
            'student_id': 1,
            'identity': 2,
            'last_used': 3,
            'name': 4,
            'line_id': 5,
            'mode': 6,
            'nationality': 7
        }
        try:
            async with self.conn.cursor() as cursor:
                query = f"SELECT * FROM {table_name} WHERE {key} = %s"
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
        await self.connect()
        try:
            async with self.conn.cursor() as cursor:
                columns = ', '.join([f"{k} = %s" for k in new_data.keys()])
                query = f"UPDATE {table_name} SET {columns} WHERE {key} = %s"
                await cursor.execute(query, list(new_data.values()) + [value])
                await self.conn.commit()
                # print("Data updated successfully")
        except aiomysql.Error as err:
            print(f"Error: {err}")
            await self.conn.rollback()

    async def delete_data(self, table_name, key, value):
        await self.connect()
        try:
            async with self.conn.cursor() as cursor:
                query = f"DELETE FROM {table_name} WHERE {key} = %s"
                await cursor.execute(query, (value,))
                await self.conn.commit()
                # print("Data deleted successfully")
        except aiomysql.Error as err:
            print(f"Error: {err}")
            await self.conn.rollback()

db = Database()  # Create a single instance of the Database class