import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

try:
   con = psycopg2.connect(dbname='Kuhaku', user='deinonzch')
except:
    print("I am unable to connect to the database")

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

cur = con.cursor()
cur.execute("CREATE DATABASE %s  ;" % self.db_name)

