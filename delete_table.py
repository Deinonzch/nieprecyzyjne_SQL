import psycopg2
conn = psycopg2.connect("dbname='alan' user='alan' host='localhost' password='alan'")
cur = conn.cursor()
cur.execute('DROP TABLE "pokemon";')  
conn.commit()
conn.close()
