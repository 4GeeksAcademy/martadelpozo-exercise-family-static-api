"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json()
    print(body)
    print(body["first_name"])
    member={
        "first_name": body["first_name"],
		"age": body["age"],
		"lucky_numbers": body["lucky_numbers"],
        "id": body["id"]
    }

    new_member = jackson_family.add_member(member)
    response_body = {
        "msg": "you added a member",
        "member": "new_member"
    }

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
         return jsonify({
            "first_name": member["first_name"],
            "id": member["id"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }), 200
    else:
        return jsonify({"error": "Member not found"}), 404
    

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted_member = jackson_family.delete_member(member_id)
    if deleted_member:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
