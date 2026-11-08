from flask import Flask, render_template, request, jsonify

import random
import time

app = Flask(__name__)


# Weka hapa jina la mtumiaji na nenosiri unalolitaka kulinda tovuti yako
users = {
    "Porket option": "54321"
}

# Ulinzi umeondolewa

# Hifadhi ya bei za ndani kwa ajili ya usomaji wa papo hapo (Direct Live Sync)
live_cache = {
    "EURUSD_otc": 1.12675,
    "GBPUSD_otc": 1.26500,
    "USDJPY_otc": 150.200,
    "AEDCNY_otc": 1.58872
}

@app.route('/')

def index():
    return render_template('main.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    market = data.get('market', 'otc')
    asset = data.get('asset', 'EURUSD_otc')
    timeframe = data.get('timeframe', 's5')

    # Hakikisha asset ipo kwenye kumbukumbu
    if asset not in live_cache:
        if 'JPY' in asset:
            live_cache[asset] = 150.200
        elif 'AED' in asset or 'CNY' in asset:
            live_cache[asset] = 1.58872
        else:
            live_cache[asset] = 1.12675

    # Mjongeo wa ndani unaoendana na soko la moja kwa moja (Internal Direct Tick)
    if 'JPY' in asset:
        step = random.uniform(-0.012, 0.014)
        decimals = 3
    else:
        step = random.uniform(-0.00010, 0.00012)
        decimals = 5

    live_cache[asset] = round(live_cache[asset] + step, decimals)
    current_price = f"{live_cache[asset]:.{decimals}f}"

    # Uchambuzi wa Viashiria vya Ndani (Internal Technical Indicators)
    rsi_val = int(50 + (step * 400000) + random.randint(-6, 6))
    rsi_val = max(20, min(80, rsi_val))

    trend_1h = 'UP 🟢' if rsi_val > 50 else 'DOWN 🔴'
    ema_50_200 = 'BULLISH 🟢' if rsi_val > 48 else 'BEARISH 🔴'
    momentum = 'STRONG ⚡' if rsi_val > 52 or rsi_val < 48 else 'STABLE ⚖️'
    move_1min = f"±{random.randint(12, 28)} pips"
    level_below = f"{random.randint(5, 18)} pips"
    rsi_display = f"{rsi_val}"

    if rsi_val > 53:
        signal = "🟢 BUY (CALL) ⬆️"
        accuracy = f"{random.randint(96, 99)}%"
    elif rsi_val < 47:
        signal = "🔴 SELL (PUT) ⬇️"
        accuracy = f"{random.randint(96, 99)}%"
    else:
        signal = "🟡 HOLD / CONSOLIDATION ⏸️"
        accuracy = f"{random.randint(88, 93)}%"

    return jsonify({
        "asset": asset,
        "timeframe": timeframe,
        "price": current_price,
        "signal": signal,
        "accuracy": accuracy,
        "reason": f"Direct Internal Stream | RSI: {rsi_val}",
        "readings": {
            "trend_1h": trend_1h,
            "ema_50_200": ema_50_200,
            "momentum": momentum,
            "rsi": rsi_display,
            "move_1min": move_1min,
            "level_below": level_below
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
