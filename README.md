# nieprecyzyjne_SQL

do zadziałania skryptu write_table.py, potrzebna jest biblioteka texttable:

pip3 install texttable

Bazy danych: https://public.tableau.com/en-us/s/resources

Tworzenie bazy:

$ sudo -u postgres createuser alan

$ sudo -u postgres createdb alan

$ sudo -u postgres psql

psql=# alter user alan with encrypted password 'alan';

psql=# grant all privileges on database alan to alan ;




tworzenie tabeli z pokemonami w postgresie:

1. uruchom w konsoli  python3 bazy_danych_tworzenie_tabeli.py
2. uruchom w konsoli  python3 bazy_danych_import_csv.py
3. gotowe

Do podania zapytania do bazy wystarczy uruchomić w konsoli write_table.py

Żeby usunąć tabelę wystarczy użyć wpisać w konsoli python3 delete_table.py 

