from app.socket.init import sio

memberIdtoSid = dict()

def setSid(memberId, sid):
    memberIdtoSid[memberId] = sid

def getSid(memberId):
    return memberIdtoSid[memberId]

def getSids(member1Id, member2Id):
    return (memberIdtoSid.get(member1Id), memberIdtoSid.get(member2Id))

def popSid(memberId):
    return memberIdtoSid.pop(memberId)

def addToRoom(sid, roomName):
    sio.join_room(roomName, sid=sid)

def removeFromRoom(sid, roomName):
    sio.leave_room(roomName, sid=sid)

def emitMessageToRoom(event, data, roomName):
    sio.emit(event, data, room=roomName)

def destroyRoom(roomName):
    sio.close_room(room=roomName)

def disconnectMember(memberId):
    sid = popSid(memberId)
    if sid != None:
        sio.disconnect(sid)

