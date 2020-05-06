from flask import Blueprint, make_response, jsonify
from data.files import get_file_class

#  Blueprint объект
blueprint = Blueprint('api', __name__, template_folder='templates')


#  API получения информации о файле
@blueprint.route('/api/infoFile/<int:file_id>')
def infoFile(file_id):
    if not file_id:
        return make_response(jsonify({'error': 'Not found'}), 404)
    file = get_file_class(file_id)
    if not file:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if file.is_private:
        return make_response(jsonify({'error': 'File is private'}), 401)
    answer = file.to_dict()
    return jsonify(answer)
