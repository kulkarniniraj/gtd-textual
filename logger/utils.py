import requests

def info(message):
    try:
        requests.post('http://localhost:5000/log', json={'level': 'info', 'message': message}, timeout=10)
        print(f"INFO: {message}")
    except Exception:
        pass

def debug(message):
    try:
        requests.post('http://localhost:5000/log', json={'level': 'debug', 'message': message}, timeout=10)
        print(f"DEBUG: {message}")
    except Exception:
        pass

def warning(message):
    try:
        requests.post('http://localhost:5000/log', json={'level': 'warning', 'message': message}, timeout=10)
        print(f"WARNING: {message}")
    except Exception:
        pass

def error(message):
    try:
        requests.post('http://localhost:5000/log', json={'level': 'error', 'message': message}, timeout=10)
        print(f"ERROR: {message}")
    except Exception:
        pass


