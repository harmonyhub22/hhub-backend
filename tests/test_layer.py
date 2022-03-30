import pytest
from app.services.LayerService import *

def testGetLayers(client, auth):
    auth.login()
    response = client.get('/api/session/b52d3f89-b5a6-43e9-b352-4161a273e659/layers')
    # some assert statement here about the retrieved layers

def testAddLayer(client, auth):
    pass

def testEditLayer(client, auth):
    pass

def testDeleteLayer(client, auth):
    pass