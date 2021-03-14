#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from predictiveModel.Reviser import Reviser
from predictiveModel.decision_tree import Decision_tree
from models.DataSet import DataSet
from flasgger import Swagger

app = Flask(__name__)
app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec.json"
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/todo/api/v1.0/swagger"
}

swagger = Swagger(app, config=swagger_config)

decision_tree = Decision_tree()
dataSet = DataSet()
reviser = Reviser()


@app.route('/todo/api/v1.0/recommended-books/<int:id>', methods=['GET'])
def get_recommended_fields(id):
    """
   Get Recommended books
   This endpoint return a list of 10 books personally recommended
   ---
   parameters:
     - in: path
       name: id
       type: integer
       required: true
   responses:
     200:
       description: list of books recommended
    """
    prediction_name = decision_tree.fit(id)
    recommended_Data, name = reviser.get_recommendations(prediction_name[0], id)
    df_ordered = recommended_Data.sort_values(['genre', 'score'], ascending=False)
    df_ordered = df_ordered.drop(['score'], axis=1)
    df_ordered = df_ordered.head(10)
    information_json = df_ordered.to_dict('records')
    data = {
        'recommendations': information_json,
        'name': name[0]['name']
    }
    return data, 200


@app.route('/todo/api/v1.0/rates/<int:id>', methods=['GET'])
def create_punctuation(id):
    """
   Get rates by user id
   This endpoint return all the rates of a user
   ---
   parameters:
     - in: path
       name: id
       type: integer
       required: true
   responses:
     200:
       description: list of rates of the user
    """
    data_of_initial_user, name = dataSet.get_punctuations_by_id(id)
    information_json = data_of_initial_user.to_dict('records')
    data = {
        'rates': information_json,
        'name': name[0]['name']
    }
    return data, 200


@app.route('/todo/api/v1.0/rate', methods=['POST'])
def get_rates_by_id():
    """
    Create a new rate
    This endpoint return done if it has been done correctly
    ---
    parameters:
    - in: "body"
      name: "body"
      description: "Accepts a name of an user, the score, and the name of the book"
      required: true
      schema:
        type: "object"
        properties:
          name:
            type: "string"
            example : "Chuck"
          score:
            type: "int"
            format: "int64"
            example : 5
          book:
            type: "string"
            example: "Analysis, Vol I"
    responses:
      405:
        description: "Invalid input"
    """
    if not request.json:
        abort(400)
    punctuation = {
        'name': request.json['name'],
        'score': request.json['score'],
        'book': request.json['book'],
    }
    dataSet.insert_punctuation(punctuation['name'], punctuation['score'], punctuation['book'])
    return jsonify({'task': 'done'}), 201


@app.route('/todo/api/v1.0/books', methods=['GET'])
def get_names_books():
    """
  Get all books
  This endpoint return a list of all books
  ---
  responses:
    200:
      description: list of all books
   """
    books = dataSet.get_books(True)
    information_json = books.to_dict('records')
    data = {
        'books': information_json
    }
    return data, 200


@app.route('/todo/api/v1.0/users', methods=['GET'])
def get_users():
    """
   Get all users
   This endpoint return a list with all the users in the app
   ---
   responses:
     200:
       description: list of users
    """
    users = dataSet.get_users()
    information_json = users.to_dict('records')
    data = {
        'users': information_json
    }
    return data, 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'URL Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
