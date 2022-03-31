import pytest
from app.db.db import db
from app.db.models.Layer import Layer

'''
route: api/session/<sessionID>/layers/<layerID>
REST operation: GET
service method tested: getById()
'''
def testGetLayerById():
    pass

'''
route: api/session/<sessionID>/layers
REST operation: GET
service method tested: getAllBySessionId()
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
            reversed=False,
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
route: api/sessions/<sessionID>/layers
REST operation: POST
service method tested: addOrEditLayer()
'''
def testAddLayer(client, auth):
    pass

'''
route: api/sessions/<sessionID>/layers/<layerID>
REST operation: POST
service method tested: addOrEditLayer()
'''
def testEditLayer(client, auth):
    pass

'''
route: api/sessions/<sessionID>/layers/<layerID>/upload
REST operation: PUT
service method tested: uploadFile()
'''
def testUploadLayer(client, auth):
    pass

'''
route: api/session/<sessionID>/layers/<layerID>
REST operation: DELETE
service method tested: deleteLayer()
'''
def testDeleteLayer(client, auth):
    pass