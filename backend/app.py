from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a proper secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.JSON, nullable=True)

# Authentication Routes
@app.route('/signup', methods=['POST'])
def signup():
    username = request.json['username']
    password = request.json['password']
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created."}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        access_token = create_access_token(identity={'username': username})
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

# Patient Data Endpoints
@app.route('/patients', methods=['POST'])
@jwt_required()
def add_patient():
    name = request.json['name']
    data = request.json.get('data', {})
    new_patient = Patient(name=name, data=data)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"msg": "Patient added."}), 201

@app.route('/patients/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({"id": patient.id, "name": patient.name, "data": patient.data})

@app.route('/patients/<int:patient_id>', methods=['PUT'])
@jwt_required()
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient.name = request.json.get('name', patient.name)
    patient.data = request.json.get('data', patient.data)
    db.session.commit()
    return jsonify({"msg": "Patient updated."})

@app.route('/patients/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"msg": "Patient deleted."})

# Analytics Data Endpoint
@app.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    # Example to return historical analytics data
    # In reality, you would implement actual data retrieval and analysis logic
    return jsonify({"analytics": "historical patient data and trends"})

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)