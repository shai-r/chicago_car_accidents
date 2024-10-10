from flask import Blueprint, request

from config.connect import daily
from repository.csv_repository import init_accidents

accidents_blueprint = Blueprint('/', __name__)

@accidents_blueprint.route('initialize-db', methods=['POST'])
def initialize_db():
    init_accidents()
    return {'message': 'Database initialized successfully'}, 200


@accidents_blueprint.route('accidents/area', methods=['GET'])
def total_accidents_in_area():
    beat = request.args.get('beat')

    if not beat:
        return {'error': 'beat parameter is required'}, 400

    total_accidents = daily.count_documents({'area': beat})

    return {'total_accidents': total_accidents}, 200