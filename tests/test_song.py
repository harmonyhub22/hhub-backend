# import pytest
# from app.db.db import db
# from app.db.models.Song import Song

# '''
# Route: api/songs/<songID>
# CRUD operation: DELETE
# Service method tested: getById()
# Cases to test:
# 1. getting a song which is not yet created, in which case queryset is empty
# 2. for a song which is created, queryset should have 1 song. check metadata
# '''
# def testGetSongById(app, client, auth):
#     pass

# '''
# Route: api/songs?name=<songName>
# CRUD operation: GET
# Service method tested: getByName()
# Cases to test:
# 1. getting a song which is not yet created, in which case queryset is empty
# 2. trying to get a song with an invalid name (name != 'My New Song')
# 3. for a song which is created, queryset should have 1 song, if the name is correct. check matadata
# '''
# def testGetSongByName(app, client, auth):
#     pass

# '''
# Route: api/songs/<songID>
# CRUD operation: GET
# Service method tested: getBySessionId()
# Cases to test:
# 1. getting a song for a session with no song yet created should return an empty queryset
# 2. 1 session is occuring, with a song made. ensure that the queryset returns just 1 song with proper metadata
# 3. 2 sessions are occuring, each with different songs. ensure that the queryset returns just 1 song still. also
#     make sure that each song corresponds to the proper session
# '''
# def testGetSongBySessionId(app, client, auth):
#     pass

# '''
# Route: api/songs
# CRUD operation: GET
# Service method tested: getAll()
# Cases to test:
# 1. no songs are created at all, so queryset is empty
# 2. one song is created, so queryset has 1 song
# 3. another song is created, so queryset has 2 songs
# '''
# def testGetAllSongs(app, client, auth):
#     pass

# '''
# Route: api/songs/<songID>
# CRUD operation: DELETE
# Service method tested: deleteSong()
# Cases to test:
# 1. deleting a song where there arent any (catch ServerErrorException)
# 2. trying to delete a song that belongs to a session that you are/were not in (catch UnauthorizedException)
# 3. normal case: delete a song that you have the rights to. queryset size should decrease by 1 and remove the right layer
# '''
# def testDeleteSong(app, client, auth):
#     pass