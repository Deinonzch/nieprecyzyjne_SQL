import psycopg2
import texttable as tt
# Try to connect
#"SELECT * from pokemon WHERE attack>35"
#number,name,type,total,hp,attack,defense,special_attack,specialdefense,speed - pokemon table
#attack,defense,effectiveness,multiplier - pokemontypechart table
#evolving_from,evolving_to,level,condition,evolution_type pokemonevolution table
#score,title,type,genres,studios,main_actors - animelist table
#id,tytul,rezyser,kraj,rok_produkcji,budzet,czas,gatunek - filmylist table
#model,cena,wielkość_pamięci,wielkość_dysku,częstotliwość_procesora,rozmiar_monitora - komputery table
#category_id,category_name,description - categories table
#customer_id,customer_name,contact_name,address,city,postal_code,country - customers table
#product_id,product_name,supplier_id,category_id,unit,price - products table
print('Podaj zapytanie SQL: ')
zapytanie=input()

try:
    conn=psycopg2.connect("dbname='alan' user='alan' host='localhost' password='alan'")
except:
    print("I am unable to connect to the database.")
rows=[]
column_names = []
cur = conn.cursor()
try:
    cur.execute(zapytanie)
    column_names = [desc[0] for desc in cur.description]
    for row in cur:
        rows.append(row)
except:
    print("I can't do SELECT")

#rows = cur.fetchall()
print("\nRows: \n")


tab = tt.Texttable()

tab.add_rows(rows, tab.header(column_names))

s = tab.draw()
print(s)

conn.close()

