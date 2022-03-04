from flask import request, session
from flask_socketio import SocketIO
from flask_socketio import emit

from app.socket.utils import getSid, numMembers, popSid, setSid

sio = SocketIO()

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

@sio.on('connect')
def connect():
    sid = request.sid      
    memberId = request.args['memberId']
    print(sid)
    print('memberId', memberId)
    #if memberId == None: # not member is logged in
    #    raise ConnectionRefusedError('unauthorized!')
    oldSid = getSid(memberId)
    print('oldSid', oldSid)
    if getSid(memberId) != None and sid != getSid(memberId):
        print('disconnecting member')
        disconnectMember(memberId)
    print('adding member')
    setSid(memberId, sid)
    print(str(numMembers()) + ' members connected')

@sio.event
def message(json):
    print(session)
    print('received json: ' + str(json))
    emit('message', 'sup')

@sio.on('disconnect')
def disconnect():
    disconnectMember(request.sid)
    print('goodbye')

@sio.on_error()  # Handles the default namespace
def error_handler(e):
    print(str(e))