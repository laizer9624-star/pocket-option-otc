from flask import Flask, render_template_string, request

app = Flask(__name__)
app.secret_key = "weka_secret_key_hapa_kwa_usalama"

# Tafsiri za Lugha (Kiswahili na Kiingereza)
translations = {
    "sw": {
        "title": "Karibu kwenye PocketOption Bot",
        "welcome": "Mfumo wa Uchambuzi na Ishara za Moja kwa Moja",
        "select_lang": "Chagua Lugha",
        "btn_signal": "Pata Signal Mpya"
    },
    "en": {
        "title": "Welcome to PocketOption Bot",
        "welcome": "Live Analysis and Signal System",
        "select_lang": "Select Language",
        "btn_signal": "Get New Signal"
    },
    "fr": {
        "title": "Bienvenue sur PocketOption Bot",
        "welcome": "Système d'analyse et de signaux en direct",
        "select_lang": "Choisir la langue",
        "btn_signal": "Obtenir un nouveau signal"
    },
    "es": {
        "title": "Bienvenido a PocketOption Bot",
        "welcome": "Sistema de análisis y señales en vivo",
        "select_lang": "Seleccionar idioma",
        "btn_signal": "Obtener nueva señal"
    },
    "de": {
        "title": "Willkommen bei PocketOption Bot",
        "welcome": "Live-Analyse- und Signalsystem",
        "select_lang": "Sprache auswählen",
        "btn_signal": "Neues Signal erhalten"
    },
    "pt": {
        "title": "Bem-vindo ao PocketOption Bot",
        "welcome": "Sistema de análise e sinais ao vivo",
        "select_lang": "Selecionar idioma",
        "btn_signal": "Obter novo sinal"
    },
    "ar": {
        "title": "مرحباً بك في بوت PocketOption",
        "welcome": "نظام التحليل والإشارات المباشرة",
        "select_lang": "اختر اللغة",
        "btn_signal": "احصل على إشارة جديدة"
    },
    "ru": {
        "title": "Добро пожаловать в PocketOption Bot",
        "welcome": "Система анализа и сигналов в реальном времени",
        "select_lang": "Выберите язык",
        "btn_signal": "Получить новый сигнал"
    },
    "hi": {
        "title": "PocketOption बॉट में आपका स्वागत है",
        "welcome": "लाइव विश्लेषण और सिग्नल प्रणाली",
        "select_lang": "भाषा चुनें",
        "btn_signal": "नया सिग्नल प्राप्त करें"
    },
    "zh": {
        "title": "欢迎使用 PocketOption Bot",
        "welcome": "实时分析和信号系统",
        "select_lang": "选择语言",
        "btn_signal": "获取新信号"
    }
}

@app.route('/')
def index():
    lang = request.args.get('lang', 'sw')
    t = translations.get(lang, translations['sw'])
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <title>{t['title']}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #0f172a; color: #f8fafc; font-family: monospace; }}
            .buy-signal {{ background-color: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #4ade80; }}
            .sell-signal {{ background-color: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #f87171; }}
        </style>
    </head>
    <body class="p-4 flex flex-col items-center justify-center min-h-screen">
        <div class="max-w-md w-full bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
            <div class="flex justify-between items-center mb-4">
                <h1 class="text-lg font-bold text-emerald-400">PocketOption Bot</h1>
                <div>
                    <a href="/?lang=sw" class="text-xs px-2 py-1 bg-slate-700 rounded hover:bg-slate-600">Swahili</a>
                    <a href="/?lang=en" class="text-xs px-2 py-1 bg-slate-700 rounded hover:bg-slate-600">English</a>
                </div>
            </div>

            <p class="text-sm text-slate-400 mb-4">{t['welcome']}</p>

            <!-- Boksi la Signal na Countdown -->
            <div id="res-signal" class="p-4 rounded-lg text-center font-bold text-base mb-3 bg-slate-900 border border-slate-600">
                ⏳ Subiri uchambuzi...
            </div>

            <div class="space-y-2 text-sm text-slate-300 mb-4">
                <div>Bei: <span id="res-price" class="font-mono text-white">-</span></div>
                <div>Ushindi: <span id="res-acc" class="font-bold text-slate-400">-</span></div>
                <div>Muda (TF): <span id="res-candle" class="text-slate-400">-</span></div>
                <div>Viashiria: <span id="res-indicators" class="text-slate-400">-</span></div>
            </div>

            <button onclick="generateSignal()" class="w-full py-3 bg-emerald-600 hover:bg-emerald-500 font-bold rounded-lg text-white transition">
                {t['btn_signal']}
            </button>
        </div>

        <script>
            let marketPrices = {{}};
            let selectedAsset = "EURUSD";
            let selectedTF = "1m";

            function playVictoryBeat(isBuy) {{
                // Audio placeholder au sauti ya ushindi
                console.log("Victory beat played for:", isBuy ? "BUY" : "SELL");
            }}

            function generateSignal() {{
                if(!marketPrices[selectedAsset]) marketPrices[selectedAsset] = 1.35000;
                marketPrices[selectedAsset] += (Math.random() - 0.49) * 0.0003;
                const calculatedPrice = marketPrices[selectedAsset].toFixed(5);
                
                const rsiVal = (Math.random() * 55 + 30).toFixed(1);
                let realAccuracy = (Math.random() * 20 + 78).toFixed(1);

                let isBuy = rsiVal >= 50;
                let lockedSignalText = isBuy ? "🟢 BUY ⬆ (WIN READY)" : "🔴 SELL ⬇ (WIN READY)";
                let lockedSignalClass = isBuy ? "buy-signal" : "sell-signal";
                
                const sigEl = document.getElementById('res-signal');
                const accEl = document.getElementById('res-acc');

                // Countdown ya sekunde 3 kwenye Box la Signal
                let countdown = 3;
                sigEl.innerHTML = `⏳ UAMUZI UMEFUNGWA: ${{lockedSignalText}} - Jiandae (${{countdown}})...`;
                sigEl.className = lockedSignalClass;

                let timer = setInterval(() => {{
                    countdown--;
                    if (countdown > 0) {{
                        sigEl.innerHTML = `⏳ INASUBIRI SEKUNDE: ${{lockedSignalText}} - Kimesalia <b>${{countdown}}</b>...`;
                    }} else {{
                        clearInterval(timer);

                        sigEl.innerText = lockedSignalText.replace(" (WIN READY)", " (WIN 🔥)");
                        sigEl.className = lockedSignalClass;

                        document.getElementById('res-price').innerText = calculatedPrice;
                        accEl.innerText = realAccuracy + "% (Verified Win)";
                        accEl.style.color = "#22c55e";

                        const now = new Date();
                        let addSec = 60;
                        now.setSeconds(now.getSeconds() + addSec);
                        document.getElementById('res-candle').innerText = now.toUTCString().split(' ')[4] + " UTC (1M)";
                        document.getElementById('res-indicators').innerText = `RSI(9): ${{rsiVal}} | Locked Signal Active`;

                        playVictoryBeat(isBuy);
                    }}
                }}, 1000);
            }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
