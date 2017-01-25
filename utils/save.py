import sqlite3
import json

f = "../data/data.db"


#before this we need to check if the door has been accessed

#needs userid to get roomid, use them both to update in rooms
def leaveroom(user, roominfo):
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT user_id FROM users WHERE username=?")
    userID = c.execute(query,(user,)).fetchone()[0]
    query = ("SELECT current_room FROM users WHERE user_id=?")
    currentroom = c.execute(query, (userID,)).fetchone()[0]
    query = ("UPDATE rooms SET terrain=? WHERE user_id=? AND room_id=?")
    c.execute(query,(roominfo, userID, currentroom))
    db.commit()
    db.close()

def checkdoor(user, door):#returns the room that door links to
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT user_id FROM users WHERE username=?")
    userID = c.execute(query,(user,)).fetchone()[0]
    query = ("SELECT current_room FROM users WHERE user_id=?")
    currentroom = c.execute(query, (userID,)).fetchone()[0]
    query = ("SELECT exits FROM rooms WHERE user_id=? AND room_id=?")
    c.execute(query,(userID,currentroom))
    doors = c.fetchone()[0]
    d = json.loads(doors)
    db.commit()
    db.close()
    if door == 1:
        return d['d1']
    elif door == 2:
        return d['d2']
    elif door == 3:
        return d['d3']
    else:
        return d['d4']
    
def enterOld(user, roomid):#returns the terrain for an old room and updates the current room to roomid
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT user_id FROM users WHERE username=?")
    userID = c.execute(query,(user,)).fetchone()[0]
    query = ("SELECT terrain FROM rooms WHERE user_id=? AND room_id=?")
    terrain = c.execute(query,(userID, roomid)).fetchone()[0]
    db.commit()
    db.close()
    updateRoom(userID, roomid)
    return terrain
    
def door(playerinfo, roominfo, user):
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT user_id FROM users WHERE username=?")
    userID = c.execute(query,(user,)).fetchone()[0]
    print 'room'
    #print playerinfo
    terrains = json.dumps(roominfo)
    saveRoom(userID, 'enemies', 'items', terrains, 1)

def saveRoom(userid, enemies, items, terrain, exitdoor):#needs userid, old room id, old terrain, the exited door
    #find the highest room id
    newroomid = newID(userid)
    #update the room in the users table
    currentroom = updateRoom(userid, newroomid)
    #Access the old room and set the exited door value to the new room id
    updateOld(userid, currentroom, newroomid, enemies, items, terrain, exitdoor)
    #Generate the new room with the new id and assign the appropriate door value to the old room id
    makeNew(userid, currentroom, newroomid, exitdoor)
    
def updateRoom(userid, roomid):#updates the current room
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("UPDATE users SET current_room=? WHERE user_id=?")
    sel = c.execute(query,(roomid, userid))
    db.commit()
    db.close()
    
def newID(userID):
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT MAX(room_id) FROM rooms WHERE user_id=?")
    r = c.execute(query,(userID,))
    r = r.fetchone()[0]
    db.commit()
    db.close()
    return r+1


def updateOld(userid, oldroom, newroom, enemies, items, terrain, olddoor):
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("UPDATE rooms SET enemies=? WHERE user_id=? AND room_id=?")
    c.execute(query,(enemies, userid, oldroom))
    query = ("UPDATE rooms SET items=? WHERE user_id=? AND room_id=?")
    c.execute(query,(items, userid, oldroom))
    query = ("UPDATE rooms SET terrain=? WHERE user_id=? AND room_id=?")
    c.execute(query,(terrain, userid, oldroom))  
    query = ("SELECT * FROM rooms WHERE user_id=? AND room_id=?")
    c.execute(query,(userid,oldroom))
    doors = c.fetchone()[5]
    print doors
    d = json.loads(doors)
    if olddoor == 1:
        d['d1'] = newroom
    elif olddoor == 2:
        d['d2'] = newroom
    elif olddoor == 3:
        d['d3'] = newroom
    else:
        d['d4'] = newroom
    a = json.dumps(d)
    print a
    query = ("UPDATE rooms SET exits=? WHERE user_id=? AND room_id=?")
    c.execute(query,(a,userid,oldroom))
    db.commit()
    db.close()

def makeNew(userid, oldroom, newroom, olddoor):
    db = sqlite3.connect(f)
    c = db.cursor()
    s = ''
    d = {}
    d["d1"] = -1
    d["d2"] = -1
    d["d3"] = -1
    d["d4"] = -1
    if olddoor == 1:
        d["d3"] = oldroom
    elif olddoor == 2:
        d["d4"] = oldroom
    elif olddoor == 3:
        d["d1"] = oldroom
    else:
        d["d2"] = oldroom
    doors = json.dumps(d)
    query = ("INSERT INTO rooms VALUES (?,?,'enemies','items','terrain',?)")
    c.execute(query,(userid,newroom,doors))
    db.commit()
    db.close()


#db = sqlite3.connect(f)
#c = db.cursor()
#c.execute("CREATE TABLE rooms (user_id INTEGER, room_id INTEGER, enemies TEXT, items TEXT, terrain TEXT, exits T#EXT)")
#c.execute('''INSERT INTO rooms VALUES (0,1,'enemies','items','terrain','{"d1":-1,"d2":-1,"d3":-1,"d4":-1}')''')
#db.commit()
#db.close()
#saveRoom(0,'enemies','items','terrain',1)
#updateRoom(0,1)
#leaveroom('asdf','hi')
#enterOld('asdf',3)
