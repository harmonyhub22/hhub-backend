from app.socket.init import sio
from app.services.MatchingQueueService import getAll
from app.services.SessionService import createSession

# web socket listener for when the user joins the queue
# sid = a random string idneitfying the socket connection (different for each client)
# environ = a dictionary with all the details from the client request (headers, cookies, query string args, etc.). used for authentication:
# username = authenticate_user(environ)
@sio.event
def connect(sid, environ):        
    print(sid, 'connected!')
    sio.emit('hello there')

    # if there are 2 users in the queue, create the session with them
    '''
    allQueuedUsers = getAll()
    if len(allQueuedUsers) >= 2:
        member1 = allQueuedUsers[0]
        member2 = allQueuedUsers[1]
        data = {
            'genreId': 'dff3c144-eb29-41d3-82ea-9bcd200fc891',  # default of Alt genre for now (change later)
            'memberId': member2
        }
        newSession = createSession(member1, data)
        sio.emit('session_made', { 'sessionId': newSession.sessionId })
    else:
        return
    '''

@sio.event
def myMessageInRoom(sid, data):
    sio.emit('reply from server', data, room='new_room')

@sio.event
def myMessage(sid, data):
    print('received this event')
    
# web socket listener for joining a session
@sio.event
def begin_chat(sid):
    sio.enter_room(sid, 'new_room')

# web socket listener for leaving a session
@sio.event
def exit_chat(sid):
    sio.leave_room(sid, 'new_room')

@sio.event
def disconnect(sid):
    print(sid, 'disconnected')