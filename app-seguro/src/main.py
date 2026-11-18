from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "App Seguro On!!!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)