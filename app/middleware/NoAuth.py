
from flask import request
from app.exceptions.UnauthorizedException import UnauthorizedException


def getCookie():
    memberId = request.cookies.get('memberId')
    if request.path == '/api/login':
        if memberId != None:
            request.environ['HTTP_MEMBERID'] = memberId
        return
    if memberId == None or len(memberId) < 36:
        raise UnauthorizedException('no memberId cookie found')
    request.environ['HTTP_MEMBERID'] = memberId
