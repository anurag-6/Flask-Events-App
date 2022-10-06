import sqlite3
con = sqlite3.connect('eventsApp.db')
cur = con.cursor()


# Creating table events 
cur.execute('CREATE TABLE EVENTS (id INTEGER PRIMARY KEY AUTOINCREMENT ,ev_name varchar(100),ev_date text,ev_prio varchar(20),ev_img text)')

con.close()