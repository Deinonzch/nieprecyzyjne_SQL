import psycopg2
conn = psycopg2.connect("dbname='Kuhaku' user='deinonzch'")
cur = conn.cursor()
cur.execute('DROP TABLE "pokemon";')  
conn.commit()
conn.close()
