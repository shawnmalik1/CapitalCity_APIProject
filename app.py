from flask import Flask, jsonify, request
from functools import wraps
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz
import pandas as pd

app = Flask(__name__)
API_TOKEN = "supersecrettoken123"

# Load capital cities and determine timezones
df = pd.read_csv("worldcities.csv")
df = df[df["capital"] == "primary"][["city", "lat", "lng"]].dropna()
tf = TimezoneFinder()

CAPITAL_TIMEZONES = {}
for _, row in df.iterrows():
    city = row["city"]
    lat = row["lat"]
    lng = row["lng"]
    tz = tf.timezone_at(lat=lat, lng=lng)
    if tz:
        CAPITAL_TIMEZONES[city] = tz

# Token protection
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    return decorator

@app.route('/')
def index():
    return "This is the Capital Time API. Use /api/time?city=CapitalName to get the time for a capital city."

@app.route('/api/time', methods=['GET'])
@token_required
def get_time():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing 'city' query parameter"}), 400

    timezone_str = CAPITAL_TIMEZONES.get(city)
    if not timezone_str:
        return jsonify({"error": f"City '{city}' not found in database"}), 404

    try:
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        utc_offset = now.strftime('%z')
        utc_offset_formatted = f"{utc_offset[:3]}:{utc_offset[3:]}"
        return jsonify({
            "city": city,
            "local_time": now.strftime('%Y-%m-%d %H:%M:%S'),
            "utc_offset": utc_offset_formatted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
