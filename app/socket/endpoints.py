from flask import request
from app.socket.init import sio
from app.socket.utils import disconnectMember, getSid, getSids, setSid, popSid

@sio.on('connect')
def connect():
    sid = request.sid      
    print('sid', sid)
    memberId = request.headers['MEMBERID']
    print('memberid', memberId)
    if sid != getSid(memberId):
        disconnectMember(memberId)
    setSid(memberId, sid)
    sio.emit('message', sid=sid)

@sio.on('disconnect')
def disconnect():
    disconnectMember(request.sid)
    print('goodbye')

@sio.on('message')
def message(json):
    print(str(json))