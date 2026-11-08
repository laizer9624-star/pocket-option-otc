from flask import Flask, render_template_string
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "PorketOption": "54321"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pocket Option OTC Dashboard</title>
        <style>
            body { background: #0f172a; color: #ffffff; font-family: Arial, sans-serif; margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; }
            .header { background: #1e293b; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; }
            h2 { color: #38bdf8; margin: 0; font-size: 18px; }
            .user-info { color: #4ade80; font-size: 14px; }
            .container { flex: 1; width: 100%; height: 100%; }
            iframe { width: 100%; height: 100%; border: none; background: #0f172a; }
        </style>
    </head>
    <body>
        <div class="header">
            <h2>Pocket Option OTC Dashboard</h2>
            <div class="user-info">Imeingia: PorketOption</div>
        </div>
        <div class="container">
            <iframe src="https://pocketoption.com" title="Pocket Option Terminal"></iframe>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
