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
            body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; text-align: center; }
            .card { background: #1e293b; padding: 20px; border-radius: 10px; max-width: 400px; margin: 50px auto; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            h1 { color: #38bdf8; font-size: 24px; }
            p { color: #94a3b8; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Pocket Option OTC Dashboard</h1>
            <p>Hali ya Mfumo: <strong style="color: #4ade80;">Iko Hewani & Salama</strong></p>
            <p>Umeingia kama: <strong>PorketOption</strong></p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
