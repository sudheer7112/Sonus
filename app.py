# A Flask application to serve a music discovery tool using the JioSaavn API.
from flask import Flask, render_template, request, jsonify
import requests
import json
import urllib.parse
import urllib3

# Disable SSL warnings for the API calls.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SaavnApiService:
    BASE_URL = "https://www.jiosaavn.com/api.php"
    API_PARAMS = "&_format=json&_marker=0&api_version=4&ctx=web6dot0"

    @staticmethod
    def search_songs(query):
        """Search for songs on JioSaavn."""
        encoded_query = urllib.parse.quote(query)
        url = f"{SaavnApiService.BASE_URL}?__call=search.getResults&q={encoded_query}{SaavnApiService.API_PARAMS}"
        
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                clean_json = response.text[response.text.find('{'):]
                data = json.loads(clean_json)
                return data.get('results', [])
            else:
                raise Exception('Failed to search songs')
        except Exception as e:
            print(f'Search Error: {e}')
            return [] 

    @staticmethod
    def get_streaming_url(song_id):
        """Get streaming URL for a song."""
        details_url = f"{SaavnApiService.BASE_URL}?__call=song.getDetails&pids={song_id}{SaavnApiService.API_PARAMS}"
        
        try:
            details_response = requests.get(details_url, verify=False)
            details_data = json.loads(details_response.text)
            
            if 'songs' in details_data and len(details_data['songs']) > 0:
                song_data = details_data['songs'][0]
                more_info = song_data.get('more_info', {})
                if 'encrypted_media_url' in more_info:
                    encrypted_url = more_info['encrypted_media_url']
                else:
                    raise Exception('Encrypted media URL not found')
            else:
                raise Exception('Song data not found')
                
        except Exception as e:
            print(f'Get Details Error: {e}')
            raise Exception('Could not get song details')
        
        encoded_encrypted_url = urllib.parse.quote(encrypted_url)
        token_url = f"{SaavnApiService.BASE_URL}?__call=song.generateAuthToken&url={encoded_encrypted_url}&bitrate=320{SaavnApiService.API_PARAMS}"
        
        try:
            token_response = requests.get(token_url, verify=False)
            token_data = json.loads(token_response.text)
            
            if isinstance(token_data.get('auth_url'), str):
                stream_url = token_data['auth_url']
                return stream_url.replace('web.saavncdn.com', 'aac.saavncdn.com').replace('_96.mp4', '_320.mp4')
            else:
                raise Exception('Failed to get auth_url, token may have expired')
                
        except Exception as e:
            print(f'Generate Token Error: {e}')
            raise Exception('Could not generate streaming URL')

# --- Flask App Setup and Routes ---
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/api/search")
def api_search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    try:
        results = SaavnApiService.search_songs(query)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/stream/<song_id>")
def api_stream(song_id):
    try:
        stream_url = SaavnApiService.get_streaming_url(song_id)
        return jsonify({'stream_url': stream_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)