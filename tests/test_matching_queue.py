from base64 import b64encode
import datetime
import pytest
from app.db.db import db
from app.db.models.MatchingQueue import MatchingQueue
from app.exceptions.BadRequestException import BadRequestException
from app.services.AuthService import generateToken
from app.services.SessionService import getByMemberId as getByMemberIdSession
from app.services.AuthService import getByMemberId as getByMemberIdAuth
import uuid

'''
Route: api/queue
REST operation: POST
Service methods tested: joinOrAttemptMatch(), match(), createSession(), getTop(), getByMemberId()
Cases to test:
1. have a 2nd user join the queue, so match with the 1st user. check for new Session record, removal of 1st user from the queue, and None is returned
2. already in a live session (catch BadRequestException)
3. join the queue for the first time, so get added to it, queue queryset has now 1 member
4. join the queue again as the same user, so dont get added, and receive existing queue record
'''
#@pytest.mark.order(1)
def testJoinQueue(app, client, auth):
    res = auth.login()

    deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    willId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')

    with app.app_context():
        authMember = getByMemberIdAuth(deanId)
        print(authMember)
        token = generateToken(authMember.memberId)
        print(token)
        client.set_cookie(app, 'hhub-token', str(token))

    # cookie = next(
    #     (cookie for cookie in client.cookie_jar if cookie.name == "hhub-token"),
    #     None
    # )
    # print("DEBUG: cookie is", cookie)
    # assert cookie is not None


    # initial checking (Will is in the queue (from seed data))
    with app.app_context():
        query = MatchingQueue.query.all()
        numWaiting = len(query)
        assert numWaiting == 1
        assert query[0].memberId == willId

    # case 1
    #credentials = b64encode(b"dean27@tamu.edu:password").decode('utf-8')
    #response = client.post('/api/queue', headers={"Authorization": "Basic {}".format(credentials)}, data={'MEMBERID': deanId})
    response = client.post('/api/queue')
    assert response == None
    with app.app_context():
        query = MatchingQueue.query.all()
        numWaiting = len(query)
        assert numWaiting == 0

    # case 2
    with pytest.raises(BadRequestException) as excinfo:
        existingRecord = client.post('/api/queue', data={
            'MEMBERID': deanId
        })
    assert "currently in a session" in str(excinfo.value)
    
    # end the session before cases 3 and 4
    with app.app_context():
        session = getByMemberIdSession(deanId)
        session.endTime = datetime.datetime.utcnow()
        db.session.commit()
    
    # case 3 
    newRecord = client.post('/api/queue', data={
        'MEMBERID': deanId
    })
    with app.app_context():
        query = MatchingQueue.query.all()
        numWaiting = len(query)
        assert numWaiting == 1
        assert newRecord.memberId == deanId

    # case 4
    existingRecord = client.post('/api/queue', data={
        'MEMBERID': deanId
    })
    with app.app_context():
        query = MatchingQueue.query.all()
        numWaiting = len(query)
        assert numWaiting == 1
        assert query[0].memberId == deanId

'''
Route: api/queue
REST operation: DELETE
Service methods tested: leave(), getByMemberId()
Cases to test:
1. trying to leave a queue that you havent joined (nothing happens, just check that queryset is same size)
2. normal case: join the queue (as the first one), then leave. check that queryset is empty
'''
def testLeaveQueue(app, client, auth):
    pass
    # auth.login()
    # response = client.delete('/api/queue/28cf2179-74ed-4fab-a14c-3c09bd904365')