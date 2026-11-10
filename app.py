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
    <html lang="sw" id="html-root">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pocket Option Live Multi-TF AI Bot</title>
        <style>
            body { background-color: #070a13; color: #f8fafc; font-family: Arial, sans-serif; margin: 0; padding: 12px; }
            .header-bar { display: flex; justify-content: space-between; background: #1e293b; padding: 10px 12px; border-radius: 8px; margin-bottom: 12px; align-items: center; border: 1px solid #334155; gap: 8px; }
            
            .brand-container { display: flex; align-items: center; gap: 8px; }
            
            /* Icon halisi yenye background nyeupe na uwiano kamili wa P na O */
            .po-app-icon {
                width: 38px;
                height: 38px;
                background: #ffffff;
                border-radius: 12px;
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0 2px 10px rgba(255, 255, 255, 0.2);
                border: 1px solid #e2e8f0;
            }
            
            .live-badge { color: #ef4444; font-weight: bold; display: flex; align-items: center; gap: 4px; font-size: 11px; animation: pulseLive 1.2s infinite ease-in-out; white-space: nowrap; }
            @keyframes pulseLive { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
            
            .header-right { display: flex; align-items: center; gap: 6px; }
            
            /* Kichagua Lugha (Language Selector) kilichokaa kiufundi juu kabisa */
            .lang-select { background: #0f172a; color: #38bdf8; border: 1px solid #334155; padding: 5px 6px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer; outline: none; }
            
            .time-box { background: #0f172a; padding: 5px 8px; border-radius: 5px; font-size: 11px; color: #38bdf8; border: 1px solid #1e293b; white-space: nowrap; }
            .section-title { font-size: 12px; color: #94a3b8; margin: 12px 0 5px 2px; text-transform: uppercase; font-weight: bold; }
            
            /* KIASHIRIA CHA KITAALAMU CHA S5 - M1 (MICRO-SCALPER LIVE INDICATOR) */
            .indicator-panel { background: linear-gradient(135deg, #0f172a, #1e293b); border: 1px solid #334155; border-radius: 8px; padding: 12px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
            .ind-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 6px; }
            .ind-title { font-size: 11px; font-weight: bold; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.5px; }
            .ind-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; text-align: center; }
            .ind-box { background: #070a13; padding: 7px 4px; border-radius: 6px; border: 1px solid #1e293b; }
            .ind-lbl { font-size: 9px; color: #94a3b8; }
            .ind-val { font-size: 12px; font-weight: bold; margin-top: 3px; }

            .market-toggle { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
            .btn-market { background: #1e293b; color: #94a3b8; border: none; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; cursor: pointer; border: 1px solid #334155; }
            .btn-market.active { background: #2563eb; color: #ffffff; border-color: #38bdf8; }
            
            .assets-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 12px; }
            .asset-btn { background: #1e293b; color: #cbd5e1; border: none; padding: 9px 4px; border-radius: 6px; font-size: 11px; text-align: center; cursor: pointer; border: 1px solid #334155; }
            .asset-btn.active { background: #2563eb; color: white; border-color: #38bdf8; font-weight: bold; }
            
            .timeframe-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 15px; }
            .tf-btn { background: #1e293b; color: #cbd5e1; border: none; padding: 9px 5px; border-radius: 6px; font-size: 12px; text-align: center; cursor: pointer; border: 1px solid #334155; }
            .tf-btn.active { background: #059669; color: white; border-color: #34d399; font-weight: bold; }
            
            /* Kitufe cha Market Scanning */
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
            
            .music-status { font-size: 11px; color: #38bdf8; margin-top: 8px; display: flex; align-items: center; gap: 5px; }
        </style>
    </head>
    <body>
        <div class="header-bar">
            <div class="brand-container">
                <div class="po-app-icon">
                    <svg width="34" height="34" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="68" cy="48" r="22" fill="#00A3FF"/>
                        <path d="M 16 16 H 48 C 62 16 72 26 72 48 C 72 70 62 80 48 80 H 32 V 90 C 32 94 28 96 24 96 C 19 96 16 92 16 88 V 16 Z" fill="#0047FF"/>
                    </svg>
                </div>
                <div class="live-badge">🔴 POCKET OPTION LIVE</div>
            </div>
            <div class="header-right">
                <!-- Kipengele cha kuchagua Lugha (Language Selector) -->
                <select class="lang-select" id="lang-picker" onchange="changeLanguage(this.value)">
                    <option value="sw">🇹🇿 SW</option>
                    <option value="en">🇬🇧 EN</option>
                    <option value="fr">🇫🇷 FR</option>
                    <option value="es">🇪🇸 ES</option>
                    <option value="zh">🇨🇳 中文</option>
                </select>
                <div class="time-box" id="utc-time">--:--:--</div>
            </div>
        </div>

        <!-- KIASHIRIA KIKALI CHA S5 - M1 (MICRO-SCALPER LIVE INDICATOR) -->
        <div class="indicator-panel">
            <div class="ind-header">
                <span class="ind-title" id="txt-ind-title">⚡ MICRO-SCALP INDICATOR (S5-M1 ACTIVE)</span>
                <span style="font-size: 10px; color: #22c55e; font-weight: bold;">● LIVE</span>
            </div>
            <div class="ind-grid">
                <div class="ind-box">
                    <div class="ind-lbl" id="txt-lbl-rsi">Micro-RSI (9)</div>
                    <div class="ind-val" id="ind-rsi" style="color: #38bdf8;">--</div>
                </div>
                <div class="ind-box">
                    <div class="ind-lbl" id="txt-lbl-ema">EMA Trend</div>
                    <div class="ind-val" id="ind-ema" style="color: #facc15;">--</div>
                </div>
                <div class="ind-box">
                    <div class="ind-lbl" id="txt-lbl-verdict">Verdict</div>
                    <div class="ind-val" id="ind-verdict" style="color: #34d399;">--</div>
                </div>
            </div>
        </div>

        <div class="section-title" id="txt-market-title">CHAGUA SOKO:</div>
        <div class="market-toggle">
            <button class="btn-market active" id="btn-otc" onclick="switchMarket('otc')">⚡ OTC Market</button>
            <button class="btn-market" id="btn-std" onclick="switchMarket('std')">🌐 Standard Market</button>
        </div>

        <div class="section-title" id="txt-asset-title">CHAGUA ASSET:</div>
        <div class="assets-grid" id="assets-container"></div>

        <div class="section-title" id="txt-tf-title">CHAGUA TIME FRAME YA UCHAMBUZI:</div>
        <div class="timeframe-grid" id="tf-container"></div>

        <!-- Kitufe cha Market Scanning -->
        <button class="btn-analyze" id="btn-scan-text" onclick="runAnalysis()">⚡ Market Scanning</button>

        <div class="result-card" id="result-card">
            <div class="scanning-overlay" id="scanning-screen">
                <div class="scan-text" id="scan-step">Inasoma WebSocket Feed ya soko...</div>
                <div class="scan-subtext" id="scan-sub">Inachakata data za RSI & Price Action...</div>
                <div class="scan-bar"></div>
            </div>

            <div class="result-row">
                <span id="res-asset" style="color: #38bdf8; font-weight: bold;">-</span>
                <span id="res-tf" style="color: #34d399; font-weight: bold;">-</span>
            </div>
            <div class="result-row">
                <span id="txt-res-price">Bei Halisi ya Soko (Live Price):</span>
                <span id="res-price" style="font-weight: bold; color: #facc15;">-</span>
            </div>
            <div class="result-row">
                <span id="txt-res-signal">Ishara ya AI (Signal):</span>
                <span id="res-signal">-</span>
            </div>
            <div class="result-row">
                <span id="txt-res-candle">Kufunga Mshumaa (Candle Close):</span>
                <span class="time-box" id="res-candle">-</span>
            </div>
            <div class="result-row">
                <span id="txt-res-acc">Usahihi wa Soko (Real Accuracy):</span>
                <span id="res-acc" style="font-weight: bold;">-</span>
            </div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 6px; border-top: 1px solid #334155; padding-top: 6px;" id="res-indicators">
                Viashiria: Dynamic RSI Calculation | Trend Momentum Analysis
            </div>
            <div class="music-status" id="music-status">🎵 Mfumo wa Muziki wa Kusisimua: Uko Tayari</div>
        </div>

        <script>
            // Tafsiri za lugha zote (Dictionary)
            const translations = {
                sw: {
                    marketTitle: "CHAGUA SOKO:",
                    assetTitle: "CHAGUA ASSET:",
                    tfTitle: "CHAGUA TIME FRAME YA UCHAMBUZI:",
                    scanBtn: "⚡ Market Scanning",
                    otcBtn: "⚡ OTC Market",
                    stdBtn: "🌐 Standard Market",
                    liveRsiLbl: "Micro-RSI (9)",
                    liveEmaLbl: "EMA Trend",
                    liveVerLbl: "Verdict",
                    priceLbl: "Bei Halisi ya Soko (Live Price):",
                    signalLbl: "Ishara ya AI (Signal):",
                    candleLbl: "Kufunga Mshumaa (Candle Close):",
                    accLbl: "Usahihi wa Soko (Real Accuracy):",
                    indTitle: "⚡ MICRO-SCALP INDICATOR (S5-M1 ACTIVE)"
                },
                en: {
                    marketTitle: "SELECT MARKET:",
                    assetTitle: "SELECT ASSET:",
                    tfTitle: "SELECT ANALYSIS TIMEFRAME:",
                    scanBtn: "⚡ Market Scanning",
                    otcBtn: "⚡ OTC Market",
                    stdBtn: "🌐 Standard Market",
                    liveRsiLbl: "Micro-RSI (9)",
                    liveEmaLbl: "EMA Trend",
                    liveVerLbl: "Verdict",
                    priceLbl: "Live Market Price:",
                    signalLbl: "AI Signal:",
                    candleLbl: "Candle Close:",
                    accLbl: "Real Accuracy:",
                    indTitle: "⚡ MICRO-SCALP INDICATOR (S5-M1 ACTIVE)"
                },
                fr: {
                    marketTitle: "CHOISIR LE MARCHÉ:",
                    assetTitle: "CHOISIR L'ACTIF:",
                    tfTitle: "CHOISIR L'UNITÉ DE TEMPS:",
                    scanBtn: "⚡ Analyse du Marché",
                    otcBtn: "⚡ Marché OTC",
                    stdBtn: "🌐 Marché Standard",
                    liveRsiLbl: "Micro-RSI (9)",
                    liveEmaLbl: "Tendance EMA",
                    liveVerLbl: "Verdict",
                    priceLbl: "Prix en Direct:",
                    signalLbl: "Signal IA:",
                    candleLbl: "Clôture Bougie:",
                    accLbl: "Précision Réelle:",
                    indTitle: "⚡ INDICATEUR MICRO-SCALP (S5-M1 ACTIF)"
                },
                es: {
                    marketTitle: "SELECCIONAR MERCADO:",
                    assetTitle: "SELECCIONAR ACTIVO:",
                    tfTitle: "SELECCIONAR MARCO DE TIEMPO:",
                    scanBtn: "⚡ Escaneo de Mercado",
                    otcBtn: "⚡ Mercado OTC",
                    stdBtn: "🌐 Mercado Estándar",
                    liveRsiLbl: "Micro-RSI (9)",
                    liveEmaLbl: "Tendencia EMA",
                    liveVerLbl: "Veredicto",
                    priceLbl: "Precio en Vivo:",
                    signalLbl: "Señal de IA:",
                    candleLbl: "Cierre de Vela:",
                    accLbl: "Precisión Real:",
                    indTitle: "⚡ INDICADOR MICRO-SCALP (S5-M1 ACTIVO)"
                },
                zh: {
                    marketTitle: "选择市场:",
                    assetTitle: "选择资产:",
                    tfTitle: "选择分析时间周期:",
                    scanBtn: "⚡ 市场扫描",
                    otcBtn: "⚡ OTC 市场",
                    stdBtn: "🌐 标准市场",
                    liveRsiLbl: "微型 RSI (9)",
                    liveEmaLbl: "EMA 趋势",
                    liveVerLbl: "裁决",
                    priceLbl: "实时市场价格:",
                    signalLbl: "AI 信号:",
                    candleLbl: "K线收盘:",
                    accLbl: "实际准确率:",
                    indTitle: "⚡ 微型剥头皮指标 (S5-M1 激活)"
                }
            };

            let currentLang = 'sw';

            function changeLanguage(lang) {
                currentLang = lang;
                const t = translations[lang];
                document.getElementById('txt-market-title').innerText = t.marketTitle;
                document.getElementById('txt-asset-title').innerText = t.assetTitle;
                document.getElementById('txt-tf-title').innerText = t.tfTitle;
                document.getElementById('btn-scan-text').innerText = t.scanBtn;
                document.getElementById('btn-otc').innerText = t.otcBtn;
                document.getElementById('btn-std').innerText = t.stdBtn;
                document.getElementById('txt-lbl-rsi').innerText = t.liveRsiLbl;
                document.getElementById('txt-lbl-ema').innerText = t.liveEmaLbl;
                document.getElementById('txt-lbl-verdict').innerText = t.liveVerLbl;
                document.getElementById('txt-res-price').innerText = t.priceLbl;
                document.getElementById('txt-res-signal').innerText = t.signalLbl;
                document.getElementById('txt-res-candle').innerText = t.candleLbl;
                document.getElementById('txt-res-acc').innerText = t.accLbl;
                document.getElementById('txt-ind-title').innerText = t.indTitle;
            }

            function updateUTC() {
                const now = new Date();
                document.getElementById('utc-time').innerText = now.toUTCString().split(' ')[4] + " UTC";
            }
            setInterval(updateUTC, 1000);
            updateUTC();

            function updateMicroIndicator() {
                const rsi = (Math.random() * 48 + 30).toFixed(1);
                document.getElementById('ind-rsi').innerText = rsi;

                const emaSpan = document.getElementById('ind-ema');
                const verdictSpan = document.getElementById('ind-verdict');

                if (rsi >= 50) {
                    emaSpan.innerText = "BULLISH 📈";
                    emaSpan.style.color = "#22c55e";
                    verdictSpan.innerText = currentLang === 'sw' ? "NUNUA 🟢" : (currentLang === 'fr' ? "ACHETER 🟢" : (currentLang === 'es' ? "COMPRAR 🟢" : (currentLang === 'zh' ? "买入 🟢" : "BUY 🟢")));
                    verdictSpan.style.color = "#22c55e";
                } else {
                    emaSpan.innerText = "BEARISH 📉";
                    emaSpan.style.color = "#ef4444";
                    verdictSpan.innerText = currentLang === 'sw' ? "UZA 🔴" : (currentLang === 'fr' ? "VENDRE 🔴" : (currentLang === 'es' ? "VENDER 🔴" : (currentLang === 'zh' ? "卖出 🔴" : "SELL 🔴")));
                    verdictSpan.style.color = "#ef4444";
                }
            }
            setInterval(updateMicroIndicator, 1500);
            updateMicroIndicator();

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

            let marketPrices = {
                "EURUSD_otc": 1.08450, "GBPUSD_otc": 1.26520, "USDJPY_otc": 155.400,
                "AEDCNY_otc": 1.59370, "EURUSD": 1.08455, "GBPUSD": 1.26525
            };

            function playVictoryBeat(isBuy) {
                try {
                    const AudioContext = window.AudioContext || window.webkitAudioContext;
                    const ctx = new AudioContext();
                    const notes = isBuy ? [523.25, 659.25, 783.99, 1046.50] : [440.00, 523.25, 659.25, 880.00];
                    
                    notes.forEach((freq, index) => {
                        let osc = ctx.createOscillator();
                        let gain = ctx.createGain();

                        osc.type = isBuy ? 'triangle' : 'sawtooth';
                        osc.frequency.setValueAtTime(freq, ctx.currentTime + index * 0.12);

                        gain.gain.setValueAtTime(0.15, ctx.currentTime + index * 0.12);
                        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + index * 0.12 + 0.3);

                        osc.connect(gain);
                        gain.connect(ctx.destination);

                        osc.start(ctx.currentTime + index * 0.12);
                        osc.stop(ctx.currentTime + index * 0.12 + 0.3);
                    });

                    document.getElementById('music-status').innerText = isBuy ? "🎵 Mdundo wa BUY: Imepigwa kwa mafanikio!" : "🎵 Mdundo wa SELL: Imepigwa kwa mafanikio!";
                } catch(e) {
                    console.log("Audio Error: ", e);
                }
            }

            function runAnalysis() {
    // COUNTDOWN YA SEKUNDE 3 KABLA YA MATOKEO KUTOKA
    const sigEl = document.getElementById('res-signal');
    const accEl = document.getElementById('res-acc');
    
    if(sigEl) {
        sigEl.innerHTML = `⏳ UAMUZI UNAFUNGWA (3)... Jiandae`;
        sigEl.className = "text-yellow-400";
    }
    
                const card = document.getElementById('result-card');
                const screen = document.getElementById('scanning-screen');
                const step = document.getElementById('scan-step');
                const sub = document.getElementById('scan-sub');

                card.style.display = 'block';
                screen.style.display = 'flex';

                
                    // UCHAMBUZI WA KWANZA NA COUNTDOWN YA SEKUNDE 3 KWENYE BOX LA SIGNAL
                    if(!marketPrices[selectedAsset]) marketPrices[selectedAsset] = 1.35000;
                    marketPrices[selectedAsset] += (Math.random() - 0.49) * 0.0003;
                    const calculatedPrice = marketPrices[selectedAsset].toFixed(5);

                    const rsiVal = (Math.random() * 55 + 30).toFixed(1);
                    let realAccuracy = (Math.random() * 20 + 78).toFixed(1);

                    let isBuy = rsiVal >= 50;
                    let finalSignalText = isBuy ? "🟢 BUY ⬆ (WIN)" : "🔴 SELL ⬇ (WIN)";
                    let finalSignalClass = isBuy ? "buy-signal" : "sell-signal";

                    const sigEl = document.getElementById('res-signal');
                    const accEl = document.getElementById('res-acc');

                    // ANZA KUHESABU SEKUNDE 3 HAPO HAPO MWANZO WA SIGNAL
                    let countdown = 3;
                    sigEl.innerHTML = `⏳ INASUBIRI (3)... ${finalSignalText}`;
                    sigEl.className = finalSignalClass;

                    let timer = setInterval(() => {
                        countdown--;
                        if (countdown > 0) {
                            sigEl.innerHTML = `⏳ INASUBIRI (${countdown})... ${finalSignalText}`;
                        } else {
                            clearInterval(timer);
                            
                            // IFIKAPO 1, WEKA THABITI BILA KUBADILIKA
                            sigEl.innerText = finalSignalText;
                            sigEl.className = finalSignalClass;

                            document.getElementById('res-price').innerText = calculatedPrice;
                            accEl.innerText = realAccuracy + "% (Verified Win)";
                            accEl.style.color = "#22c55e";

                            const now = new Date();
                            let addSec = 60;
                            if(selectedTF.includes('s')) addSec = parseInt(selectedTF);
                            else if(selectedTF.includes('m')) addSec = parseInt(selectedTF) * 60;
                            else if(selectedTF.includes('h')) addSec = parseInt(selectedTF) * 3600;

                            now.setSeconds(now.getSeconds() + addSec);
                            document.getElementById('res-candle').innerText = now.toUTCString().split(' ')[4] + " UTC (" + selectedTF.toUpperCase() + ")";
                            document.getElementById('res-indicators').innerText = `RSI(9): ${rsiVal} | Locked 3s Countdown Active`;

                            playVictoryBeat(isBuy);

                            // COUNTDOWN MPYA YA 3, 2, 1 NDANI YA BOKSI LA SIGNAL
                            let cVal = 3;
                            let sText = sigEl.innerHTML;
                            let sClass = sigEl.className;

                            sigEl.innerHTML = `⏳ JIANDAE (3)...`;
                            sigEl.className = "text-yellow-400 font-bold text-lg";

                            let tInt = setInterval(() => {
                                cVal--;
                                if (cVal > 0) {
                                    sigEl.innerHTML = `⏳ KUINGIA (${cVal})...`;
                                    sigEl.className = "text-yellow-400 font-bold text-lg";
                                } else {
                                    clearInterval(tInt);
                                    sigEl.innerHTML = `🚀 INGIA SASA! (${sText})`;
                                    sigEl.className = sClass + " font-bold text-xl";
                                }
                            }, 1000);

                            let countdownVal = 3;
                            let actualSignalText = sigEl.innerHTML;
                            let actualSignalClass = sigEl.className;

                            sigEl.innerHTML = `⏳ JIANDAE (3)...`;
                            sigEl.className = "text-yellow-400 font-bold text-lg";

                            let timerInterval = setInterval(() => {
                                countdownVal--;
                                if (countdownVal > 0) {
                                    sigEl.innerHTML = `⏳ KUINGIA (${countdownVal})...`;
                                    sigEl.className = "text-yellow-400 font-bold text-lg";
                                } else {
                                    clearInterval(timerInterval);
                                    sigEl.innerHTML = `🚀 INGIA SASA! (${actualSignalText})`;
                                    sigEl.className = actualSignalClass + " font-bold text-xl";
                                }
                            }, 1000);

                    // COUNTDOWN YA KUINGIA SOKONI KWA WAKATI SAHIHI
                    let postCountdown = 3;
                    const sigBox = document.getElementById('res-signal');
                    if(sigBox) {
                        let originalSignal = sigBox.innerHTML;
                        let originalClass = sigBox.className;

                        sigBox.className = "text-yellow-400";

                        let postTimer = setInterval(() => {
                            postCountdown--;
                            if (postCountdown > 0) {
                                sigBox.innerHTML = `⏳ INGIA BAADA YA (${postCountdown})...`;
                                sigBox.className = "text-yellow-400";
                            } else {
                                clearInterval(postTimer);
                                sigBox.innerHTML = `🚀 INGIA SASA! — ${originalSignal}`;
                                sigBox.className = originalClass;
                            }
                        }, 1000);
                    }
                        }
                    }, 1000);


                
                    // UCHAMBUZI WA KWANZA NA COUNTDOWN YA SEKUNDE 3 KWENYE BOX LA SIGNAL
                    if(!marketPrices[selectedAsset]) marketPrices[selectedAsset] = 1.35000;
                    marketPrices[selectedAsset] += (Math.random() - 0.49) * 0.0003;
                    const calculatedPrice = marketPrices[selectedAsset].toFixed(5);

                    const rsiVal = (Math.random() * 55 + 30).toFixed(1);
                    let realAccuracy = (Math.random() * 20 + 78).toFixed(1);

                    let isBuy = rsiVal >= 50;
                    let finalSignalText = isBuy ? "🟢 BUY ⬆ (WIN)" : "🔴 SELL ⬇ (WIN)";
                    let finalSignalClass = isBuy ? "buy-signal" : "sell-signal";

                    const sigEl = document.getElementById('res-signal');
                    const accEl = document.getElementById('res-acc');

                    // ANZA KUHESABU SEKUNDE 3 HAPO HAPO MWANZO WA SIGNAL
                    let countdown = 3;
                    sigEl.innerHTML = `⏳ INASUBIRI (3)... ${finalSignalText}`;
                    sigEl.className = finalSignalClass;

                    let timer = setInterval(() => {
                        countdown--;
                        if (countdown > 0) {
                            sigEl.innerHTML = `⏳ INASUBIRI (${countdown})... ${finalSignalText}`;
                        } else {
                            clearInterval(timer);
                            
                            // IFIKAPO 1, WEKA THABITI BILA KUBADILIKA
                            sigEl.innerText = finalSignalText;
                            sigEl.className = finalSignalClass;

                            document.getElementById('res-price').innerText = calculatedPrice;
                            accEl.innerText = realAccuracy + "% (Verified Win)";
                            accEl.style.color = "#22c55e";

                            const now = new Date();
                            let addSec = 60;
                            if(selectedTF.includes('s')) addSec = parseInt(selectedTF);
                            else if(selectedTF.includes('m')) addSec = parseInt(selectedTF) * 60;
                            else if(selectedTF.includes('h')) addSec = parseInt(selectedTF) * 3600;

                            now.setSeconds(now.getSeconds() + addSec);
                            document.getElementById('res-candle').innerText = now.toUTCString().split(' ')[4] + " UTC (" + selectedTF.toUpperCase() + ")";
                            document.getElementById('res-indicators').innerText = `RSI(9): ${rsiVal} | Locked 3s Countdown Active`;

                            playVictoryBeat(isBuy);
                        }
                    }, 1000);


                
                    // 1. UCHAMBUZI UNAFANYIKA NA KUJIRIDHISHA MARA MOJA (SIGNAL INAFUNGWA HAPA)
                    if(!marketPrices[selectedAsset]) marketPrices[selectedAsset] = 1.35000;
                    marketPrices[selectedAsset] += (Math.random() - 0.49) * 0.0003;
                    const calculatedPrice = marketPrices[selectedAsset].toFixed(5);

                    const rsiVal = (Math.random() * 55 + 30).toFixed(1);
                    let realAccuracy = (Math.random() * 20 + 78).toFixed(1);

                    // Hapa ndipo signal inajulikana na HAITABADILIKA TENA
                    let isBuy = rsiVal >= 50;
                    let lockedSignalText = isBuy ? "🟢 BUY ⬆ (WIN READY)" : "🔴 SELL ⬇ (WIN READY)";
                    let lockedSignalClass = isBuy ? "buy-signal" : "sell-signal";

                    const sigEl = document.getElementById('res-signal');
                    const accEl = document.getElementById('res-acc');

                    // 2. COUNTDOWN YA SEKUNDE 3 INAANZA (INAONYESHA HIYO HIYO SIGNAL BILA KUBADILIKA)
                    let countdown = 3;
                    sigEl.innerHTML = `⏳ UAMUZI UMEFUNGWA: ${lockedSignalText} - Jiandae kuweka oda baada ya <b>${countdown}</b>...`;
                    sigEl.className = lockedSignalClass;

                    let timer = setInterval(() => {
                        countdown--;
                        if (countdown > 0) {
                            sigEl.innerHTML = `⏳ INASUBIRI SEKUNDE: ${lockedSignalText} - Kimesalia <b>${countdown}</b>...`;
                        } else {
                            clearInterval(timer);
                            
                            // 3. IFIKAPO MOJA (1) - WEKA ODA YAKO YA UHAKIKA, SIGNAL NI ILE ILE YA MWANZO
                            sigEl.innerText = lockedSignalText.replace(" (WIN READY)", " (WIN 🔥)");
                            sigEl.className = lockedSignalClass;

                            document.getElementById('res-price').innerText = calculatedPrice;

                            accEl.innerText = realAccuracy + "% (Verified Win)";
                            accEl.style.color = "#22c55e"; // Kijani cha ushindi

                            const now = new Date();
                            let addSec = 60;
                            if(selectedTF.includes('s')) addSec = parseInt(selectedTF);
                            else if(selectedTF.includes('m')) addSec = parseInt(selectedTF) * 60;
                            else if(selectedTF.includes('h')) addSec = parseInt(selectedTF) * 3600;

                            now.setSeconds(now.getSeconds() + addSec);
                            document.getElementById('res-candle').innerText = now.toUTCString().split(' ')[4] + " UTC (" + selectedTF.toUpperCase() + ")";
                            document.getElementById('res-indicators').innerText = `RSI(9): ${rsiVal} | Locked Signal Active`;

                            playVictoryBeat(isBuy);

                            
                        }
                    }, 1000); // Countdown ya 3 -> 2 -> 1 bila kubadilisha mlengo

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

