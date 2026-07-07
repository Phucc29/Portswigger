from flask import Flask, request, abort, send_file
import os
import urllib.parse

app = Flask(__name__)

IMAGE_DIR = 'images'

@app.route("/")

def home():
    return """
    <h2>Product Images</h2>
    <img src="/image?filename=image.png" width=300>
    """

@app.route("/image")
def image():
    filename = request.args.get("filename","")
    filename = urllib.parse.unquote(filename)

    if not filename.endswith(".png"):
        return "Only png allowed",403

    if "\x00" in filename:
        filename = filename.split("\x00")[0]

    #Lỗi path traversal ở đây
    path = os.path.join(IMAGE_DIR, filename)

    try:
        return send_file(path)
    except Exception as e:
        return str(e), 404

if __name__ == "__main__":
    app.run(debug=True)