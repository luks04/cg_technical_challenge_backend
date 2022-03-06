from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/app", methods = ['GET'])
def api_app():
    try:
        response = jsonify({'message': f'Message from app.py'})
        response.status_code = 200
    except Exception as error:
        response = jsonify({'message': str(error).capitalize() + ' from app.py'})
        response.status_code = 500
    return response

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080, debug = True)
