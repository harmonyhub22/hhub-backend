
memberIdtoSid = dict()

def setSid(memberId, sid):
    memberIdtoSid.update(memberId, sid)

def getSid(memberId):
    return memberIdtoSid.get(memberId)

def getSids(member1Id, member2Id):
    return (memberIdtoSid.get(member1Id), memberIdtoSid.get(member2Id))

def popSid(memberId):
    return memberIdtoSid.pop(memberId)

def numMembers():
    return len(memberIdtoSid)

