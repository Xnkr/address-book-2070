from flask import Flask, request, render_template, Response, jsonify
from flask_restful import abort, Api, Resource
from werkzeug.utils import secure_filename
from constants import *
from controller import ContactMgr

app = Flask(APP_NAME, template_folder=relative_path('static'))
app.config['UPLOAD_FOLDER'] = relative_path('uploads')
api = Api(app)


def abort_if_contact_invalid(contact_id):
    if ContactMgr.is_valid_contact(contact_id):
        abort(StandardResponses.NOT_FOUND_CODE, message="Contact {} doesn't exist".format(contact_id))


def contact_json_validator(json):
    required_fields = ("fname", "mname", "lname", "addresses", "phones", "dates")
    if not all(required_field in json for required_field in required_fields):
        abort(StandardResponses.BAD_REQUEST_CODE, message="Unknown JSON structure. Required field(s) missing {}".format(required_fields))


class Contact(Resource):

    def get(self, contact_id):
        abort_if_contact_invalid(contact_id)
        return ContactMgr.get_contact(contact_id)

    def delete(self, contact_id):
        abort_if_contact_invalid(contact_id)
        ContactMgr.delete_contact(contact_id)
        return '', StandardResponses.SUCCESS_NO_RESPONSE

    def put(self, contact_id):
        abort_if_contact_invalid(contact_id)
        body = request.get_json()
        contact_json_validator(body)
        resp = ContactMgr.update_contact(contact_id, body)
        return resp, StandardResponses.CREATED


class ContactList(Resource):
    def get(self):
        return ContactMgr.get_all_contacts()

    def post(self):
        body = request.get_json()
        contact_json_validator(body)
        contact_id = ContactMgr.add_contact(body)
        return {'contact_id': contact_id}, StandardResponses.CREATED


api.add_resource(ContactList, '/contacts')
api.add_resource(Contact, '/contacts/<contact_id>')


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/contacts/bulk_upload', methods=['POST'])
def bulk_upload_csv():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            abort(StandardResponses.BAD_REQUEST_CODE, message='No file part')
        file = request.files['file']
        if file.filename == '':
            abort(StandardResponses.BAD_REQUEST_CODE, message='No selected file')
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == '.csv':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            process_status = ContactMgr.process_bulk_import(file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            if process_status == StandardResponses.BAD_REQUEST_CODE:
                return Response(jsonify(StandardResponses.INVALID_CSV), status=StandardResponses.BAD_REQUEST_CODE)
            if process_status == StandardResponses.SERVER_ERROR_CODE:
                return Response(jsonify(StandardResponses.SERVER_ERROR), status=StandardResponses.SERVER_ERROR_CODE)
        return Response(status=StandardResponses.SUCCESS_CODE)


if __name__ == '__main__':
    app.run()
