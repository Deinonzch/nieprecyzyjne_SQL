import psycopg2
conn = psycopg2.connect("dbname='alan' user='alan' host='localhost' password='alan'")
cur = conn.cursor()
##,Name,Type,Total,HP,Attack,Defense,Special Attack,Special Defense,Speed
cur.execute("""
CREATE TABLE pokemon(
    number text,
    name text,
    type text,
    total integer,
    hp integer,
    attack integer,
    defense integer,
    special_attack integer,
    special_defense integer,
    speed integer
)
""")
conn.commit()

cur.execute("""
CREATE TABLE pokemontypechart(
    attack text,
    defense text,
    effectiveness text,
    multiplier float
)
""")
conn.commit()

cur.execute("""
CREATE TABLE pokemonevolution(
    evolving_from text,
    evolving_to text,
    level integer,
    condition text,
	evolution_type text
)
""")
conn.commit()

cur.execute("""
CREATE TABLE animelist(
    score float,
    title text,
    type text,
    genres text,
    studios text,
    main_actors text
)
""")
conn.commit()

cur.execute("""
CREATE TABLE filmylist(
    id integer,
    tytul text,
    rezyser text,
    kraj text,
    rok_produkcji integer,
    budzet integer,
	czas integer,
	gatunek text
)
""")
conn.commit()

cur.execute("""
CREATE TABLE komputery(
    model text,
    cena integer,
    wielkość_pamięci integer,
    wielkość_dysku integer,
    częstotliwość_procesora float,
    rozmiar_monitora integer
)
""")
conn.commit()

cur.execute("""
CREATE TABLE categories(
    category_id integer,
    category_name text,
    description text
)
""")
conn.commit()

cur.execute("""
CREATE TABLE customers(
    customer_id integer,
    customer_name text,
    contact_name text,
	address text,
	city text,
	postal_code text,
	country text
)
""")
conn.commit()

cur.execute("""
CREATE TABLE products(
    product_id integer,
    product_name text,
    supplier_id integer,
	category_id integer,
	unit text,
	price float
)
""")
conn.commit()

conn.close()
