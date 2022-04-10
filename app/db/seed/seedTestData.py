import uuid
from app.db.db import db
from app.db.models.Auth import Auth
from app.db.models.Member import Member
from app.db.models.Session import Session
from app.db.models.MatchingQueue import MatchingQueue
from app.db.models.Layer import Layer
from app.db.models.Song import Song
from  werkzeug.security import generate_password_hash, check_password_hash
from app.services.MemberService import getAll as getAllMembers
from app.services.MatchingQueueService import getAll as getAllQueue
from app.services.SessionService import getAll as getAllSessions
from app.services.LayerService import getAll as getAllLayers
from app.services.SongService import getAll as getAllSongs
from app.db.models.Auth import Auth

def seedTest():
    s = db.session()

    layers = getAllLayers()
    for l in layers:
        s.delete(l)
    s.commit()

    queues = getAllQueue()
    for q in queues:
        s.delete(q)
    s.commit()

    sessions = getAllSessions()
    for ss in sessions:
        s.delete(ss)
    s.commit()

    auths = Auth.query.all()
    for a in auths:
        s.delete(a)
    s.commit

    members = getAllMembers()
    for m in members:
        s.delete(m)
    s.commit()

    songs = getAllSongs()
    for s in songs:
        s.delete(s)
    s.commit()

    member1 = Member('gcpetri@tamu.edu', 'Greg', 'Petri')
    member2 = Member('vitruong00@tamu.edu', 'Vi', 'Truong')
    member3 = Member('will@tamu.edu', 'Will', 'Thomas')
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

    s.add(MatchingQueue(member3.memberId)) # will joins the queue
    s.commit()
