#import sqlite3
import mariadb
import csv

#connection = sqlite3.connect('database.db')

conn = mariadb.connect(
         host='127.0.0.1',
         port= 3306,
         user='skofqq',
         password='1222245w',
         database='discogr')


#with open('schema.sql') as f:
#    connection.executescript(f.read())

#cur = connection.cursor()

cur = conn.cursor()

#with open('Discography_DB.csv') as csvfile:
#    datareader = csv.reader(csvfile, delimiter=';')
#    for row in datareader:
#
#        cur.execute("INSERT INTO posts (artist, song, duration, album, year, label, genre, cover) VALUES #(?, ?, ?, ?, ?, ?, ?)",(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))

# cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
#             ('Second Post', 'Content for the second post')
#             )


conn.close()

#connection.commit()
#connection.close()
