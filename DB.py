import sqlite3

db = sqlite3.connect('database.db', check_same_thread=False)

def newMessage(username, message, website):
    global db
    db.execute('insert into guestbook (username, message, website, entrydate) values (?, ?, ?, CURRENT_TIMESTAMP)', [username, message, website])
    db.commit()

def getMessages():
    global db
    cursor = db.execute('select * from guestbook')
    return cursor.fetchall()
    
def closeDB():
    global db
    db.close()

#Stuff:
def createTable():
    global db
    db.execute('create table if not exists guestbook (id integer primary key AUTOINCREMENT, username text not null, message text, website text, entrydate datetime not null);')

if __name__ == '__main__':
    createTable()
    