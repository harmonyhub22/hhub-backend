import json
import pytest
from sqlalchemy import join
from app.db.db import db
import uuid
from app.db.models.Session import Session
from app.exceptions.BadRequestException import BadRequestException
from app.services.AuthService import generateToken, getByMemberId as getByMemberIdAuth
from app.services.SessionService import getById as getByIdSession, getAll as getAllSessions, getByMemberId as getSessionByMemberId
from app.services.SongService import addSong, getAll as getAllSongs, getBySessionId
from requests_toolbelt import MultipartEncoder
from werkzeug.utils import secure_filename
from app.services.SongService import uploadSong
from app.services.MatchingQueueService import joinOrAttemptMatch

# one function to test all song routes and services
def testSongAll(app, client, auth):
    deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    willId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')
    badId = uuid.UUID('28cf2179-0000-0000-0000-3c09bd904365')

    auth.login()
    with app.app_context():
        authMember = getByMemberIdAuth(deanId)
        token = generateToken(authMember.memberId)
        client.set_cookie(app, 'hhub-token', str(token))

    # setting up a new session first
    sessionId = None
    with app.app_context():
        response = client.post('/api/queue')
        sessionId = str(Session.query.first().sessionId)
        
    '''
    Route a: api/songs/<sessionID>
    CRUD operation: POST
    Service method tested: addOrEditLayer()
    Cases to test:
    1. song name not given (catch BadRequestException)  (done)
    2. duration not given (catch BadRequestException)  (done)
    3. valid song is added (check if number of songs increased by one and check metadata)  (done)
    4. invalid session ID (error is thrown)  (done)

    Route b: api/songs/<sessionID>/upload
    CRUD operation: PUT
    Service method tested: putSong(), uploadSong()
    Cases to test:
    1. session is non-existent (catch BadRequestException)  (done)
    2. member ID is invalid (catch BadRequestException)    (done)
    3. normal case: song file is provided, for a new song  (done)
 
    Route c: api/songs/<songID>
    CRUD operation: GET
    Service method tested: getById()
    Cases to test:
    1. getting a song which is not yet created, in which case queryset is empty  (done)
    2. for a song which is created, queryset should have 1 song. check metadata  (done)

    Route d: api/songs?name=<songName>
    CRUD operation: GET
    Service method tested: getByName()
    Cases to test:
    1. trying to get a song with an invalid name (name != 'My New Song'). so queryset is empty  (done)
    2. for a song which is created, queryset should have 1 song, if the name is correct. check matadata  (done)

    Route e: api/songs?session=<sessionID>
    CRUD operation: GET
    Service method tested: getBySessionId()
    Cases to test:
    1. getting a song for a session with a song created should return a song  (done)
    2. getting a song for a session with no song yet created should return an empty queryset  (done)

    Route f: api/songs
    CRUD operation: GET
    Service method tested: getAll()
    Cases to test:
    1. no songs are created at all, so queryset is empty  (done)
    2. one song is created, so queryset has 1 song  (done)
    3. another song is created, so queryset has 2 songs  (done)

    Route g: api/songs/<songID>
    CRUD operation: DELETE
    Service method tested: deleteSong()
    Cases to test:
    1. deleting a song where there arent any (catch ServerErrorException)
    2. trying to delete a song that belongs to a session that you are/were not in (catch UnauthorizedException)
    3. normal case: delete a song that you have the rights to. queryset size should decrease by 1 and remove the right layer
    '''

    # case f1
    response = client.get('api/songs')
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert len(jsonResponse) == 0

    # case g1
    response = client.delete('api/songs/' + str(badId))
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "no song found" in jsonResponse['message']

    # case c1
    response = client.get('api/songs/' + str(badId))
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse == None

    # case a1
    body = {
        'duration': 7,
    }
    response = client.post(
        'api/songs/' + sessionId,
        data=json.dumps(body),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "song name or duration not provided" in jsonResponse['message']

    # case a2
    body = {
        'name': 'new song!',
    }
    response = client.post(
        'api/songs/' + sessionId,
        data=json.dumps(body),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "song name or duration not provided" in jsonResponse['message']

    # case a3
    body = {
        'name': 'new song!',
        'duration': 7,
    }
    response = client.post(
        'api/songs/' + sessionId,
        data=json.dumps(body),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    song = json.loads(response.data.decode('utf-8'))
    assert song['name'] == 'new song!'
    assert song['duration'] == 7
    assert song['session']['sessionId'] == sessionId
    assert song['session']['member1']['memberId'] == str(deanId)
    assert song['session']['member2']['memberId'] == str(willId)
    with app.app_context():
        query = getAllSongs()
        assert len(query) == 1

    # case a4
    response = client.post(
        'api/songs/' + str(badId),
        data=json.dumps(body),
        headers={"Content-Type": "application/json"}
    )
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "session does not exist" in jsonResponse['message']

    # case b1
    m = MultipartEncoder(fields={'file': ('file', open('tests/song.mp3', 'rb'), 'audio/mpeg')})
    response = client.put(
        'api/songs/' + str(badId) + '/upload',
        data=m,
        headers={"Content-Type": m.content_type}
    )
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "you cannot upload this file" in jsonResponse['message']

    # case b2
    with app.app_context():
        filename = secure_filename('file')
        songFile = ('file', open('tests/song.mp3', 'rb'))
        try:
            uploadSong(sessionId, badId, songFile, filename, 'audio/mpeg')
        except BadRequestException as exc:
            assert "you cannot upload this file" in exc.message

    # case b3
    with app.app_context():
        session = getByIdSession(sessionId)
    assert session.bucketUrl == None
    m = MultipartEncoder(fields={'file': ('file', open('tests/song.mp3', 'rb'), 'audio/mpeg')})
    response = client.put(
        'api/songs/' + sessionId + '/upload',
        data=m,
        headers={"Content-Type": m.content_type}
    )
    assert response.status_code == 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    with app.app_context():
        session = getByIdSession(sessionId)
    assert session.bucketUrl != None

    # case f2
    response = client.get('api/songs')
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert len(jsonResponse) == 1
    songId = jsonResponse[0]['songId']
    
    # case c2
    response = client.get('api/songs/' + songId)
    assert response is not None
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse['songId'] == songId
    songName = jsonResponse['name']

    # case d1
    response = client.get('api/songs?name=' + 'badname')
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse == []
    
    # case d2
    response = client.get('api/songs?name=' + songName)
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert len(jsonResponse) == 1
    assert jsonResponse[0]['name'] == songName

    # case e1
    response = client.get('api/songs?session=' + sessionId)
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert len(jsonResponse) == 1
    assert jsonResponse[0]['name'] == songName

    # case e2
    # first make a 2nd session with greg and vi
    gregId = uuid.UUID('693d350f-9cd0-4812-83c4-f1a98a8100ff')
    viId = uuid.UUID('0dfedda5-ddd3-481f-90d9-6ee388c4093e')
    song2id = None
    with app.app_context():
        songs = getAllSongs()
        assert len(songs) == 1
        joinOrAttemptMatch(gregId)
        joinOrAttemptMatch(viId)
        songs = getAllSongs()
        assert len(songs) == 1
        currSong = getBySessionId(viId)
        assert currSong == None
    
        # create new song with this session
        session2Id = getSessionByMemberId(gregId).sessionId
        body = {
            'name': 'another new song!',
            'duration': 10,
        }
        newSong = addSong(session2Id, gregId, body)
        song2id = str(newSong.songId)
    
    # case f3
    response = client.get('api/songs')
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert len(jsonResponse) == 2

    # case g2
    response = client.delete('api/songs/' + song2id)
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "you cannot delete this song" in jsonResponse['message']

    # case g3
    response = client.delete('api/songs/' + songId)
    assert response.status_code == 200
    deletedSong = json.loads(response.data.decode('utf-8'))
    assert deletedSong['session']['bucketUrl'] == None
    with app.app_context():
        query = getAllSongs()
        assert len(query) == 1