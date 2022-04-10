from flask import request, session
from flask_socketio import SocketIO, leave_room, join_room, rooms, send
from flask_socketio import emit
from app.services.MemberService import getSid, setSid, updateSid, setOnline, setOffline, getBySid
from app.services.SessionService import getById as getSessionById
from app.services.LayerService import getById as getLayerById

sio = SocketIO()

def getRoomName(sessionId):
    return str("session-" + sessionId)

def addToRoom(sid, roomName):
    print('adding ', sid, ' to', roomName)
    join_room(roomName, sid=sid, namespace="/")
    print('worked')

def getSidRooms(sid):
    return rooms(sid=sid, namespace="/")

def removeFromRoom(sid, roomName):
    leave_room(roomName, sid=sid, namespace="/")

def emitMessageToRoom(event, data, roomName, includeSelf=True):
    sio.emit(event, data, room=roomName, includeSelf=includeSelf)

def emitToSid(event, data, sid):
    sio.emit(event, data, sid=sid)

def destroyRoom(roomName):
    sio.close_room(room=roomName)

def destroyRoomById(sessionId):
    destroyRoom(getRoomName(sessionId))

def disconnectMember(memberId):
    if memberId == None:
        print('cant disconnect')
    else:
        updateSid(memberId, None)

@sio.on('connect')
def connect():
    sid = request.sid
    memberId = request.args['memberId']
    if memberId == None:
        raise ConnectionRefusedError('unauthorized!')
    member = getSid(memberId)
    if member != None and sid != getSid(memberId):
        disconnectMember(memberId)
    setSid(memberId, sid)

'''
@sio.event
def message(json):
    print('received json: ' + str(json))
    emit('message', 'sup')
'''

@sio.on('join_session')
def joinRoom(json):
    print('received json: ' + str(json))
    sid = request.sid
    member = getBySid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        print('no session id sent')
        return
    if member == None:
        print('no member sound')
        return
    musicSession = getSessionById(sessionId)
    if member != None and musicSession != None and (musicSession.member1Id == member.memberId or musicSession.member2Id == member.memberId):
        addToRoom(sid, getRoomName(sessionId))
        emitMessageToRoom('message', 'sup to room', getRoomName(sessionId))

@sio.on('pull_layer')
def pull_layer(json):
    sid = request.sid
    member = getBySid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        return
    if member == None:
        return
    musicSession = getSessionById(sessionId)
    if (musicSession.member1Id == member.memberId or musicSession.member2Id == member.memberId):
        emitMessageToRoom('pull_layer', {}, getRoomName(sessionId), includeSelf=False)

@sio.on('session_vote_end')
def sessionVoteEnd(json):
    sid = request.sid
    member = getBySid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        return
    if member == None:
        return
    musicSession = getSessionById(sessionId)
    if musicSession != None and (musicSession.member1Id == member.memberId or musicSession.member2Id == member.memberId):
        emitMessageToRoom('session_vote_end', "end_session", getRoomName(sessionId), True)

@sio.on('session_unvote_end')
def sessionUnVoteEnd(json):
    sid = request.sid
    member = getBySid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        return
    if member == None:
        return
    musicSession = getSessionById(sessionId)
    if musicSession != None and (musicSession.member1Id == member.memberId or musicSession.member2Id == member.memberId):
        emitMessageToRoom('session_unvote_end', "unend_session", getRoomName(sessionId), True)

@sio.on('session_room_message')
def sessionRoomMessage(json):
    sid = request.sid
    print(sid)
    member = getBySid(sid)
    sessionId = json['sessionId']
    if sessionId == None:
        return
    if member == None:
        return
    musicSession = getSessionById(sessionId)
    name = ''
    if musicSession.member1.memberId == member.memberId:
        name = str(musicSession.member1.firstname + ' ' + musicSession.member1.lastname)
    elif musicSession.member2.memberId == member.memberId:
        name = str(musicSession.member2.firstname + ' ' + musicSession.member2.lastname)
    data = dict()
    print(json)
    data['name'] = name
    data['message'] = json['message']
    if musicSession != None and (musicSession.member1Id == member.memberId or musicSession.member2Id == member.memberId):
        emitMessageToRoom('session_room_message', data, getRoomName(sessionId), True)

@sio.on('leave_session')
def sessionLeaveRoom(json):
    sid = request.sid
    sessionId = json['sessionId']
    try:
        removeFromRoom(sid, getRoomName(sessionId))
    except:
        print('could not leave room')

@sio.on('disconnect')
def disconnect():
    disconnectMember(request.sid)

@sio.on_error()  # Handles the default namespace
def error_handler(e):
    print(str(e))