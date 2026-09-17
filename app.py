from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    vendor = None
    error = None
    mac = ""
    if request.method == 'POST':
        mac = request.form.get('mac', '').strip()
        if mac:
            try:
                # Use a more reliable free API
                clean_mac = mac.replace(':', '').replace('-', '').upper()[:6]
                url = f"https://api.macvendors.com/{mac}"
                r = requests.get(url, timeout=10)
                if r.status_code == 200 and "errors" not in r.text.lower():
                    vendor = r.text.strip()
                else:
                    # Fallback API
                    url2 = f"https://www.macvendorlookup.com/api/v2/{mac}"
                    r2 = requests.get(url2, timeout=10)
                    if r2.status_code == 200:
                        data = r2.json()
                        if data and len(data) > 0:
                            vendor = data[0].get('company', 'Not Found')
                        else:
                            error = "Invalid MAC address or vendor not found"
                    else:
                        error = "Invalid MAC address or vendor not found"
            except Exception as e:
                error = "Invalid MAC address or vendor not found"

    return render_template('index.html', vendor=vendor, error=error, mac=mac)

if __name__ == '__main__':
    app.run(debug=True)
