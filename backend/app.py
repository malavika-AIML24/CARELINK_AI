from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_api():
    return jsonify({'message': 'Welcome to the Flask REST API!'}), 200

if __name__ == '__main__':
    app.run(debug=True)