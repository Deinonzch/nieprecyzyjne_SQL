import psycopg2

conn = psycopg2.connect("dbname='alan' user='alan' host='localhost' password='alan'")
cur = conn.cursor()
with open('tables/pokemon.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'pokemon', sep=',')
    
conn.commit()

with open('tables/typechart.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'pokemontypechart', sep=',')
    
conn.commit()

with open('tables/evolution.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'pokemonevolution', sep=',')
    
conn.commit()

with open('tables/anime_score.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'animelist', sep=',')
    
conn.commit()

with open('tables/filmy.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'filmylist', sep='	')
    
conn.commit()

with open('tables/komputery.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'komputery', sep='	')
    
conn.commit()

with open('tables/w3schools/categories.tsv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'categories', sep='	')
    
conn.commit()

with open('tables/w3schools/customers.tsv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'customers', sep='	')
    
conn.commit()

with open('tables/w3schools/products.tsv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'products', sep='	')
    
conn.commit()

conn.close()
