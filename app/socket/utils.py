from app.socket.init import sio

memberIdtoSid = dict()

def setSid(memberId, sid):
    memberIdtoSid[memberId] = sid

def getSids(member1Id, member2Id):
    return (memberIdtoSid.get(member1Id), memberIdtoSid.get(member2Id))

def addToRoom(sid, roomName):
    sio.enter_room(sid, roomName)
    sio.emit('session_made', { 'sessionId': roomName.split('=')[1] }, room=roomName)
