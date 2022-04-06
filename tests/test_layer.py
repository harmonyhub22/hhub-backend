import json
import uuid
import pytest
from urllib3 import encode_multipart_formdata
from app.db.db import db
from app.db.models.Layer import Layer
from app.db.models.Session import Session
from app.exceptions.BadRequestException import BadRequestException
from app.services.AuthService import generateToken, getByMemberId as getByMemberIdAuth
from app.services.LayerService import addOrEditLayer, uploadFile
from requests_toolbelt import MultipartEncoder
from werkzeug.utils import secure_filename

# one function to test all layer routes and services
def testGetLayerById(app, client, auth):
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
    Route a: api/session/<sessionID>/layers
    CRUD operation: GET
    Service method tested: getAllBySessionId()
    Cases to test:
    1. if the there are no layers in the session, the request should return an empty queryset
    2. if a user commits 1 layer, the queryset should now have 1 layer. check metadata
    3. if the partner commits another layer, the queryset should now have 2 layers. check metadata of 2nd layer

    Route b: api/session/<sessionID>/layers/<layerID>
    CRUD operation: GET
    Service method tested: getById()
    Cases to test:
    1. if the layer does not exist, the result should be None
    2. if the layer does exist, the result should be non-None (a layer with a matching ID). check metadata

    Route c: api/sessions/<sessionID>/layers
    CRUD operation: POST
    Service method tested: addOrEditLayer()
    Cases to test:
    1. valid layer is added (check if number of layers increased by one and check metadata)
    2. invalid session ID (error is thrown)
    3. edit a layer normally. check metadata
    
    Route d: api/sessions/<sessionID>/layers/<layerID>/upload
    CRUD operation: PUT
    Service method tested: uploadFile()
    Cases to test:
    1. session is non-existent (catch BadRequestException)
    2. member ID is invalid (catch BadRequestException)
    3. layer doesnt exist (catch BadRequestException)
    4. normal case: layer file is provided, for a new layer

    Route e: api/session/<sessionID>/layers/<layerID>
    CRUD operation: DELETE
    Service method tested: deleteLayer()
    Cases to test:
    1. 

    Route f: api/session/<sessionID>/layers/<layerID>/delete
    CRUD operation: DELETE
    Service method tested: deleteFile()
    Cases to test:
    1. session is non-existent (catch BadRequestException)
    2. member ID is invalid (catch BadRequestException)
    3. invalid layer ID (catch BadRequestException)
    4. trying to delete a staged layer (no URL exists) (catch BadRequestException)
    5. normal case: delete a layer with a set bucket URL. check that URL is null
    '''

    # case a1
    response = client.get('/api/session/' + sessionId + '/layers')
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse == []

    # case b1
    response = client.get('/api/session/' + sessionId + '/layers/' + str(badId))
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse == None

    # case c1
    # the equivalent of JSON.stringify in JavaScript
    with app.app_context():
        query = Layer.query.all()
        assert len(query) == 0
    newLayer = {
        "name": "layer1",
        "startTime": 0.5,
        "duration": 5.2,
        "fadeInDuration": 0.1,
        "fadeOutDuration": 1.5,
        "reversed": False,
        "trimmedStartDuration": 0.5,
        "trimmedEndDuration": 1.0,
        "fileName": "Drum3",
        "y": 0.0
    }
    response = client.post(
        '/api/session/' + sessionId + '/layers',
        data=json.dumps(newLayer),
        headers={"Content-Type": "application/json"}
    )
    jsonResponse = json.loads(response.data.decode('utf-8'))

    # case a2
    response = client.get('/api/session/' + sessionId + '/layers')
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert len(jsonResponse) == 1
    layer = jsonResponse[0]
    assert layer['name'] == "layer1"
    assert layer['startTime'] == 0.5
    assert layer['y'] == 0.0

    # case c2
    response = client.post(
        '/api/session/' + str(badId) + '/layers',
        data=json.dumps(newLayer),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "session not found" in jsonResponse['message']

    # case a3
    partnerLayer = {
        "name": "layer2",
        "startTime": 4.5,
        "duration": 9.5,
        "fadeInDuration": 0.5,
        "fadeOutDuration": 0.8,
        "reversed": False,
        "trimmedStartDuration": 0.0,
        "trimmedEndDuration": 0.0,
        "fileName": "Piano1",
        "y": 3.5
    }
    with app.app_context():
        addOrEditLayer(sessionId, willId, partnerLayer)
    response = client.get('/api/session/' + sessionId + '/layers')
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert len(jsonResponse) == 2
    layer = jsonResponse[1]
    assert layer['name'] == "layer2"
    assert layer['startTime'] == 4.5
    assert layer['y'] == 3.5

    # case b2
    layerId = layer['layerId']
    response = client.get('api/session/' + sessionId + '/layers/' + layerId)
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse is not None
    assert jsonResponse['layerId'] == layerId
    assert jsonResponse['name'] == "layer2"
    assert jsonResponse['startTime'] == 4.5
    assert jsonResponse['y'] == 3.5

    # case b1
    response = client.get('api/session/' + sessionId + '/layers/' + str(badId))
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse == None

    m = MultipartEncoder(fields={'file': ('file', open('tests/sample.mp3', 'rb'), 'audio/mpeg')})

    # case d1
    response = client.put(
        '/api/session/' + str(badId) +'/layers/' + layerId + '/upload',
        data=m,
        headers={"Content-Type": m.content_type}
    )
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "cannot edit this layer" in jsonResponse['message']

    # case d2
    with app.app_context():
        filename = secure_filename('file')
        layerFile = ('file', open('tests/sample.mp3', 'rb'))
        try:
            uploadFile(sessionId, layerId, badId, layerFile, filename, m.content_type)
            assert False
        except BadRequestException as exc:
            assert True

    # case d3
    m = MultipartEncoder(fields={'file': ('file', open('tests/sample.mp3', 'rb'), 'audio/mpeg')})
    response = client.put(
        '/api/session/' + sessionId + '/layers/' + str(badId) + '/upload',
        data=m,
        headers={"Content-Type": m.content_type}
    )
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "layer with this id does not exist" in jsonResponse['message']

    # case d4
    m = MultipartEncoder(fields={'file': ('file', open('tests/sample.mp3', 'rb'), 'audio/mpeg')})
    response = client.put(
        '/api/session/' + sessionId + '/layers/' + layerId + '/upload',   # layer ID from case b2
        data=m,
        headers={"Content-Type": m.content_type}
    )
    assert response.status_code == 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse['bucketUrl'] != None
    url = jsonResponse['bucketUrl']

    # case e1
    # case e2
    # case e3
    # case e4
    # case e5