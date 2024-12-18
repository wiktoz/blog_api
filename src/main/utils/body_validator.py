from flask import jsonify

def check_data(data, required_data):
    missing_data = [key for key in required_data if key not in data]

    if missing_data:
        return False
    return True