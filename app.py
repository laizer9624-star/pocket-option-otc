from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "Porket option": "54321"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    return "Karibu kwenye Pocket Option OTC Dashboard!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
