import psycopg2
from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute("CREATE SCHEMA IF NOT EXISTS public;")
conn.commit()
print("✅ public schema created")
cursor.close()
conn.close()


# The issue: Neon doesn't automatically pick a schema for your tables to live in.
# PostgreSQL organizes tables inside schemas — think of a schema as a folder.
# The default folder is called public. Neon sometimes doesn't set this default,
# so when you say CREATE TABLE, PostgreSQL says "create it where? I don't know which folder."
