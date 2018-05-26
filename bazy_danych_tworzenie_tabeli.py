import psycopg2
conn = psycopg2.connect("dbname='Kuhaku' user='deinonzch'")
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
