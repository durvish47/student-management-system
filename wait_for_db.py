import time
import pymysql
import os

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "student_db")

print("⏳ Waiting for MySQL to be ready...")

while True:
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=3306
        )
        conn.close()
        print("✅ MySQL is ready!")
        break
    except Exception as e:
        print("❌ MySQL not ready yet. Retrying in 2 seconds...")
        time.sleep(2)
