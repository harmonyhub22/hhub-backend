from flask import request, session
from flask_socketio import SocketIO, leave_room, join_room, rooms
from flask_socketio import emit
from app.services.MemberService import getMemberIdFromSid, getSid, setSid, updateSid, setOnline, setOffline, getBySid
from app.services.SessionService import getById as getSessionById
from app.services.LayerService import getById as getLayerById

sio = SocketIO()

def getRoomName(sessionId):
    return str("session-" + sessionId)

def addToRoom(sid, roomName):
    join_room(roomName, sid=sid)

def removeFromRoom(sid, roomName):
    leave_room(roomName, sid=sid)

def emitMessageToRoom(event, data, roomName, includeSelf=True):
    sio.emit(event, data, room=roomName, includeSelf=includeSelf)

def destroyRoom(roomName):
    sio.close_room(room=roomName)

def disconnectMember(sid):
    if sid == None:
        print('cant disconnect')
    else:
        member = getBySid(sid)
        if member is None:
            print('cant find member with the given sid')
        else:
            memberId = member.memberId
            updateSid(memberId, None)

@sio.on('connect')
def connect():
    sid = request.sid
    memberId = request.args['memberId']
    if memberId == None:
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
        addToRoom(sid, getRoomName(sessionId))
        emitMessageToRoom('message', 'sup to room', getRoomName(sessionId))

@sio.on('pull_layer')
def pull_layer(json):
    sid = request.sid
    memberId = getMemberIdFromSid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        return
    musicSession = getSessionById(sessionId)
    if (musicSession.member1Id == memberId or musicSession.member2Id == memberId):
        emitMessageToRoom('pull_layer', {}, getRoomName(sessionId), includeSelf=False)

@sio.on('finished')
def finishSong(json):
    print('received json: ' + str(json))

@sio.on('session_vote_end')
def sessionVoteEnd(json):
    sid = request.sid
    memberId = getMemberIdFromSid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        return
    musicSession = getSessionById(sessionId)
    if memberId != None and musicSession != None and (musicSession.member1Id == memberId or musicSession.member2Id == memberId):
        emitMessageToRoom('session_vote_end', "end_session", getRoomName(sessionId), True)

@sio.on('session_unvote_end')
def sessionUnVoteEnd(json):
    sid = request.sid
    memberId = getMemberIdFromSid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        return
    musicSession = getSessionById(sessionId)
    if memberId != None and musicSession != None and (musicSession.member1Id == memberId or musicSession.member2Id == memberId):
        emitMessageToRoom('session_unvote_end', "unend_session", getRoomName(sessionId), True)

@sio.on('session_room_message')
def sessionRoomMessage(json):
    sid = request.sid
    memberId = getMemberIdFromSid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        return
    musicSession = getSessionById(sessionId)
    name = ''
    if musicSession.member1.memberId == memberId:
        name = str(musicSession.member1.firstname + ' ' + musicSession.member1.lastname)
    elif musicSession.member2.memberId == memberId:
        name = str(musicSession.member2.firstname + ' ' + musicSession.member2.lastname)
    data = dict()
    print(json)
    data['name'] = name
    data['message'] = json['message']
    if memberId != None and musicSession != None and (musicSession.member1Id == memberId or musicSession.member2Id == memberId):
        emitMessageToRoom('session_room_message', data, getRoomName(sessionId), True)

@sio.on('disconnect')
def disconnect():
    disconnectMember(request.sid)
    print('goodbye')

@sio.on_error()  # Handles the default namespace
def error_handler(e):
    print(str(e))