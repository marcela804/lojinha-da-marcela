# db.py - Clean MySQL connection for XAMPP
import mysql.connector
from mysql.connector import Error

def get_db():
    try:
        con = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="lojinha_da_marcela"
        )
        cur = con.cursor()
        cur.execute("USE lojinha_da_marcela")
        cur.close()
        return con
    except Error as e:
        print(f"DB Error: {e}")
        return None
