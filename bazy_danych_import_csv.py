import psycopg2

conn = psycopg2.connect("dbname='alan' user='alan' host='localhost' password='alan'")
cur = conn.cursor()
with open('tables/pokemon.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'pokemon', sep=',')
    
conn.commit()
