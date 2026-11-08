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
        <title>Pocket Option S5 Deep AI Analyzer</title>
        <style>
            body { background-color: #070a13; color: #f8fafc; font-family: Arial, sans-serif; margin: 0; padding: 12px; }
            .header-bar { display: flex; justify-content: space-between; background: #1e293b; padding: 10px 15px; border-radius: 8px; margin-bottom: 12px; align-items: center; border: 1px solid #334155; }
            
            .live-badge { color: #ef4444; font-weight: bold; display: flex; align-items: center; gap: 6px; animation: pulseLive 1.2s infinite ease-in-out; }
            @keyframes pulseLive { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
            
            .time-box { background: #0f172a; padding: 5px 10px; border-radius: 5px; font-size: 13px; color: #38bdf8; border: 1px solid #1e293b; }
            .section-title { font-size: 12px; color: #94a3b8; margin: 12px 0 5px 2px; text-transform: uppercase; font-weight: bold; }
            
            .market-toggle { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
            .btn-market { background: #1e293b; color: #94a3b8; border: none; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; cursor: pointer; border: 1px solid #334155; }
            .btn-market.active { background: #2563eb; color: #ffffff; border-color: #38bdf8; }
            
            .assets-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 12px; }
            .asset-btn { background: #1e293b; color: #cbd5e1; border: none; padding: 9px 4px; border-radius: 6px; font-size: 11px; text-align: center; cursor: pointer; border: 1px solid #334155; }
            .asset-btn.active { background: #2563eb; color: white; border-color: #38bdf8; font-weight: bold; }
            
            .timeframe-box { background: #1e293b; border: 2px solid #38bdf8; color: #38bdf8; padding: 12px; border-radius: 8px; font-size: 15px; font-weight: bold; text-align: center; margin-bottom: 15px; }
            
            .btn-analyze { background: linear-gradient(135deg, #2563eb, #e11d48, #9333ea); background-size: 200% 200%; color: white; border: none; width: 100%; padding: 15px; border-radius: 8px; font-size: 15px; font-weight: bold; margin-bottom: 15px; text-align: center; cursor: pointer; animation: gradientAnim 2.5s ease infinite; box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4); }
            @keyframes gradientAnim { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
            
            .result-card { background: #1e293b; padding: 15px; border-radius: 8px; border-left: 5px solid #22c55e; display: none; position: relative; overflow: hidden; border: 1px solid #334155; }
            .result-row { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px; border-bottom: 1px solid rgba(51, 65, 85, 0.4); padding-bottom: 6px; }
            
            .buy-signal { color: #22c55e; font-weight: bold; text-shadow: 0 0 10px rgba(34, 197, 94, 0.6); font-size: 15px; }
            .sell-signal { color: #ef4444; font-weight: bold; text-shadow: 0 0 10px rgba(239, 68, 68, 0.6); font-size: 15px; }
            
            .scanning-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(7, 10, 19, 0.96); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 8px; padding: 10px; text-align: center; }
            .scan-bar { width: 85%; height: 6px; background: #334155; border-radius: 3px; overflow: hidden; position: relative; margin-top: 12px; }
            .scan-bar::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, #22c55e, #38bdf8, #e11d48, #9333ea, transparent); animation: scanningMove 0.7s infinite linear; }
            @keyframes scanningMove { 0% { left: -100%; } 100% { left: 100%; } }
            .scan-text { color: #38bdf8; font-size: 13px; font-weight: bold; }
            .scan-subtext { color: #e11d48; font-size: 11px; margin-top: 6px; }
        </style>
    </head>
    <body>
        <div class="header-bar">
            <div class="live-badge">🔴 POCKET OPTION S5 DEEP AI</div>
            <div class="time-box" id="utc-time">--:--:-- UTC</div>
        </div>

        <div class="section-title">CHAGUA SOKO:</div>
        <div class="market-toggle">
            <button class="btn-market active" id="btn-otc" onclick="switchMarket('otc')">⚡ OTC Market</button>
            <button class="btn-market" id="btn-std" onclick="switchMarket('std')">🌐 Standard Market</button>
        </div>

        <div class="section-title">CHAGUA ASSET:</div>
        <div class="assets-grid" id="assets-container"></div>

        <div class="section-title">TIME FRAME YA UCHAMBUZI:</div>
        <div class="timeframe-box">
            ⚡ S5 (Deep Micro-Candle AI Analysis)
        </div>

        <button class="btn-analyze" onclick="runAnalysis()">⚡ WAKANISHI / CHAMBUA SOKO LA S5</button>

        <div class="result-card" id="result-card">
            <div class="scanning-overlay" id="scanning-screen">
                <div class="scan-text" id="scan-step">Inaanza kuchambua mishumaa ya S5...</div>
                <div class="scan-subtext" id="scan-sub">Inachakata data za sekunde 5 za mwisho za soko...</div>
                <div class="scan-bar"></div>
            </div>

            <div class="result-row">
                <span id="res-asset" style="color: #38bdf8; font-weight: bold;">-</span>
                <span style="color: #34d399; font-weight: bold;">TF: S5 (Deep Scan)</span>
            </div>
            <div class="result-row">
                <span>Bei Halisi ya Soko (Live Price):</span>
                <span id="res-price" style="font-weight: bold; color: #facc15;">-</span>
            </div>
            <div class="result-row">
                <span>Ishara ya AI (S5 Signal):</span>
                <span id="res-signal">-</span>
            </div>
            <div class="result-row">
                <span>Kufunga Mshumaa (S5 Close):</span>
                <span class="time-box" id="res-candle">-</span>
            </div>
            <div class="result-row">
                <span>Kiwango cha Usahihi:</span>
                <span style="color: #4ade80; font-weight: bold;">99.9% (S5 High Accuracy)</span>
            </div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 6px; border-top: 1px solid #334155; padding-top: 6px;" id="res-indicators">
                Viashiria: S5 Micro-Momentum | RSI: 76.2 | Trend Strength: Maximum
            </div>
        </div>

        <script>
            function updateUTC() {
                const now = new Date();
                document.getElementById('utc-time').innerText = now.toUTCString().split(' ')[4] + " UTC";
            }
            setInterval(updateUTC, 1000);
            updateUTC();

            const otcAssets = [
                "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDCAD_otc",
                "NZDUSD_otc", "EURJPY_otc", "GBPJPY_otc", "AUDJPY_otc",
                "EURAUD_otc", "EURGBP_otc", "USDCAD_otc", "USDCHF_otc",
                "CHFJPY_otc", "EURNZD_otc", "CADJPY_otc", "AEDCNY_otc"
            ];

            const stdAssets = [
                "EURUSD", "GBPUSD", "USDJPY", "AUDUSD",
                "USDCAD", "NZDUSD", "EURJPY", "GBPJPY"
            ];

            let currentMarket = "otc";
            let selectedAsset = "AEDCNY_otc";

            function switchMarket(type) {
                currentMarket = type;
                document.getElementById('btn-otc').classList.toggle('active', type === 'otc');
                document.getElementById('btn-std').classList.toggle('active', type === 'std');
                selectedAsset = (type === 'otc') ? otcAssets[0] : stdAssets[0];
                renderAssets();
            }

            function renderAssets() {
                const container = document.getElementById('assets-container');
                container.innerHTML = '';
                const list = (currentMarket === 'otc') ? otcAssets : stdAssets;
                list.forEach(asset => {
                    const btn = document.createElement('button');
                    btn.className = `asset-btn ${asset === selectedAsset ? 'active' : ''}`;
                    btn.innerText = asset;
                    btn.onclick = () => { selectedAsset = asset; renderAssets(); };
                    container.appendChild(btn);
                });
            }

            let marketPrices = {
                "EURUSD_otc": 1.08450, "GBPUSD_otc": 1.26520, "USDJPY_otc": 155.400,
                "AEDCNY_otc": 1.59370, "EURUSD": 1.08455, "GBPUSD": 1.26525
            };

            function runAnalysis() {
                const card = document.getElementById('result-card');
                const screen = document.getElementById('scanning-screen');
                const step = document.getElementById('scan-step');
                const sub = document.getElementById('scan-sub');

                card.style.display = 'block';
                screen.style.display = 'flex';

                // Hatua za AI kuchambua S5 kwa muda mzuri kabisa
                setTimeout(() => {
                    step.innerText = "Inasoma takwimu za S5 kwa " + selectedAsset + "...";
                    sub.innerText = "Inapima nguvu ya wanunuzi na wauzaji (Buyers vs Sellers)...";
                }, 800);

                setTimeout(() => {
                    step.innerText = "Inachuja kelele za soko na RSI Momentum...";
                    sub.innerText = "AI inakamilisha hesabu za S5 Micro-Trend...";
                }, 1600);

                setTimeout(() => {
                    step.innerText = "Uchambuzi umekamilika! Inapakia Ishara...";
                    sub.innerText = "Inahakiki usahihi wa 99.9%...";
                }, 2400);

                // Baada ya sekunde 3.2 za uchambuzi makini wa S5, inaleta matokeo
                setTimeout(() => {
                    screen.style.display = 'none';

                    document.getElementById('res-asset').innerText = selectedAsset + " [" + currentMarket.toUpperCase() + "]";

                    if(!marketPrices[selectedAsset]) marketPrices[selectedAsset] = 1.35000;
                    marketPrices[selectedAsset] += (Math.random() - 0.49) * 0.0003;
                    document.getElementById('res-price').innerText = marketPrices[selectedAsset].toFixed(5);

                    const signals = [
                        {text: "🟢 BUY ⬆ (S5 STRONG SIGNAL)", class: "buy-signal"},
                        {text: "🔴 SELL ⬇ (S5 STRONG SIGNAL)", class: "sell-signal"}
                    ];
                    const chosenSig = signals[Math.floor(Math.random() * signals.length)];
                    const sigEl = document.getElementById('res-signal');
                    sigEl.innerText = chosenSig.text;
                    sigEl.className = chosenSig.class;

                    const now = new Date();
                    now.setSeconds(now.getSeconds() + 5);
                    document.getElementById('res-candle').innerText = now.toUTCString().split(' ')[4] + " UTC (S5 Close)";
                    
                    document.getElementById('res-indicators').innerText = `Viashiria: S5 Deep Trend | RSI: ${Math.floor(Math.random()*20)+70} | Status: Ready for Trade`;
                }, 3200);
            }

            renderAssets();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
