import datetime
import os
import uuid
from app.db.db import db
from app.db.models.Auth import Auth
from app.db.models.Member import Member
from app.db.models.Session import Session
from app.db.models.MatchingQueue import MatchingQueue
from app.db.models.Layer import Layer
from app.db.models.Song import Song
from werkzeug.security import generate_password_hash, check_password_hash

def seed():
    s = db.session()

    if len(Member.query.filter(Member.email=='gcpetri@tamu.edu').all()) == 1: # seed data is already present
        return

    member1 = Member('gcpetri@tamu.edu', 'Greg', 'Petri')
    member2 = Member('vitruong00@tamu.edu', 'Vi', 'Truong', True)
    member3 = Member('will@tamu.edu', 'Will', 'Thomas', True)
    member4 = Member('dean27@tamu.edu', 'Dean', 'Something')
    member1.memberId = uuid.UUID('693d350f-9cd0-4812-83c4-f1a98a8100ff')
    member2.memberId = uuid.UUID('0dfedda5-ddd3-481f-90d9-6ee388c4093e')
    member3.memberId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')
    member4.memberId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')

    s.add(member1)
    s.add(member2)
    s.add(member3)
    s.add(member4)
    s.commit()

    hashedPwd = generate_password_hash('password')
    member1auth = Auth(member1.memberId, hashedPwd)
    member2auth = Auth(member2.memberId, hashedPwd)
    member3auth = Auth(member3.memberId, hashedPwd)
    member4auth = Auth(member4.memberId, hashedPwd)
    s.add(member1auth)
    s.add(member2auth)
    s.add(member3auth)
    s.add(member4auth)
    s.commit()

    # matching queues
    queue1 = MatchingQueue(member2.memberId)
    queue1.matchingQueueId = '1c74a6fd-b7b9-4fe4-96fd-f7e78eb6d2c2'
    s.add(queue1) # vi joins the queue
    #s.add(MatchingQueue(member3.memberId)) # will joins the queue

    # sessions
    #session1 = Session(member1.memberId, member4.memberId) # greg and dean join a session
    #session1.sessionId = 'b52d3f89-b5a6-43e9-b352-4161a273e659'
    # session1.endTime = datetime.datetime.utcnow()
    #s.add(session1)

    s.commit()

    # layers
    #layer1 = Layer(session1.sessionId, member1.memberId, name='layer1', startTime=0.5, duration=5.2, fadeInDuration=0.1, 
    #    fadeOutDuration=1.5, reversed=False, trimmedStartDuration=0.5, trimmedEndDuration=1.0, bucketUrl=None, fileName="Drum3", y=0.0)
    #layer1.layerId = '650c0a24-5aab-4c79-990a-61493cd146dc'
    #s.add(layer1)

    #s.commit()

    # songs
    #song1 = Song(sessionId=session1.sessionId, memberId=member1.memberId, name='Some song')
    #song1.songId = 'e165e9e0-6a54-4bd9-9d78-0008d49f04d0'
    # s.add(song1)
