from flask import Flask, request, render_template, url_for
from flask_restful import abort, Api, Resource
from constants import *
from controller import ContactMgr

app = Flask(APP_NAME, template_folder=relative_path('static'))
api = Api(app)


def abort_if_contact_invalid(contact_id):
    if ContactMgr.is_valid_contact(contact_id):
        abort(404, message="Contact {} doesn't exist".format(contact_id))


def contact_json_validator(json):
    required_fields = ("fname", "mname", "lname", "addresses", "phones", "dates")
    if not all(required_field in json for required_field in required_fields):
        abort(400, message="Unknown JSON structure. Required field(s) missing {}".format(required_fields))


class Contact(Resource):

    def get(self, contact_id):
        abort_if_contact_invalid(contact_id)
        return ContactMgr.get_contact(contact_id)

    def delete(self, contact_id):
        abort_if_contact_invalid(contact_id)
        ContactMgr.delete_contact(contact_id)
        return '', 204

    def put(self, contact_id):
        abort_if_contact_invalid(contact_id)
        body = request.get_json()
        contact_json_validator(body)
        resp = ContactMgr.update_contact(contact_id, body)
        return resp, 201


class ContactList(Resource):
    def get(self):
        return ContactMgr.get_all_contacts()

    def post(self):
        body = request.get_json()
        contact_json_validator(body)
        contact_id = ContactMgr.add_contact(body)
        return {'contact_id': contact_id}, 201


api.add_resource(ContactList, '/contacts')
api.add_resource(Contact, '/contacts/<contact_id>')


@app.route('/')
def root():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
