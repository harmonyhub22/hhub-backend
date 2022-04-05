# from base64 import b64encode
# import datetime
# from http import HTTPStatus
# import json
# import pytest
# from app.db.db import db
# from app.db.models.MatchingQueue import MatchingQueue
# from app.db.models.Session import Session
# from app.exceptions.BadRequestException import BadRequestException
# from app.services.AuthService import generateToken
# from app.services.MemberService import setSid
# from app.services.SessionService import getByMemberId as getByMemberIdSession
# from app.services.AuthService import getByMemberId as getByMemberIdAuth
# import uuid

# '''
# Route: api/queue
# REST operation: POST
# Service methods tested: joinOrAttemptMatch(), match(), createSession(), getTop(), getByMemberId()
# Cases to test:
# 1. have a 2nd user join the queue, so match with the 1st user. check for new Session record, removal of 1st user from the queue, and None is returned
# 2. already in a live session (catch BadRequestException)
# 3. join the queue for the first time, so get added to it, queue queryset has now 1 member
# 4. join the queue again as the same user, so dont get added, and receive existing queue record
# '''
# def testJoinQueue(app, client, auth):
#     deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
#     willId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')

#     auth.login()
#     with app.app_context():
#         authMember = getByMemberIdAuth(deanId)
#         token = generateToken(authMember.memberId)
#         client.set_cookie(app, 'hhub-token', str(token))
#         #setSid(deanId, '123')  # uncomment this if we are also testing web sockets

#     # initial checking (Will is in the queue (from seed data))
#     with app.app_context():
#         query = MatchingQueue.query.all()
#         numWaiting = len(query)
#         assert numWaiting == 1
#         assert query[0].memberId == willId

#     # case 1
#     response = client.post('/api/queue')
#     assert response is not None
#     with app.app_context():
#         query = MatchingQueue.query.all()
#         numWaiting = len(query)
#         assert numWaiting == 0

#     # case 2
#     response = client.post('/api/queue')
#     assert response.status_code != 200
#     jsonResponse = json.loads(response.data.decode('utf-8'))
#     assert "currently in a session" in jsonResponse['message']
    
#     # end the session before cases 3 and 4
#     with app.app_context():
#         session = getByMemberIdSession(deanId)
#         session.endTime = datetime.datetime.utcnow()
#         db.session.commit()
    
#     # case 3 
#     response = client.post('/api/queue')
#     with app.app_context():
#         query = MatchingQueue.query.all()
#         numWaiting = len(query)
#         assert numWaiting == 1
#         jsonResponse = json.loads(response.data.decode('utf-8'))
#         assert jsonResponse['member']['memberId'] == '28cf2179-74ed-4fab-a14c-3c09bd904365'

#     # case 4
#     response = client.post('/api/queue')
#     with app.app_context():
#         query = MatchingQueue.query.all()
#         numWaiting = len(query)
#         assert numWaiting == 1
#         assert query[0].memberId == deanId

# '''
# Route: api/queue
# REST operation: DELETE
# Service methods tested: leave(), getByMemberId()
# Cases to test:
# 1. normal case: join the queue (as the first one), then leave. check that queryset is empty
# 2. trying to leave a queue that you havent joined (nothing happens, just check that queryset is same size)
# '''
# def testLeaveQueue(app, client, auth):
#     deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')

#     auth.login()
#     with app.app_context():
#         authMember = getByMemberIdAuth(deanId)
#         token = generateToken(authMember.memberId)
#         client.set_cookie(app, 'hhub-token', str(token))
    
#     # case 1
#     response = client.post('/api/queue')
#     response = client.delete('/api/queue')
#     assert response.status_code == HTTPStatus.NO_CONTENT
#     with app.app_context():
#         query = MatchingQueue.query.all()
#         assert len(query) == 0

#     # case 2
#     response = client.delete('/api/queue')
#     with app.app_context():
#         query = MatchingQueue.query.all()
#         assert len(query) == 0