from flask import Blueprint, jsonify, request

from app.service import service

my_controller = Blueprint("controller", __name__)


@my_controller.route("/")
def hello():
    return jsonify(greetings="Greetings from tax calculator!")


@my_controller.route('/income-info')
def get_all_rows():
    # TODO - proba bly we have easiest way to convert it to json data.
    return jsonify([entity.__dict__ for entity in service.find_income_info(**request.args)])


@my_controller.route("/income-info", methods=['POST'])
def add_invoice():
    data = request.get_json()
    # TODO which options we have for initializing entities except init
    added_row = service.add_income_info(**data)
    # TODO seems it's not elegant solution. Perhaps we have some API standard for jsonify object case?
    return jsonify(added_row.__dict__)


@my_controller.route("/income-value")
def get_income():
    return jsonify(value=service.get_income_value(**request.args))
