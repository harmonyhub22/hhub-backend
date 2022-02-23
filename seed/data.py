import uuid

from app import db
from models.User import User
from models.UserFriend import UserFriend
from models.Genre import Genre
from models.UserFriendRequest import UserFriendRequest
from models.Session import Session
from models.MatchingQueue import MatchingQueue
from models.Layer import Layer

def seed():
    s = db.session()

    user1 = User('gcpetri@tamu.edu', 'Greg', 'Petri')
    user2 = User('vi@tamu.edu', 'Vi', 'Truong')
    user3 = User('will@tamu.edu', 'Will', 'Thomas')
    user4 = User('dean@tamu.edu', 'Dean', 'Something')
    s.add(user1)
    s.add(user2)
    s.add(user3)
    s.add(user4)

    s.commit()

    # add friend requests
    s.add(UserFriendRequest(user2.userId, user1.userId)) # vi requests greg

    # add friends
    s.add(UserFriend(user1.userId, user3.userId)) # vi and will are friends

    # add genres
    genre1 = Genre('Alt')
    s.add(genre1)

    s.commit()

    # matching queues
    s.add(MatchingQueue(user2.userId)) # vi joins the queue
    s.add(MatchingQueue(user3.userId)) # will joins the queue

    # sessions
    session1 = Session(genre1.genreId, user1.userId, user4.userId) # greg and dean join a session
    s.add(session1)

    s.commit()

    # layers
    s.add(Layer(session1.sessionId, 0, 1, 'something.com')) 

    s.commit()
