from flask import Blueprint, jsonify

from app.db.models.Member import Member

member_controller_bp = Blueprint('member_controller', __name__)

@member_controller_bp.route("/", methods=['GET'])
def getMembers():
    members = Member.query.all()
    print(members)
    #return 200
    return jsonify(success=True)