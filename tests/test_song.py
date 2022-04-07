import json
import pytest
from app.db.db import db
import uuid
from app.db.models.Session import Session
from app.exceptions.BadRequestException import BadRequestException
from app.services.AuthService import generateToken, getByMemberId as getByMemberIdAuth
from app.services.SessionService import getByMemberId as getByMemberIdSession, getLiveSession
from requests_toolbelt import MultipartEncoder
from werkzeug.utils import secure_filename

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
    1. valid song is added (check if number of songs increased by one and check metadata)
    2. invalid session ID (error is thrown)
    '''
    
    '''
    Route b: api/songs/<sessionID>/upload
    CRUD operation: PUT
    Service method tested: putSong(), uploadSong()
    Cases to test:
    1. session is non-existent (catch BadRequestException)
    2. member ID is invalid (catch BadRequestException)    
    3. normal case: song file is provided, for a new song
    '''

    '''
    Route c: api/songs/<songID>
    CRUD operation: GET
    Service method tested: getById()
    Cases to test:
    1. getting a song which is not yet created, in which case queryset is empty
    2. for a song which is created, queryset should have 1 song. check metadata
    3. just checking link for some reason
    '''

    '''
    Route d: api/songs?name=<songName>
    CRUD operation: GET
    Service method tested: getByName()
    Cases to test:
    1. getting a song which is not yet created, in which case queryset is empty
    2. trying to get a song with an invalid name (name != 'My New Song')
    3. for a song which is created, queryset should have 1 song, if the name is correct. check matadata
    '''

    '''
    Route e: api/songs/<songID>
    CRUD operation: GET
    Service method tested: getBySessionId()
    Cases to test:
    1. getting a song for a session with no song yet created should return an empty queryset
    2. 1 session is occuring, with a song made. ensure that the queryset returns just 1 song with proper metadata
    3. 2 sessions are occuring, each with different songs. ensure that the queryset returns just 1 song still. also
        make sure that each song corresponds to the proper session
    '''

    '''
    Route f: api/songs
    CRUD operation: GET
    Service method tested: getAll()
    Cases to test:
    1. no songs are created at all, so queryset is empty
    2. one song is created, so queryset has 1 song
    3. another song is created, so queryset has 2 songs
    '''

    '''
    Route g: api/songs/<songID>
    CRUD operation: DELETE
    Service method tested: deleteSong()
    Cases to test:
    1. deleting a song where there arent any (catch ServerErrorException)
    2. trying to delete a song that belongs to a session that you are/were not in (catch UnauthorizedException)
    3. normal case: delete a song that you have the rights to. queryset size should decrease by 1 and remove the right layer
    '''

     # case c1
    response = client.get('api/songs/' + str(badId))
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse == []


