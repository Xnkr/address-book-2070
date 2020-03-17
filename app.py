from flask import Flask, request, Response, jsonify, send_from_directory
from flask_restful import abort, Api, Resource
from werkzeug.utils import secure_filename
from constants import *
from controller import ContactMgr
from flask_cors import CORS

# Set up Flask
app = Flask(APP_NAME, static_url_path='', static_folder="frontend/public")
app.config['UPLOAD_FOLDER'] = relative_path('uploads')

# To fix CORS issue when using APIs
CORS(app)

# Convert to RESTful app
api = Api(app)


def abort_if_contact_invalid(contact_id):
    """
        Validates requested contact_id with database
        :param contact_id: ID of the contact in request
    """
    if not ContactMgr.is_valid_contact(contact_id):
        abort(StandardResponses.NOT_FOUND_CODE, message="Contact {} doesn't exist".format(contact_id))


def contact_json_validator(json):
    """
        Validates POST/PUT requests body
        :param json: JSON request within POST/PUT body
    """
    required_fields = ("fname", "mname", "lname", "addresses", "phones", "dates")
    if not all(required_field in json for required_field in required_fields):
        logger.error("Unknown JSON structure. Required field(s) missing {}".format(json))
        abort(StandardResponses.BAD_REQUEST_CODE,
              message="Unknown JSON structure. Required field(s) missing {}".format(required_fields))


# Parsing query parameter
def arg_parse_to_int(param): return int(param) if param is not None and str.isnumeric(param) else 0


class Contact(Resource):
    """
        Contact resource for handling requests pertaining to a single contact
    """

    def get(self, contact_id):
        """
            Fetches Contact information with contact_id
            :param contact_id: contact_id of the required Contact
        """
        abort_if_contact_invalid(contact_id)
        return ContactMgr.get_contact(contact_id)

    def delete(self, contact_id):
        """
            Deletes the Contact with contact_id
            :param contact_id: contact_id to delete
        """
        abort_if_contact_invalid(contact_id)
        ContactMgr.delete_contact(contact_id)
        return '', StandardResponses.SUCCESS_NO_RESPONSE

    def put(self, contact_id):
        """
            Updates the Contact if found in database else creates new contact
            :param contact_id: contact_id to update/edit
        """
        body = request.get_json()
        contact_json_validator(body)
        resp = ''
        try:
            resp, status = ContactMgr.update_contact(contact_id, body)
        except TypeError as e:
            abort(StandardResponses.BAD_REQUEST_CODE, message=str(e))
        if resp:
            resp = {'contact_id': contact_id}
        return resp, status


class ContactList(Resource):
    """
        ContactList resource for handling requests pertaining to bulk contacts
    """

    def get(self):
        """
            Fetches all contacts (or) contacts matching criteria
            :query_param offset: Offset for fetching contacts
            :query_param limit: Number of contacts to fetched
            :query_param q: Query for searching contacts (Name, Address, Phone)
        """
        offset = arg_parse_to_int(request.args.get('offset'))
        limit = arg_parse_to_int(request.args.get('limit'))
        q = request.args.get('q')
        fmt = request.args.get('fmt', '')
        if q:
            return ContactMgr.search(q, fmt == 'minimal')
        return ContactMgr.get_all_contacts(offset, limit, fmt == 'minimal')

    def post(self):
        """
            Creates a contact and returns contact_id
        """
        body = request.get_json()
        contact_json_validator(body)
        try:
            contact_id = ContactMgr.add_contact(body)
            return {'contact_id': contact_id}, StandardResponses.CREATED
        except TypeError as e:
            abort(StandardResponses.BAD_REQUEST_CODE, message=str(e))


# Assign endpoints to resource
api.add_resource(ContactList, '/contacts')
api.add_resource(Contact, '/contacts/<int:contact_id>')


@app.route('/')
def root():
    """
        Endpoint for launching frontend
    """
    path = os.path.join('.', 'frontend', 'public')
    return send_from_directory(path, 'index.html')


@app.route('/contacts/bulk_upload', methods=['POST'])
def bulk_upload_csv():
    """
        Endpoint for uploading CSV file for bulk contact creation
        :request-body-param file: File-part of CSV file
    """
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


@app.before_request
def log_request():
    """
        Logs information about incoming requests
    """
    logger.info(f"{request.remote_addr} - [{request.method}] {request.path}")


if __name__ == '__main__':
    app.run()
