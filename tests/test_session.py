import datetime
import json
import pytest
from app.db.db import db
from app.db.models.MatchingQueue import MatchingQueue
from app.db.models.Session import Session
import uuid
from app.exceptions.BadRequestException import BadRequestException
from app.services.AuthService import generateToken, getByMemberId as getByMemberIdAuth
from app.services.AuthService import getByMemberId
from app.services.MatchingQueueService import joinOrAttemptMatch
from app.services.SessionService import getByMemberId as getByMemberIdSession, getLiveSession

'''
Route: api/session
REST operation: GET
Service method tested: getAllByMemberId()
Cases to test:
1. invalid session ID (catch BadRequestException)
2. normal case: valid session ID, member ID exists, queryset should have only 1 session. check metadata
'''
def testGetSession(app, client, auth):
    deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    willId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')
    
    auth.login()
    with app.app_context():
        authMember = getByMemberIdAuth(deanId)
        token = generateToken(authMember.memberId)
        client.set_cookie(app, 'hhub-token', str(token))

    # setting up a new session first
    existingSessionId = None
    with app.app_context():
        response = client.post('/api/queue')
        existingSessionId = Session.query.first().sessionId

    # case 1
    response = client.get('api/session/28cf2179-0000-0000-a14c-3c09bd904365')
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "no session exists with this session ID" in jsonResponse['message']

    # case 2
    response = client.get('api/session/' + str(existingSessionId))
    assert response.status_code == 200
    with app.app_context():
        query = Session.query.all()
        assert len(query) == 1
    jsonResponse = json.loads(response.data.decode('utf-8'))
    partner, layers, endTime = jsonResponse['member2']['email'], jsonResponse['layers'], jsonResponse['endTime']
    assert partner == "will@tamu.edu"
    assert layers == []
    assert endTime == None

'''
Route: api/session/live
REST operation: GET
Service method tested: getLiveSession()
Cases to test:
1. if member is currently in a session (no endTime set), return a session
2. if member is not in a session, return nothing
'''
def testGetLiveSession(app, client, auth):
    deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    willId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')
    
    auth.login()
    with app.app_context():
        authMember = getByMemberIdAuth(deanId)
        token = generateToken(authMember.memberId)
        client.set_cookie(app, 'hhub-token', str(token))
        
        # set up new session
        client.post('/api/queue')
    
    # case 1
    response = client.get('api/session/live')
    assert response.status_code == 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    with app.app_context():
        query = getLiveSession(deanId)
        assert query

    # end the session
    with app.app_context():
        session = getByMemberIdSession(deanId)
        session.endTime = datetime.datetime.utcnow()
        db.session.commit()

    # case 2
    with app.app_context():
        query = getLiveSession(deanId)
        assert not query

'''
Route: api/session/<session ID>/end
REST operation: POST
Service method tested: endSession()
Cases to test:
1. no session is created, so you cant end one (catch BadRequestException)
2. member is not yet in a session, so cant end one (catch BadRequestException)
3. normal case: end a session the member is in. check that the session record has a properly updated end time
'''
def testEndSession(app, client, auth):
    deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    willId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')
    gregId = uuid.UUID('693d350f-9cd0-4812-83c4-f1a98a8100ff')

    auth.login()
    with app.app_context():
        authMember = getByMemberIdAuth(deanId)
        token = generateToken(authMember.memberId)
        client.set_cookie(app, 'hhub-token', str(token))

    # case 1
    response = client.post('/api/session/28cf2179-0000-0000-a14c-3c09bd904365/end')
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "session does not exist" in jsonResponse['message']

    # Greg and Will join a session
    sessionId = None
    with app.app_context():
        joinOrAttemptMatch(gregId)
        sessionId = Session.query.first().sessionId

    # case 2 (Dean tries ending the session Greg and Will are in)
    response = client.post('/api/session/' + str(sessionId) + '/end')
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "you are not in this session" in jsonResponse['message']
