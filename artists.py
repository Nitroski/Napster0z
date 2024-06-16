


##import mysql.connector
##
##c = mysql.connector.connect(
##    host="localhost",
##    user="root",
##    passwd="somyaa",
##    database="music_playlist")
##
##
##
##print("CONNECTION STATUS:", c.is_connected())
##x = c.cursor()
##
##
####Artists TABLE CREATION (;
##
##def create_table(cursor):
##    
##        x.execute("""
##            CREATE TABLE IF NOT EXISTS Artists (
##                ArtistID INT AUTO_INCREMENT PRIMARY KEY,
##                ArtistName VARCHAR(100) NOT NULL)""")
##        x.execute('USE music_playlist ;')
##        
##        print("Artists Table created successfully!")
##
##create_table(x)
##
##c.commit()
##c.close()
