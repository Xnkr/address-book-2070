from flask import Flask, request, Response, jsonify, send_from_directory
from flask_restful import abort, Api, Resource
from werkzeug.utils import secure_filename
from constants import *
from controller import ContactMgr
from flask_cors import CORS

app = Flask(APP_NAME, static_url_path='', static_folder="frontend/public")
app.config['UPLOAD_FOLDER'] = relative_path('uploads')
CORS(app)
api = Api(app)


def abort_if_contact_invalid(contact_id):
    if ContactMgr.is_valid_contact(contact_id):
        abort(StandardResponses.NOT_FOUND_CODE, message="Contact {} doesn't exist".format(contact_id))


def contact_json_validator(json):
    required_fields = ("fname", "mname", "lname", "addresses", "phones", "dates")
    if not all(required_field in json for required_field in required_fields):
        abort(StandardResponses.BAD_REQUEST_CODE,
              message="Unknown JSON structure. Required field(s) missing {}".format(required_fields))


def arg_parse_to_int(param):
    if param is not None and str.isnumeric(param):
        return int(param)
    else:
        return 0


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
        offset = arg_parse_to_int(request.args.get('offset'))
        limit = arg_parse_to_int(request.args.get('limit'))
        return ContactMgr.get_all_contacts(offset, limit)

    def post(self):
        body = request.get_json()
        contact_json_validator(body)
        contact_id = ContactMgr.add_contact(body)
        return {'contact_id': contact_id}, StandardResponses.CREATED


api.add_resource(ContactList, '/contacts')
api.add_resource(Contact, '/contacts/<contact_id>')


@app.route('/')
def root():
    path = os.path.join('.', 'frontend', 'public')
    return send_from_directory(path, 'index.html')


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
