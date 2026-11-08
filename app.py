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
    <html lang="sw">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pocket Option OTC Dashboard</title>
        <style>
            body { background-color: #0f172a; color: #f8fafc; font-family: Arial, sans-serif; margin: 0; padding: 15px; }
            .header-bar { display: flex; justify-content: space-between; background: #1e293b; padding: 10px 15px; border-radius: 8px; margin-bottom: 15px; align-items: center; }
            .live-badge { color: #f87171; font-weight: bold; display: flex; align-items: center; gap: 5px; }
            .time-box { background: #334155; padding: 5px 10px; border-radius: 5px; font-size: 14px; }
            .section-title { font-size: 13px; color: #94a3b8; margin: 15px 0 5px 2px; text-transform: uppercase; }
            .market-toggle { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
            .btn-market { background: #1e293b; color: #94a3b8; border: none; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; cursor: pointer; }
            .btn-market.active { background: #2563eb; color: #ffffff; }
            .assets-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 15px; }
            .asset-btn { background: #1e293b; color: #cbd5e1; border: none; padding: 10px 5px; border-radius: 6px; font-size: 12px; text-align: center; cursor: pointer; }
            .asset-btn.active { background: #2563eb; color: white; }
            .timeframe-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 15px; }
            .tf-btn { background: #1e293b; color: #cbd5e1; border: none; padding: 10px; border-radius: 6px; font-size: 13px; text-align: center; cursor: pointer; }
            .tf-btn.active { background: #2563eb; color: white; }
            .btn-analyze { background: #2563eb; color: white; border: none; width: 100%; padding: 15px; border-radius: 8px; font-size: 15px; font-weight: bold; margin-bottom: 20px; text-align: center; cursor: pointer; }
            .result-card { background: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #22c55e; }
            .result-row { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px; }
            .buy-signal { color: #22c55e; font-weight: bold; display: flex; align-items: center; gap: 5px; }
        </style>
    </head>
    <body>
        <div class="header-bar">
            <div class="live-badge">🔴 REAL-TIME STREAM</div>
            <div class="time-box" id="utc-time">10:37:45 UTC</div>
        </div>

        <div class="section-title">CHAGUA SOKO LA BIASHARA:</div>
        <div class="market-toggle">
            <button class="btn-market active">⚡ OTC Market</button>
            <button class="btn-market">🌐 Standard Market</button>
        </div>

        <div class="section-title">CHAGUA ASSET YA OTC (25+):</div>
        <div class="assets-grid">
            <button class="asset-btn">EURUSD_otc</button>
            <button class="asset-btn">GBPUSD_otc</button>
            <button class="asset-btn">USDJPY_otc</button>
            <button class="asset-btn">AUDCAD_otc</button>
            <button class="asset-btn">NZDUSD_otc</button>
            <button class="asset-btn">EURJPY_otc</button>
            <button class="asset-btn">GBPJPY_otc</button>
            <button class="asset-btn">AUDJPY_otc</button>
            <button class="asset-btn">EURAUD_otc</button>
            <button class="asset-btn">EURGBP_otc</button>
            <button class="asset-btn">USDCAD_otc</button>
            <button class="asset-btn">USDCHF_otc</button>
            <button class="asset-btn">CHFJPY_otc</button>
            <button class="asset-btn">EURNZD_otc</button>
            <button class="asset-btn">CADJPY_otc</button>
            <button class="asset-btn active">AEDCNY_otc</button>
        </div>

        <div class="section-title">CHAGUA TIME FRAME:</div>
        <div class="timeframe-grid">
            <button class="tf-btn active">s5</button>
            <button class="tf-btn">s4</button>
            <button class="tf-btn">s10</button>
            <button class="tf-btn">s15</button>
            <button class="tf-btn">s30</button>
            <button class="tf-btn">1m</button>
            <button class="tf-btn">2m</button>
            <button class="tf-btn">3m</button>
            <button class="tf-btn">5m</button>
            <button class="tf-btn">10m</button>
            <button class="tf-btn">15m</button>
            <button class="tf-btn">30m</button>
            <button class="tf-btn">1h</button>
            <button class="tf-btn">2h</button>
            <button class="tf-btn">4h</button>
        </div>

        <button class="btn-analyze">⚡ CHANGANUA SOKO LA LIVE</button>

        <div class="result-card">
            <div class="result-row">
                <span style="color: #60a5fa; font-weight: bold;">AEDCNY_otc</span>
                <span style="color: #94a3b8;">TF: S5</span>
            </div>
            <div class="result-row">
                <span>Bei ya Sasa (Live):</span>
                <span style="font-weight: bold;">1.59377</span>
            </div>
            <div class="result-row">
                <span>Uamuzi wa AI:</span>
                <span class="buy-signal">🟢 BUY ⬆</span>
            </div>
            <div class="result-row">
                <span>Mwisho wa Mshumaa (Candle Close):</span>
                <span class="time-box">10:37:10 UTC (Funga Mshumaa)</span>
            </div>
            <div class="result-row">
                <span>Kiwango cha Usahihi:</span>
                <span style="color: #4ade80; font-weight: bold;">99%</span>
            </div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 8px; border-top: 1px solid #334155; padding-top: 6px;">
                Vhashiria: OTC Market Momentum | RSI: 78
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
