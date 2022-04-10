import json
import uuid
import pytest
from app.db.db import db
from app.db.models.Layer import Layer
from app.db.models.Session import Session
from app.exceptions.BadRequestException import BadRequestException
from app.services.AuthService import generateToken, getByMemberId as getByMemberIdAuth
from app.services.LayerService import addOrEditLayer, deleteFile, deleteLayer, uploadFile, getAll as getAllLayers
from requests_toolbelt import MultipartEncoder
from werkzeug.utils import secure_filename

# one function to test all layer routes and services
def testLayerAll(app, client, auth):
    deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
    willId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')
    badId = uuid.UUID('28cf2179-0000-0000-0000-3c09bd904365')
    
    auth.login()
    with app.app_context():
        authMember = getByMemberIdAuth(deanId)
        token = generateToken(authMember.memberId)
        client.set_cookie(app, 'hhub-token', str(token))

    # setting up a new session first
    response = client.post('/api/queue')
    jsonResponse = json.loads(response.data.decode('utf-8'))
    sessionId = None
    with app.app_context():
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
    Service method tested: deleteLayer(), deleteFile()
    Cases to test:
    1. session is non-existent (catch BadRequestException)
    2. member ID is invalid (catch BadRequestException)
    3. deleting a layer that doesnt exist or is already deleted. check that {} is returned
    4. trying to delete a staged layer (no URL exists) (catch BadRequestException)
    5. normal case (bucket delete): delete a layer with a set bucket URL. check that URL is null
    6. normal case (layer delete): delete a layer completely. check that number of layers decreased by 1
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

    # case a2
    response = client.get('/api/session/' + sessionId + '/layers')
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert len(jsonResponse) == 1
    layer = jsonResponse[0]
    layerId = layer['layerId']
    assert layer['name'] == "layer1"
    assert layer['startTime'] == 0.5
    assert layer['duration'] == 5.2
    assert layer['fadeInDuration'] == 0.1
    assert layer['fadeOutDuration'] == 1.5
    assert layer['trimmedStartDuration'] == 0.5
    assert layer['trimmedEndDuration'] == 1.0
    assert layer['fileName'] == 'Drum3'
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
    partnerLayer = jsonResponse[1]
    assert partnerLayer['name'] == "layer2"
    assert partnerLayer['startTime'] == 4.5
    assert partnerLayer['y'] == 3.5

    # case b2
    partnerLayerId = partnerLayer['layerId']
    response = client.get('api/session/' + sessionId + '/layers/' + partnerLayerId)
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse is not None
    assert jsonResponse['layerId'] == partnerLayerId
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
        '/api/session/' + str(badId) + '/layers/' + layerId + '/upload',
        data=m,
        headers={"Content-Type": m.content_type}
    )
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "you cannot upload this file" in jsonResponse['message']

    # case d2
    with app.app_context():
        filename = secure_filename('file')
        layerFile = ('file', open('tests/sample.mp3', 'rb'))
        try:
            uploadFile(sessionId, layerId, badId, layerFile, filename, m.content_type)
        except BadRequestException as exc:
            assert "you cannot upload this file" in exc.message

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

    # case e1
    response = client.delete('api/session/' + str(badId) + '/layers/' + layerId)  # layer ID from case b2
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "cannot delete this layer" in jsonResponse['message']

    # case e2
    with app.app_context():
        try:
            deleteLayer(sessionId, layerId, badId)
        except BadRequestException as exc:
            assert "you cannot delete this layer" in exc.message

    # case e3
    response = client.delete('api/session/' + sessionId + '/layers/' + str(badId))
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse == {}

    # case e4
    layerId = None
    with app.app_context():
        record = addOrEditLayer(sessionId, deanId, newLayer)
        layerId = str(record.layerId)
        assert len(getAllLayers()) == 3
    response = client.delete('api/session/' + sessionId + '/layers/' + layerId + '/delete')
    assert response.status_code != 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert "layer has no url yet" in jsonResponse['message']

    # case e5
    layerWithUrlId = None
    with app.app_context():
        for layer in getAllLayers():
            if layer.bucketUrl is not None:
                layerWithUrlId = str(layer.layerId)
                break
    assert layerWithUrlId is not None
    response = client.delete('api/session/' + sessionId + '/layers/' + layerWithUrlId + '/delete')
    assert response.status_code == 200
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse['layerId'] == layerWithUrlId
    assert jsonResponse['bucketUrl'] is None

    # case c3
    response = client.get('api/session/' + sessionId + '/layers/' + layerId)
    currLayer = json.loads(response.data.decode('utf-8'))
    assert currLayer['name'] == "layer1"
    assert currLayer['startTime'] == 0.5
    assert currLayer['trimmedStartDuration'] == 0.5
    editedLayer = {
        "name": "new layer name",  # changed
        "startTime": 0.8,  # changed
        "duration": 5.2,
        "fadeInDuration": 0.1,
        "fadeOutDuration": 1.5,
        "trimmedStartDuration": 0.9,  # changed
        "trimmedEndDuration": 1.0,
        "fileName": "Drum3",
        "y": 0.0
    }
    response = client.post(
        '/api/session/' + sessionId + '/layers/' + layerId,
        data=json.dumps(editedLayer),
        headers={"Content-Type": "application/json"}
    )
    with app.app_context():
        numLayers = len(Layer.query.all())
        assert numLayers  == 3  # should still just have 3 layers
    jsonResponse = json.loads(response.data.decode('utf-8'))
    assert jsonResponse is not None
    assert jsonResponse['layerId'] == layerId
    assert jsonResponse['name'] == "new layer name"
    assert jsonResponse['startTime'] == 0.8
    assert jsonResponse['trimmedStartDuration'] == 0.9

    # case e6
    m = MultipartEncoder(fields={'file': ('file', open('tests/sample.mp3', 'rb'), 'audio/mpeg')})
    response = client.put(
        '/api/session/' + sessionId + '/layers/' + layerId + '/upload',   # layer ID from case b2
        data=m,
        headers={"Content-Type": m.content_type}
    )
    response = client.delete('api/session/' + sessionId + '/layers/' + layerId)
    assert response.status_code == 200
    with app.app_context():
        assert len(getAllLayers()) == 2
