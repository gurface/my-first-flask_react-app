# crud app - create, read, update, delete
# create
# - first_name
# - last_name
# - email

# requests have different types: GET (recieve), POST (create), PUT / PATCH (update), DELETE
# we also have json data, information that comes alongside the request, 
# also have responses from backend, status: 200 = success, 404 = error, 403 = forbidden
# can also respond with json

# example -

# Request
# type: DELETE
# json: {}

# Response
# status: 400
# json: {}

# we have made different @app.routes for different methods, e.g. deleting, updating, creating a contact

# this entire code is what you call an API 🤯🙀

from flask import request, jsonify
from config import app, db
from models import Contact

# GET method, only uses GET method for certain URL
@app.route("/contacts", methods=["GET"])
def get_contacts():
    # this uses flaskSQAlchemy, ORM, to get all of the different contacts that exist inside contact database
    contacts = Contact.query.all()
    # converts it to list by letting contact = x, making a dictionary from json
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    # makes it a python dictionary
    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
# makes sure the json data is valid
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    # if the values do not exist, user did not input it:
    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name and email"}),
            400, # did not work 400 = error
        )
    
    # creates the contact
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact) # adds the contact to the database
        db.session.commit() # permanently adds to the database from session
    except Exception as e: # if something goes wrong ->
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created!"}), 201 # if no errors occur

@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id) # finds user with the id

    if not contact: # if no user with the id exists:
        return jsonify({"message": "User not found"}), 404 # error
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name) # makes sure if the contact is updated and matches json data
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id) # finds user with the id

    if not contact: # if no user with the id exists:
        return jsonify({"message": "User not found"}), 404 # error
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200

# avoid from importing whole file
if __name__ == "__main__":
    # it creates all of the models
    with app.app_context():
        db.create_all()
    app.run(debug=True)