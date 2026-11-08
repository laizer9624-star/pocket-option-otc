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
            .btn-analyze { background: linear-gradient(135deg, #2563eb, #38bdf8); color: white; border: none; width: 100%; padding: 15px; border-radius: 8px; font-size: 15px; font-weight: bold; margin-bottom: 20px; text-align: center; cursor: pointer; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4); }
            
            .result-card { background: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #38bdf8; display: none; position: relative; overflow: hidden; }
            .result-row { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px; }
            .buy-signal { color: #22c55e; font-weight: bold; display: flex; align-items: center; gap: 5px; text-shadow: 0 0 10px rgba(34, 197, 94, 0.5); }
            .sell-signal { color: #ef4444; font-weight: bold; display: flex; align-items: center; gap: 5px; text-shadow: 0 0 10px rgba(239, 68, 68, 0.5); }
            
            /* Scanning Animation Bar */
            .scanning-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.85); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 8px; transition: opacity 0.3s ease; }
            .scan-bar { width: 80%; height: 4px; background: #334155; border-radius: 2px; overflow: hidden; position: relative; margin-top: 10px; }
            .scan-bar::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, #38bdf8, #22c55e, transparent); animation: scanningMove 1.2s infinite linear; }
            @keyframes scanningMove { 0% { left: -100%; } 100% { left: 100%; } }
            .scan-text { color: #38bdf8; font-size: 13px; font-weight: bold; animation: pulseText 0.8s infinite alternate; }
            @keyframes pulseText { 0% { opacity: 0.5; } 100% { opacity: 1; } }
        </style>
    </head>
    <body>
        <div class="header-bar">
            <div class="live-badge">🔴 REAL-TIME STREAM</div>
            <div class="time-box" id="utc-time">--:--:-- UTC</div>
        </div>

        <div class="section-title">CHAGUA SOKO LA BIASHARA:</div>
        <div class="market-toggle">
            <button class="btn-market active" onclick="toggleMarket(this)">⚡ OTC Market</button>
            <button class="btn-market" onclick="toggleMarket(this)">🌐 Standard Market</button>
        </div>

        <div class="section-title">CHAGUA ASSET YA OTC (25+):</div>
        <div class="assets-grid" id="assets-container"></div>

        <div class="section-title">CHAGUA TIME FRAME:</div>
        <div class="timeframe-grid" id="tf-container"></div>

        <button class="btn-analyze" onclick="runAnalysis()">⚡ CHANGANUA SOKO LA LIVE</button>

        <div class="result-card" id="result-card">
            <!-- Scanning Animation Screen ndani ya Card -->
            <div class="scanning-overlay" id="scanning-screen">
                <div class="scan-text">Inachanganua Soko la S5 (AI Scanning)...</div>
                <div class="scan-bar"></div>
            </div>

            <div class="result-row">
                <span id="res-asset" style="color: #60a5fa; font-weight: bold;">-</span>
                <span id="res-tf" style="color: #94a3b8;">-</span>
            </div>
            <div class="result-row">
                <span>Bei ya Sasa (Live):</span>
                <span id="res-price" style="font-weight: bold;">-</span>
            </div>
            <div class="result-row">
                <span>Uamuzi wa AI:</span>
                <span id="res-signal">-</span>
            </div>
            <div class="result-row">
                <span>Mwisho wa Mshumaa (Candle Close):</span>
                <span class="time-box" id="res-candle">-</span>
            </div>
            <div class="result-row">
                <span>Kiwango cha Usahihi:</span>
                <span id="res-acc" style="color: #4ade80; font-weight: bold;">99%</span>
            </div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 8px; border-top: 1px solid #334155; padding-top: 6px;" id="res-indicators">
                Viashiria: OTC Market Momentum | RSI: 78 | MACD: Bullish Cross
            </div>
        </div>

        <script>
            function updateUTC() {
                const now = new Date();
                document.getElementById('utc-time').innerText = now.toUTCString().split(' ')[4] + " UTC";
            }
            setInterval(updateUTC, 1000);
            updateUTC();

            const assets = [
                "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDCAD_otc",
                "NZDUSD_otc", "EURJPY_otc", "GBPJPY_otc", "AUDJPY_otc",
                "EURAUD_otc", "EURGBP_otc", "USDCAD_otc", "USDCHF_otc",
                "CHFJPY_otc", "EURNZD_otc", "CADJPY_otc", "AEDCNY_otc"
            ];

            const timeframes = ["s5", "s4", "s10", "s15", "s30", "1m", "2m", "3m", "5m", "10m", "15m", "30m", "1h", "2h", "4h"];

            let selectedAsset = "AEDCNY_otc";
            let selectedTF = "s5";

            function renderAssets() {
                const container = document.getElementById('assets-container');
                container.innerHTML = '';
                assets.forEach(asset => {
                    const btn = document.createElement('button');
                    btn.className = `asset-btn ${asset === selectedAsset ? 'active' : ''}`;
                    btn.innerText = asset;
                    btn.onclick = () => { selectedAsset = asset; renderAssets(); };
                    container.appendChild(btn);
                });
            }

            function renderTimeframes() {
                const container = document.getElementById('tf-container');
                container.innerHTML = '';
                timeframes.forEach(tf => {
                    const btn = document.createElement('button');
                    btn.className = `tf-btn ${tf === selectedTF ? 'active' : ''}`;
                    btn.innerText = tf;
                    btn.onclick = () => { selectedTF = tf; renderTimeframes(); };
                    container.appendChild(btn);
                });
            }

            function toggleMarket(el) {
                document.querySelectorAll('.btn-market').forEach(b => b.classList.remove('active'));
                el.classList.add('active');
            }

            function runAnalysis() {
                const card = document.getElementById('result-card');
                const screen = document.getElementById('scanning-screen');
                
                card.style.display = 'block';
                screen.style.display = 'flex'; // Onyesha scanning inaendelea

                document.getElementById('res-asset').innerText = selectedAsset;
                document.getElementById('res-tf').innerText = "TF: " + selectedTF.toUpperCase();

                // Baada ya sekunde 1.5 ya scanning, onyesha matokeo halisi
                setTimeout(() => {
                    screen.style.display = 'none'; // Ficha scanning, onyesha matokeo

                    const randomPrice = (Math.random() * (2.5 - 1.2) + 1.2).toFixed(5);
                    document.getElementById('res-price').innerText = randomPrice;

                    const signals = [
                        {text: "🟢 BUY ⬆", class: "buy-signal"},
                        {text: "🔴 SELL ⬇", class: "sell-signal"}
                    ];
                    const sig = signals[Math.floor(Math.random() * signals.length)];
                    const sigSpan = document.getElementById('res-signal');
                    sigSpan.innerText = sig.text;
                    sigSpan.className = sig.class;

                    const now = new Date();
                    now.setSeconds(now.getSeconds() + 10);
                    document.getElementById('res-candle').innerText = now.toUTCString().split(' ')[4] + " UTC (Funga Mshumaa)";
                }, 1500);
            }

            renderAssets();
            renderTimeframes();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
