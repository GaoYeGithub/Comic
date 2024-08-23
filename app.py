import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/generate-comic', methods=['POST'])
def generate_comic():
    api_key = "API-key"
    prompt = request.json.get('prompt')

    try:
        response = requests.post(
            'https://stablehorde.net/api/v2/generate/async',
            headers={'apikey': api_key},
            json={
                "prompt": prompt,
                "params": {
                    "samples": 1,
                    "width": 768,
                    "height": 1024
                },
                "nsfw": False,
                "censor_nsfw": False,
                "trusted_workers": True
            }
        )
        response.raise_for_status()
        task_id = response.json().get('id')
        max_attempts = 30
        for attempt in range(max_attempts):
            check_response = requests.get(
                f'https://stablehorde.net/api/v2/generate/check/{task_id}',
                headers={'apikey': api_key}
            )
            check_response.raise_for_status()
            status = check_response.json()
            
            if status.get('done'):
                result_response = requests.get(
                    f'https://stablehorde.net/api/v2/generate/status/{task_id}',
                    headers={'apikey': api_key}
                )
                result_response.raise_for_status()
                return jsonify(result_response.json())
            
            time.sleep(5)

        return jsonify({"error": "Timeout: Image generation took too long"}), 504

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if e.response.status_code == 401:
            return jsonify({"error": "Unauthorized: Invalid API key"}), 401
        return jsonify({"error": f"Failed to generate comic: {str(e)}"}), 500

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)