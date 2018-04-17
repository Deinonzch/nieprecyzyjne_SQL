import psycopg2

# Try to connect

try:
    conn=psycopg2.connect("dbname='Kuhaku' user='deinonzch'")
except:
    print("I am unable to connect to the database.")
    
cur = conn.cursor()
try:
    cur.execute("""SELECT * from baby_name WHERE gender='F'""")
except:
    print("I can't SELECT from baby_name")

rows = cur.fetchall()
print("\nRows: \n")
for row in rows:
    print("   ", row)

