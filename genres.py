##   
##import mysql.connector
##
##import mysql.connector
##
##c = mysql.connector.connect(
##    host="localhost",
##    user="root",
##    passwd="somyaa",
##    database="music_playlist"
##)
##
##print("CONNECTION STATUS:", c.is_connected())
##x = c.cursor()
##
##
####Genres TABLE CREATION (;
##
##def create_table(cursor):
##    x.execute("""
##                CREATE TABLE IF NOT EXISTS Genres (
##                GenreID INT PRIMARY KEY,
##                GenreName VARCHAR(50) NOT NULL)""")
##
##    x.execute('USE music_playlist ;')
##
##    print("Genres Table created successfully!")
##
##
##create_table(x)
##
##
##c.commit()
##c.close()
