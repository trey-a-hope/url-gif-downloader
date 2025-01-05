# Server (app.py)
from flask import Flask, send_file, request, jsonify
import requests
import io
import validators

app = Flask(__name__)

@app.route('/download-gif', methods=['GET'])
def download_gif():
    # Get the GIF URL from query parameters
    gif_url = request.args.get('url')
    
    # Validate URL
    if not gif_url or not validators.url(gif_url):
        return jsonify({'error': 'Invalid URL provided'}), 400
    
    try:
        # Download the GIF
        response = requests.get(gif_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Verify content type is actually a GIF
        content_type = response.headers.get('content-type', '')
        if 'gif' not in content_type.lower():
            return jsonify({'error': 'URL does not point to a GIF image'}), 400
        
        # Create in-memory file
        gif_data = io.BytesIO(response.content)
        gif_data.seek(0)
        
        # Generate filename from URL
        filename = gif_url.split('/')[-1]
        if not filename.endswith('.gif'):
            filename = 'downloaded.gif'
        
        # Send file to user's browser which will trigger their download dialog
        return send_file(
            gif_data,
            mimetype='image/gif',
            as_attachment=True,
            download_name=filename
        )
    
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to download GIF: {str(e)}'}), 500

# Simple HTML interface
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>GIF Downloader</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .container {
                text-align: center;
            }
            input[type="text"] {
                width: 80%;
                padding: 10px;
                margin: 10px 0;
            }
            button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            #status {
                margin-top: 20px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>GIF Downloader</h1>
            <input type="text" id="gifUrl" placeholder="Enter GIF URL">
            <button onclick="downloadGif()">Download GIF</button>
            <div id="status"></div>
        </div>
        
        <script>
            function downloadGif() {
                const url = document.getElementById('gifUrl').value;
                if (!url) {
                    document.getElementById('status').textContent = 'Please enter a URL';
                    return;
                }
                
                document.getElementById('status').textContent = 'Downloading...';
                window.location.href = `/download-gif?url=${encodeURIComponent(url)}`;
                setTimeout(() => {
                    document.getElementById('status').textContent = 'Download started!';
                }, 1000);
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
