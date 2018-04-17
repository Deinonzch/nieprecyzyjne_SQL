import psycopg2

conn = psycopg2.connect("dbname='Kuhaku' user='deinonzch'")
cur = conn.cursor()
with open('TopBabyNamesbyState.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'baby_name', sep=',')
    
conn.commit()
