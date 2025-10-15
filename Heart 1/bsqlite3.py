import sqlite3
#table creation
conn=sqlite3.connect("users.db")
cursor=conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS USERS(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        contactnumber TEXT,
        gender TEXT,
        email TEXT,
        password TEXT,
        address TEXT
   );   """
)
conn.commit()
conn.close()