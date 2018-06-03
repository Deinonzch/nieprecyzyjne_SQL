import psycopg2

# Try to connect
#"SELECT * from pokemon WHERE attack>35"
print('Podaj zapytanie SQL: ')
zapytanie=input()

try:
    conn=psycopg2.connect("dbname='alan' user='alan' host='localhost' password='alan'")
except:
    print("I am unable to connect to the database.")
    
cur = conn.cursor()
try:
    cur.execute(zapytanie)
except:
    print("I can't SELECT from pokemon")

rows = cur.fetchall()
print("\nRows: \n")
for row in rows:
    print("   ", row)

