from functools import reduce

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from climbing_route_dao import ClimbingRouteDao
from climbing_route import ClimbingRoute

climbing_route_blueprint = Blueprint('climbing_route_blueprint', __name__)
climbing_route_dao = ClimbingRouteDao('climbing_management.db')


@climbing_route_blueprint.route('/routes', methods=['GET'])
@login_required
def get_all_routes():
    routes = climbing_route_dao.get_all_routes()
    return jsonify([route.__dict__ for route in routes]), 200


@climbing_route_blueprint.route('/routes/<int:route_id>', methods=['GET'])
@login_required
def get_route(route_id):
    route = climbing_route_dao.get_route(route_id)
    if route:
        return jsonify(route.__dict__), 200
    else:
        return jsonify({'message': 'Route not found'}), 404


@climbing_route_blueprint.route('/routes', methods=['POST'])
@login_required
def add_route():
    data = request.get_json()
    new_route = ClimbingRoute(None, current_user.id, data['name'], data['grade'])
    climbing_route_dao.add_route(new_route, current_user.id)
    return jsonify({'message': 'Climbing route created'}), 201


@climbing_route_blueprint.route('/routes/<int:route_id>', methods=['PUT'])
@login_required
def update_route(route_id):
    data = request.get_json()
    updated_route = ClimbingRoute(route_id, current_user.id, data['name'], data['grade'])
    if climbing_route_dao.update_route(updated_route, current_user.id):
        return jsonify({'message': 'Route updated'}), 200
    else:
        return jsonify({'message': 'Route not found or not updated'}), 404


@climbing_route_blueprint.route('/routes/filter', methods=['POST'])
@login_required
def filter_routes():
    data = request.get_json()
    name_filter = data.get('name')
    grade_filter = data.get('grade')

    routes = climbing_route_dao.get_all_routes()
    filtered_routes = list(filter(lambda route: (route.name == name_filter or not name_filter) and
                                                (route.grade == grade_filter or not grade_filter), routes))
    return jsonify([route.__dict__ for route in filtered_routes]), 200


@climbing_route_blueprint.route('/routes/uppercase', methods=['GET'])
@login_required
def get_all_routes_uppercase():
    routes = climbing_route_dao.get_all_routes()
    uppercase_routes = [{'name': (lambda name: name.upper())(route.name), 'grade': route.grade} for route in routes]
    return jsonify(uppercase_routes), 200


@climbing_route_blueprint.route('/routes/summary', methods=['GET'])
@login_required
def route_summary():
    routes = climbing_route_dao.get_all_routes()

    grade_counts = reduce(
        lambda acc, route: {**acc, route.grade: acc.get(route.grade, 0) + 1},
        routes,
        {}
    )

    grade_to_numeric = {'5a': 1, '5b': 2, '6a': 3, '6b': 4, '7a': 5, '7b': 6, '7c': 7, '8a': 8, '8b': 9, '8c': 10}
    numeric_grades = list(map(lambda route: grade_to_numeric.get(route.grade, 0), routes))
    average_difficulty = reduce(lambda acc, x: acc + x, numeric_grades, 0) / len(
        numeric_grades) if numeric_grades else 0

    uppercase_routes = list(map(lambda route: {'name': route.name.upper(), 'grade': route.grade}, routes))

    return jsonify({
        'total_routes': len(routes),
        'grade_counts': grade_counts,
        'average_difficulty': average_difficulty,
        'uppercase_routes': uppercase_routes
    }), 200


@climbing_route_blueprint.route('/routes/<int:route_id>', methods=['DELETE'])
@login_required
def delete_route(route_id):
    if climbing_route_dao.delete_route(route_id, current_user.id):
        return jsonify({'message': 'Route deleted'}), 200
    else:
        return jsonify({'message': 'Route not found or not deleted'}), 404
