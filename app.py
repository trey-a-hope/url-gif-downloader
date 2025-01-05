from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import requests
import io
import validators

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/download-gif", methods=["GET"])
def download_gif():
    gif_url = request.args.get("url")

    if not gif_url or not validators.url(gif_url):
        return jsonify({"error": "Invalid URL provided"}), 400

    try:
        # Add headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "image/gif,image/jpeg,image/png,*/*",
            "Referer": gif_url,
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(gif_url, headers=headers, allow_redirects=True)
        response.raise_for_status()

        # Verify content type
        content_type = response.headers.get("content-type", "")
        if "image" not in content_type.lower():
            return jsonify({"error": "URL does not point to an image"}), 400

        gif_data = io.BytesIO(response.content)
        gif_data.seek(0)

        filename = gif_url.split("/")[-1]
        if not filename.endswith((".gif", ".jpg", ".jpeg", ".png")):
            filename = "downloaded.gif"

        return send_file(
            gif_data, mimetype=content_type, as_attachment=True, download_name=filename
        )

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to download image: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
