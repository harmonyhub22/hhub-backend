from flask import request, session
from flask_socketio import SocketIO, leave_room, join_room, rooms
from flask_socketio import emit
from app.services.MemberService import getMemberIdFromSid, getSid, setSid, updateSid
from app.services.SessionService import getById as getSessionById

sio = SocketIO()

def addToRoom(sid, roomName):
    join_room(roomName, sid=sid)

def removeFromRoom(sid, roomName):
    leave_room(roomName, sid=sid)

def emitMessageToRoom(event, data, roomName, includeSelf=True):
    sio.emit(event, data, room=roomName, includeSelf=includeSelf)

def destroyRoom(roomName):
    sio.close_room(room=roomName)

def disconnectMember(memberId):
    sid = updateSid(memberId, None)
    if sid != None:
        disconnect(sid)

@sio.on('connect')
def connect():
    sid = request.sid      
    memberId = request.args['memberId']
    if memberId == None: # not member is logged in
        raise ConnectionRefusedError('unauthorized!')
    if getSid(memberId) != None and sid != getSid(memberId):
        disconnectMember(memberId)
    setSid(memberId, sid)

@sio.event
def message(json):
    print('received json: ' + str(json))
    emit('message', 'sup')

@sio.on('join_session')
def joinRoom(json):
    print('received json: ' + str(json))
    sid = request.sid
    memberId = getMemberIdFromSid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        return
    musicSession = getSessionById(sessionId)
    if memberId != None and musicSession != None and (musicSession.member1Id == memberId or musicSession.member2Id == memberId):
        addToRoom(sid, str('session-' + sessionId))
        emitMessageToRoom('message', 'sup to room', str('session=' + sessionId))

@sio.on('add_layers')
def add_layer(json):
    sid = request.sid
    layerIds = json['layerIds']
    roomNames = rooms(sid=sid)
    if len(roomNames) < 1: return
    name = roomNames[0]
    emitMessageToRoom('layer_added', { layerIds: layerIds }, name, includeSelf=False)

@sio.on('finished')
def finishSong(json):
    print('received json: ' + str(json))
    

@sio.on('disconnect')
def disconnect():
    disconnectMember(request.sid)

@sio.on_error()  # Handles the default namespace
def error_handler(e):
    print(str(e))