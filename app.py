from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        # Get MAC address from form and clean it
        mac_input = request.form['mac']
        mac_cleaned = mac_input.replace(':', '').replace('-', '')

        # Use free API to find vendor
        url = f"https://api.macvendors.com/{mac_cleaned}"
        response = requests.get(url)
        
        if response.status_code == 200:
            result = {
                'mac': mac_input,
                'vendor': response.text
            }
        else:
            result = {'error': 'Invalid MAC address or vendor not found'}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)