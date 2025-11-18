from django.db import connection
from django.conf import settings
import os

# 设置DJANGO_SETTINGS_MODULE环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointment_system.settings')

# 导入Django设置
import django
django.setup()

# 列出所有表
print("数据库中的所有表:")
for table in connection.introspection.table_names():
    print(f"- {table}")

# 查看auth_token表的结构
print("\nauth_token表的结构:")
cursor = connection.cursor()
cursor.execute("PRAGMA table_info(auth_token)")
columns = cursor.fetchall()
for column in columns:
    print(f"- {column}")

# 查看django_session表的结构
print("\ndjango_session表的结构:")
cursor.execute("PRAGMA table_info(django_session)")
columns = cursor.fetchall()
for column in columns:
    print(f"- {column}")