import atexit 
import sqlite3


db_con = sqlite3.connect('db.sqlite3')
atexit.register(db_con.close)
