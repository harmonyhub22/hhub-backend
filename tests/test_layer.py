# import json
# import uuid
# import pytest
# from app.db.db import db
# from app.db.models.Layer import Layer
# from app.db.models.Session import Session
# from app.services.AuthService import generateToken, getByMemberId as getByMemberIdAuth

# # one function to test all layer routes and services
# def testGetLayerById(app, client, auth):
#     deanId = uuid.UUID('28cf2179-74ed-4fab-a14c-3c09bd904365')
#     willId = uuid.UUID('73f80e58-bc0e-4d35-b0d8-d711a26299ac')
    
#     auth.login()
#     with app.app_context():
#         authMember = getByMemberIdAuth(deanId)
#         token = generateToken(authMember.memberId)
#         client.set_cookie(app, 'hhub-token', str(token))

#     # setting up a new session first
#     sessionId = None
#     with app.app_context():
#         response = client.post('/api/queue')
#         sessionId = str(Session.query.first().sessionId)

#     '''
#     Route a: api/session/<sessionID>/layers
#     CRUD operation: GET
#     Service method tested: getAllBySessionId()
#     Cases to test:
#     1. if the there are no layers in the session, the request should return an empty queryset
#     2. if a user commits 1 layer, the queryset should now have 1 layer. check metadata
#     3. if the partner commits another layer, the queryset should now have 2 layers. check metadata of 2nd layer

#     Route b: api/session/<sessionID>/layers/<layerID>
#     CRUD operation: GET
#     Service method tested: getById()
#     Cases to test:
#     1. if the layer does not exist, the queryset should be empty
#     2. if the layer does exist, the query should return 1 result (a layer with a matching ID). check metadata

#     Route c: api/sessions/<sessionID>/layers
#     CRUD operation: POST
#     Service method tested: addOrEditLayer()
#     Cases to test:
#     1. valid layer is added (check if number of layers increased by one and check metadata)
#     2. invalid session ID (error is thrown)
#     3. edit a layer normally. check metadata
    
#     Route d: api/sessions/<sessionID>/layers/<layerID>/upload
#     CRUD operation: PUT
#     Service method tested: uploadFile()

#     Route e: api/session/<sessionID>/layers/<layerID>
#     CRUD operation: DELETE
#     Service method tested: deleteLayer()

#     Route f: api/session/<sessionID>/layers/<layerID>/delete
#     CRUD operation: DELETE
#     Service method tested: deleteFile()
#     '''

#     # case a1
#     response = client.get('/api/session/' + sessionId + '/layers')
#     jsonResponse = json.loads(response.data.decode('utf-8'))
#     assert jsonResponse == []

#     # case b1
#     response = client.get('/api/session/' + sessionId + '/layers/28cf2179-0000-0000-0000-3c09bd904365')
#     jsonResponse = json.loads(response.data.decode('utf-8'))
#     assert jsonResponse == None

#     # case c1
#     # the equivalent of JSON.stringify in JavaScript
#     with app.app_context():
#         query = Layer.query.all()
#         assert len(query) == 0
#     newLayer = json.loads('{ "name": "layer1", "startTime": 0.5, "duration": 5.2, "fadeInDuration": 0.1, "fadeOutDuration": 1.5, "reversed": false, "trimmedStartDuration": 0.5, "trimmedEndDuration": 1.0, "fileName": "Drum3", "y": 0.0 }')
#     # TODO: solve this error: {'message': 'The browser (or proxy) sent a request that this server could not understand.'}
#     response = client.post('/api/session/' + sessionId + '/layers', data=newLayer)
#     jsonResponse = json.loads(response.data.decode('utf-8'))
#     assert jsonResponse == 1
#     with app.app_context():
#         query = Layer.query.all()
#         assert len(query) == 1

#     # case a2
