import mysql.connector

c = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="somyaa",
)
print("CONNECTION STATUS:", c.is_connected())
x = c.cursor()
x.execute('CREATE DATABASE IF NOT EXISTS music_playlist;')




c.commit()
c.close()
