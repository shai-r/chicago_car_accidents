from http.client import responses

from flask import Blueprint, request
from config.connect import daily
from repository.accidents_repository import find_all_accidents_by_area
from repository.csv_repository import init_accidents
from  dto.ResponseDto import ResponseDto

accidents_blueprint = Blueprint('/', __name__)

@accidents_blueprint.route('initialize-db', methods=['POST'])
def initialize_db():
    init_accidents()
    return ResponseDto(message='Database initialized successfully'), 200


@accidents_blueprint.route('/<string:area>', methods=['GET'])
def total_accidents_in_area(area: str):
    all_accidents_by_area = find_all_accidents_by_area(area=area)
    return all_accidents_by_area, 200
