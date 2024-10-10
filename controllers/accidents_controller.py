from dataclasses import asdict
from http.client import responses
from flask import Blueprint, jsonify, request
from config.connect import daily
from repository.accidents_repository import (find_all_accidents_by_area,
                                             get_accidents_by_area_and_time, get_accidents_by_cause,
                                             get_injury_stats_by_area)
from repository.csv_repository import init_accidents
from  dto.ResponseDto import ResponseDto
from utils.convert_to_json_utils import convert_accidents_by_area_to_json, parse_json

accidents_blueprint = Blueprint('/', __name__)

@accidents_blueprint.route('initialize-db', methods=['POST'])
def initialize_db():
    init_accidents()
    return jsonify(asdict(ResponseDto(message='Database initialized successfully'))), 200

@accidents_blueprint.route('/<int:area>', methods=['GET'])
def total_accidents_in_area(area):
    accidents = find_all_accidents_by_area(area=str(area))
    return jsonify(asdict(ResponseDto(body=list(map(parse_json, accidents))))), 200

@accidents_blueprint.route("/accidents_by_date/<int:area>", methods=['GET'])
def get_accidents_by_area(area: int):
    if not area:
        return jsonify({"error": "beat area is required"}), 400
    time_type = request.args.get('time-type')
    date = request.args.get('date')

    if (time_type and not date) or (not time_type and date):
        return jsonify({"error": "date params are required"}), 400

    accidents = get_accidents_by_area_and_time(area, time_type, date)
    return jsonify(asdict(ResponseDto(body=parse_json(accidents)))), 200

@accidents_blueprint.route('/by_cause/<int:area>', methods=['GET'])
def accidents_by_cause(area):
    results = get_accidents_by_cause(area=str(area))
    return jsonify(results)

@accidents_blueprint.route('/injury_stats/<int:area>', methods=['GET'])
def injury_stats_by_area(area):
    results = get_injury_stats_by_area(area=str(area))
    return jsonify(results[0])
