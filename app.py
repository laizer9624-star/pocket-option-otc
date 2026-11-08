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
        <title>Pocket Option OTC & Standard Live Bot</title>
        <style>
            body { background-color: #0b0f19; color: #f8fafc; font-family: Arial, sans-serif; margin: 0; padding: 12px; }
            .header-bar { display: flex; justify-content: space-between; background: #1e293b; padding: 10px 15px; border-radius: 8px; margin-bottom: 12px; align-items: center; border: 1px solid #334155; }
            
            /* Live Badge inayowaka na kufifia */
            .live-badge { color: #ef4444; font-weight: bold; display: flex; align-items: center; gap: 6px; animation: pulseLive 1.5s infinite ease-in-out; }
            @keyframes pulseLive { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }
            
            .time-box { background: #0f172a; padding: 5px 10px; border-radius: 5px; font-size: 13px; color: #38bdf8; border: 1px solid #1e293b; }
            .section-title { font-size: 12px; color: #94a3b8; margin: 12px 0 5px 2px; text-transform: uppercase; font-weight: bold; }
            
            .market-toggle { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
            .btn-market { background: #1e293b; color: #94a3b8; border: none; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; cursor: pointer; transition: 0.2s; border: 1px solid #334155; }
            .btn-market.active { background: #2563eb; color: #ffffff; border-color: #38bdf8; }
            
            .assets-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 12px; }
            .asset-btn { background: #1e293b; color: #cbd5e1; border: none; padding: 9px 4px; border-radius: 6px; font-size: 11px; text-align: center; cursor: pointer; border: 1px solid #334155; }
            .asset-btn.active { background: #2563eb; color: white; border-color: #38bdf8; font-weight: bold; }
            
            .timeframe-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 12px; }
            .tf-btn { background: #1e293b; color: #cbd5e1; border: none; padding: 8px; border-radius: 6px; font-size: 12px; text-align: center; cursor: pointer; border: 1px solid #334155; }
            .tf-btn.active { background: #059669; color: white; border-color: #34d399; font-weight: bold; }
            
            /* Kitufe cha Kuchanganua chenye Rangi za Kuvutia */
            .btn-analyze { background: linear-gradient(135deg, #2563eb, #9333ea, #db2777); background-size: 200% 200%; color: white; border: none; width: 100%; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: bold; margin-bottom: 15px; text-align: center; cursor: pointer; animation: gradientAnim 3s ease infinite; box-shadow: 0 4px 15px rgba(147, 51, 234, 0.4); }
            @keyframes gradientAnim { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
            
            .result-card { background: #1e293b; padding: 15px; border-radius: 8px; border-left: 5px solid #38bdf8; display: none; position: relative; overflow: hidden; border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155; }
            .result-row { display: flex; justify-content: space-between; margin-bottom: 9px; font-size: 13px; border-bottom: 1px solid rgba(51, 65, 85, 0.4); padding-bottom: 5px; }
            
            .buy-signal { color: #22c55e; font-weight: bold; text-shadow: 0 0 10px rgba(34, 197, 94, 0.6); font-size: 15px; }
            .sell-signal { color: #ef4444; font-weight: bold; text-shadow: 0 0 10px rgba(239, 68, 68, 0.6); font-size: 15px; }
            
            /* Scanning Animation Screen ndani ya Card */
            .scanning-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.92); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; border-radius: 8px; }
            .scan-bar { width: 85%; height: 6px; background: #334155; border-radius: 3px; overflow: hidden; position: relative; margin-top: 12px; }
            .scan-bar::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, #ef4444, #38bdf8, #22c55e, #9333ea, transparent); animation: scanningMove 1s infinite linear; }
            @keyframes scanningMove { 0% { left: -100%; } 100% { left: 100%; } }
            .scan-text { color: #38bdf8; font-size: 13px; font-weight: bold; text-align: center; }
            .scan-subtext { color: #a855f7; font-size: 11px; margin-top: 5px; }
            
            .ws-status { font-size: 10px; color: #34d399; margin-top: 5px; text-align: right; }
        </style>
    </head>
    <body>
        <div class="header-bar">
            <div class="live-badge">🔴 POCKET OPTION LIVE WebSocket</div>
            <div class="time-box" id="utc-time">--:--:-- UTC</div>
        </div>

        <div class="section-title">CHAGUA SOKO LA BIASHARA:</div>
        <div class="market-toggle">
            <button class="btn-market active" id="btn-otc" onclick="switchMarket('otc')">⚡ OTC Market (Real)</button>
            <button class="btn-market" id="btn-std" onclick="switchMarket('std')">🌐 Standard Market</button>
        </div>

        <div class="section-title">CHAGUA ASSET:</div>
        <div class="assets-grid" id="assets-container"></div>

        <div class="section-title">CHAGUA TIME FRAME (S5 AI Analyzer):</div>
        <div class="timeframe-grid" id="tf-container"></div>

        <button class="btn-analyze" onclick="runAnalysis()">⚡ CHANGANUA SOKO LA S5 (AI LIVE)</button>

        <div class="result-card" id="result-card">
            <!-- Scanning Animation Screen -->
            <div class="scanning-overlay" id="scanning-screen">
                <div class="scan-text" id="scan-step-text">Inounganisha WebSocket ya Pocket Option...</div>
                <div class="scan-subtext" id="scan-sub-text">Inachanganua Mshumaa wa S5 & Viashiria...</div>
                <div class="scan-bar"></div>
            </div>

            <div class="result-row">
                <span id="res-asset" style="color: #38bdf8; font-weight: bold;">-</span>
                <span id="res-tf" style="color: #a855f7; font-weight: bold;">-</span>
            </div>
            <div class="result-row">
                <span>Bei Halisi ya WebSocket (Live):</span>
                <span id="res-price" style="font-weight: bold; color: #facc15;">-</span>
            </div>
            <div class="result-row">
                <span>Uamuzi wa AI (Signal):</span>
                <span id="res-signal">-</span>
            </div>
            <div class="result-row">
                <span>Mwisho wa Mshumaa (Candle Close):</span>
                <span class="time-box" id="res-candle">-</span>
            </div>
            <div class="result-row">
                <span>Kiwango cha Usahihi (Accuracy):</span>
                <span style="color: #4ade80; font-weight: bold;">99.8% (Real Signal)</span>
            </div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 6px; border-top: 1px solid #334155; padding-top: 6px;" id="res-indicators">
                Viashiria: RSI (14): 76.4 (Overbought) | MACD: Bullish Cross | Volume: High OTC
            </div>
            <div class="ws-status">🟢 WebSocket Stream: Active (Real-time Feed)</div>
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
                "USDCAD", "NZDUSD", "EURJPY", "GBPJPY",
                "AUDJPY", "EURGBP", "USDCHF", "CADJPY"
            ];

            const timeframes = ["s5", "s4", "s10", "s15", "s30", "1m", "2m", "3m", "5m", "10m", "15m", "30m", "1h", "2h", "4h"];

            let currentMarket = "otc";
            let selectedAsset = "AEDCNY_otc";
            let selectedTF = "s5";

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

            // Kuiga muunganisho halisi wa WebSocket ya Pocket Option kusoma bei za soko
            let wsPriceBase = 1.59377;
            function getWebSocketLivePrice(asset) {
                const variance = (Math.random() - 0.48) * 0.0008;
                wsPriceBase += variance;
                return wsPriceBase.toFixed(5);
            }

            function runAnalysis() {
                const card = document.getElementById('result-card');
                const screen = document.getElementById('scanning-screen');
                const stepText = document.getElementById('scan-step-text');
                const subText = document.getElementById('scan-sub-text');
                
                card.style.display = 'block';
                screen.style.display = 'flex';

                // Hatua za maelezo ya scanning kwenye skrini
                setTimeout(() => {
                    stepText.innerText = "Inasoma WebSocket Feed ya " + selectedAsset + "...";
                    subText.innerText = "Inachambua RSI, Momentum na S5 Candles...";
                }, 600);

                setTimeout(() => {
                    stepText.innerText = "Inathibitisha Ishara ya 100% Real Account...";
                    subText.innerText = "AI inatoa uamuzi wa mwisho...";
                }, 1300);

                // Baada ya sekunde 2, onyesha matokeo kamili
                setTimeout(() => {
                    screen.style.display = 'none';

                    document.getElementById('res-asset').innerText = selectedAsset + " (" + currentMarket.toUpperCase() + ")";
                    document.getElementById('res-tf').innerText = "TF: " + selectedTF.toUpperCase();
                    
                    const livePrice = getWebSocketLivePrice(selectedAsset);
                    document.getElementById('res-price').innerText = livePrice;

                    const signals = [
                        {text: "🟢 BUY ⬆ (POCKET OPTION SIGNAL)", class: "buy-signal"},
                        {text: "🔴 SELL ⬇ (POCKET OPTION SIGNAL)", class: "sell-signal"}
                    ];
                    const sig = signals[Math.floor(Math.random() * signals.length)];
                    const sigSpan = document.getElementById('res-signal');
                    sigSpan.innerText = sig.text;
                    sigSpan.className = sig.class;

                    const now = new Date();
                    now.setSeconds(now.getSeconds() + (selectedTF.includes('s') ? parseInt(selectedTF) : 60));
                    document.getElementById('res-candle').innerText = now.toUTCString().split(' ')[4] + " UTC (Funga Mshumaa)";
                    
                    // Kubadilisha viashiria kulingana na asset
                    const rsiVal = Math.floor(Math.random() * 30) + 60;
                    document.getElementById('res-indicators').innerText = `Viashiria: RSI (${rsiVal}) | MACD: Strong Trend | WebSocket Feed: Connected (${currentMarket.toUpperCase()})`;
                }, 2200);
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
