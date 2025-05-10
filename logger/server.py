from loguru import logger
from flask import Flask, request, jsonify

"""
This is a logging server for other application
This is a flask server with only one route /log, which accepts POST request with JSON body and logs given message on screen
"""



app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    level = data.get('level', 'info').upper()
    message = data.get('message', '')
    logger.log(level, message)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=5000)

# test using curl
# curl -X POST -H "Content-Type: application/json" -d '{"level": "info", "message": "Hello World"}' http://localhost:5100/log