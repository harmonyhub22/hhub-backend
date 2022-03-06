import uuid
from app.db.db import db
from app.db.models.Member import Member
from app.db.models.MemberFriend import MemberFriend
from app.db.models.Genre import Genre
from app.db.models.MemberFriendRequest import MemberFriendRequest
from app.db.models.Session import Session
from app.db.models.MatchingQueue import MatchingQueue
from app.db.models.Layer import Layer
from app.db.models.Song import Song

def seed():
    s = db.session()

    if len(Member.query.filter(Member.email=='gcpetri@tamu.edu').all()) == 1: # seed data is already present
        return
    print('inserting seed data')

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

    # add friend requests
    s.add(MemberFriendRequest(member2.memberId, member1.memberId)) # vi requests greg

    # add friends
    s.add(MemberFriend(member1.memberId, member3.memberId)) # vi and will are friends

    # add genres
    genre1 = Genre('Alt')
    genre2 = Genre('Country')
    genre3 = Genre('R&B')
    genre4 = Genre('Jazz')
    genre5 = Genre('Indie')
    genre6 = Genre('Pop')
    genre1.genreId = uuid.UUID('dff3c144-eb29-41d3-82ea-9bcd200fc891')
    s.add(genre1)
    s.add(genre2)
    s.add(genre3)
    s.add(genre4)
    s.add(genre5)
    s.add(genre6)

    s.commit()

    # matching queues
    queue1 = MatchingQueue(member2.memberId)
    queue1.matchingQueueId = '1c74a6fd-b7b9-4fe4-96fd-f7e78eb6d2c2'
    s.add(queue1) # vi joins the queue
    #s.add(MatchingQueue(member3.memberId)) # will joins the queue

    # sessions
    # session1 = Session(genre1.genreId, member1.memberId, member4.memberId) # greg and dean join a session
    # session1.sessionId = 'b52d3f89-b5a6-43e9-b352-4161a273e659'
    # s.add(session1)

    s.commit()

    # layers
    layer1 = Layer(session1.sessionId, member1.memberId, 0, 0, 1, 'something.com')
    layer1.layerId = '650c0a24-5aab-4c79-990a-61493cd146dc'
    s.add(layer1)

    s.commit()

    # songs
    song1 = Song(session1.sessionId, 'Some song', 60, 'something.com', 120)
    song1.songId = 'e165e9e0-6a54-4bd9-9d78-0008d49f04d0'
    s.add(song1)

    s.commit()
