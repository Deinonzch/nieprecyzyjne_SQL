import psycopg2

# Try to connect

try:
    conn=psycopg2.connect("dbname='Kuhaku' user='deinonzch'")
except:
    print("I am unable to connect to the database.")
    
cur = conn.cursor()
try:
    cur.execute("""SELECT * from pokemon WHERE attack>35""")
except:
    print("I can't SELECT from pokemon")

rows = cur.fetchall()
print("\nRows: \n")
for row in rows:
    print("   ", row)

