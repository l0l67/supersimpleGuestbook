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

def setLastPost(ip):
    global db
    if _IPexists(ip):
        db.execute('update lastplaced set postdate = CURRENT_TIMESTAMP where ip_addr = ?', [ip])
    else:
        db.execute('insert into lastplaced (ip_addr, postdate) values (?, CURRENT_TIMESTAMP)', [ip])

def _IPexists(ip):
    global db
    cursor = db.execute('select exists(select 1 from lastplaced where ip_addr = ?)', [ip]).fetchone()[0]
    print(cursor)
    return cursor == 1

def getLastPost(ip):
    global db
    cursor = db.execute("select ip_addr, datetime(postdate, 'localtime') from lastplaced where ip_addr = ?", [ip])
    return cursor.fetchall()

def closeDB():
    global db
    db.close()

#Stuff:
def createTable():
    global db
    db.execute('create table if not exists guestbook (id integer primary key AUTOINCREMENT, username text not null, message text, website text, entrydate datetime not null);')
    db.execute('create table if not exists lastplaced (id integer primary key AUTOINCREMENT, ip_addr text not null, postdate datetime not null)')

if __name__ == '__main__':
    createTable()
    