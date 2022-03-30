import pytest
from app.db.db import db
from app.services.LayerService import *

def testGetLayers(app, client, auth):
    auth.login()

    # starting with no committed layers, so do those tests first
    response = client.get('/api/session/b52d3f89-b5a6-43e9-b352-4161a273e659/layers')
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

def testAddLayer(client, auth):
    pass

def testEditLayer(client, auth):
    pass

def testDeleteLayer(client, auth):
    pass