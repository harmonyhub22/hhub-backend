from app.db.db import db
from app.db.models.Member import Member
from app.db.models.MemberFriend import MemberFriend
from app.db.models.Genre import Genre
from app.db.models.MemberFriendRequest import MemberFriendRequest
from app.db.models.Session import Session
from app.db.models.MatchingQueue import MatchingQueue
from app.db.models.Layer import Layer

def seed():
    s = db.session()

    member1 = Member('gcpetri@tamu.edu', 'Greg', 'Petri')
    member2 = Member('vi@tamu.edu', 'Vi', 'Truong')
    member3 = Member('will@tamu.edu', 'Will', 'Thomas')
    member4 = Member('dean@tamu.edu', 'Dean', 'Something')
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
    s.add(genre1)

    s.commit()

    # matching queues
    s.add(MatchingQueue(member2.memberId)) # vi joins the queue
    s.add(MatchingQueue(member3.memberId)) # will joins the queue

    # sessions
    session1 = Session(genre1.genreId, member1.memberId, member4.memberId) # greg and dean join a session
    s.add(session1)

    s.commit()

    # layers
    s.add(Layer(session1.sessionId, 0, 1, 'something.com')) 

    s.commit()
