from flask import Flask
# from handlers.payload_builder import VroomPayloadBuilder
# import requests
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

BASE_PATH_FS_DROPBOX = '/test_dropbox'

api_key = os.environ["DROPBOX_KEY"]


@app.route('/frame')
def baseUri():
    # TODO: return json contract
    return {
        "description": "Friendly frames.",
        "external_link": "https://github.com/mrbents/",
        "image": "https://example.com/image.png",
        "name": "Canvas Frames"
    }


@app.route('/frame/<token_id>')
def tokenUri():
    # TODO: return token metadata
    pass


@app.route('/frame/initialize/<token_id>')
def intializeMetadata():
    # TODO: (1) save blanc image, (2) save token metadata
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
