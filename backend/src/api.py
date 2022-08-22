import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks")
@requires_auth('get:drinks')
def drinks(jwt):
    drinks = Drink.query.all()
    drinks_short = [drink.short() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks_short
    })

'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    drinks = Drink.query.all()
    drinks_long = [drink.long() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks_long
    })

'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    parsed = request.get_json()
    drink = Drink(
        id = None,
        title= parsed['title'],
        recipe= json.dumps(parsed['recipe'])
    )
    drink.insert()
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })

'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt,id):
    try:
        drink = Drink.query.filter(Drink.id==id).first()
        if not drink:
            abort(404)
        parsed = request.get_json()
        drink.title=parsed['title']
        drink.recipe=json.dumps(parsed['recipe'])
        drink.update()
        return jsonify({
            'success':True,
            'drinks':[drink.long()]
        })
    except Exception as e:
        print(e)
        abort(401)

'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def update_specific_drink(jwt,id):
    try:
        drink = Drink.query.filter(Drink.id==id).first()
        if not drink:
            abort(404)
        drink.delete()
        return jsonify({
            'success':True,
            'delete': id
        })
    except Exception as e:
        print(e)
        abort(401)


# Error Handling
'''
Example error handling for unprocessable entity
'''

#handle unproccessable
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# handle authentication
@app.errorhandler(AuthError)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

#handle bad request
@app.errorhandler(400)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

#handle bad request
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "missing"
    }), 401

#handle missing
@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

# handle not allowed
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405