import pytest
from app.db.db import db
from app.db.models.MatchingQueue import MatchingQueue

'''
Route: api/queue
REST operation: POST
Service methods tested: joinOrAttemptMatch(), match(), createSession(), getTop(), getByMemberId()
Cases to test:
1. join the queue for the first time, so get added to it, queue queryset has now 1 member
2. join the queue again as the same user, so dont get added, and receive existing queue record
3. have a 2nd user join the queue, so match with the 1st user. check for new Session record, removal of 1st user from the queue, and None is returned
'''
def testJoinQueue(app, client, auth):
    pass

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