import pytest
from app.db.db import db
from app.db.models.Layer import Layer

'''
Route: api/session/<sessionID>/layers/<layerID>
CRUD operation: GET
Service method tested: getById()
Cases to test:
1. if the layer does not exist, the queryset should be empty
2. if the layer does exist, the query should return 1 result (a layer with a matching ID). check metadata
'''
def testGetLayerById(app, client, auth):
    pass

'''
Route: api/session/<sessionID>/layers
CRUD operation: GET
Service method tested: getAllBySessionId()
Cases to test:
1. if the there are no layers in the session, the request should return an empty queryset
2. if a user commits 1 layer, the queryset should now have 1 layer. check metadata
3. if the partner commits another layer, the queryset should now have 2 layers. check metadata of 2nd layer
'''
def testGetLayers(app, client, auth):
    auth.login()

    # starting with no committed layers, so do those tests first
    response = client.get('/api/session/b52d3f89-b5a6-43e9-b352-4161a273e659/layers')
    print(response)
    assert len(list(response)) == 0

    with app.app_context():
        s = db.session()
        
        # use session 1 id and member 1 id to create a new layer
        layer1 = Layer(
            'b52d3f89-b5a6-43e9-b352-4161a273e659',
            '693d350f-9cd0-4812-83c4-f1a98a8100ff',
            name='layer1',
            startTime=0.5,
            duration=5.2,
            fadeInDuration=0.1, 
            fadeOutDuration=1.5,
            isReversed=False,
            trimmedStartDuration=0.5,
            trimmedEndDuration=1.0,
            bucketUrl=None,
            fileName="Drum3",
            y=0.0
        )
        layer1.layerId = '650c0a24-5aab-4c79-990a-61493cd146dc'
        s.add(layer1)
        s.commit()

    response = client.get('/api/session/b52d3f89-b5a6-43e9-b352-4161a273e659/layers')
    assert len(list(response)) == 1

'''
Route: api/sessions/<sessionID>/layers
CRUD operation: POST
Service method tested: addOrEditLayer()
Cases to test:
1. valid layer is added (check if number of layers increased by one and check metadata)
2. invalid session ID (error is thrown)
3. other ways adding a layer can fail?
'''
def testAddLayer(app, client, auth):
    pass

'''
Route: api/sessions/<sessionID>/layers/<layerID>
CRUD operation: POST
Service method tested: addOrEditLayer()
Cases to test:
1. edit a 
'''
def testEditLayer(app, client, auth):
    pass

'''
Route: api/sessions/<sessionID>/layers/<layerID>/upload
CRUD operation: PUT
Service method tested: uploadFile()
'''
def testUploadLayer(app, client, auth):
    pass

'''
Route: api/session/<sessionID>/layers/<layerID>
CRUD operation: DELETE
Service method tested: deleteLayer()
Cases to test:

'''
def testDeleteLayer(app, client, auth):
    pass

'''
Route: api/session/<sessionID>/layers/<layerID>/delete
CRUD operation: DELETE
Service method tested: deleteFile()
Cases to test:

'''
def testDeleteLayerFile(app, client, auth):
    pass