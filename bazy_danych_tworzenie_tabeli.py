import psycopg2
conn = psycopg2.connect("dbname='Kuhaku' user='deinonzch'")
cur = conn.cursor()
cur.execute("""
CREATE TABLE baby_name(
    state text,
    gender text,
    year integer,
    top_name text,
    occurences integer
)
""")
conn.commit()
