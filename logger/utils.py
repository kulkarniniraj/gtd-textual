import requests

def info(message):
    requests.post('http://localhost:5000/log', json={'level': 'info', 'message': message})
    print(f"INFO: {message}")

def debug(message):
    requests.post('http://localhost:5000/log', json={'level': 'debug', 'message': message})
    print(f"DEBUG: {message}")

def warning(message):
    requests.post('http://localhost:5000/log', json={'level': 'warning', 'message': message})
    print(f"WARNING: {message}")    

def error(message):
    requests.post('http://localhost:5000/log', json={'level': 'error', 'message': message})
    print(f"ERROR: {message}")


