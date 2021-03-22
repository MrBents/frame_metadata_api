from flask import Flask
# from handlers.payload_builder import VroomPayloadBuilder
# import requests
from utils.dropbox_manager import DropboxManager
from utils.utils import tokenIdToImagePath, tokenIdToMetadataPath, synthetizeMetadata
import json
import tempfile

import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

api_key = os.environ["DROPBOX_KEY"]

dropbox_manager = DropboxManager(api_key)


@app.route('/frame')
def baseUri():
    return {
        "description": "Friendly frames.",
        "external_link": "https://github.com/mrbents/",
        "image": "https://example.com/image.png",
        "name": "Canvas Frames",
        "column": "column",
        "row": "row"
    }


@app.route('/frame/<token_id>')
def tokenUri(token_id):
    # recalculate dropbox path.
    metadata_path = tokenIdToMetadataPath(token_id)
    return dropbox_manager.preview_metadata(metadata_path)


@app.route('/frame/initialize/<token_id>/<x>/<y>')
def intializeMetadata(token_id, x, y):
    # (1) Define image and metadata paths.
    dropbox_img_path = tokenIdToImagePath(token_id)
    dropbox_metadata_path = tokenIdToMetadataPath(token_id)
    # (2) Upload image.
    external_img_url = dropbox_manager.upload_file(
        './white_square.jpg', dropbox_img_path)
    # (3) Create json metadata.
    metadata_dict = synthetizeMetadata(external_img_url, x, y)
    # (4) save to temp file and upload.
    temp = tempfile.TemporaryFile()
    temp.write(json.dumps(metadata_dict).encode('utf-8'))
    dropbox_manager.upload_file(temp, dropbox_metadata_path)
    temp.close()

    return "ok\n"


@app.route('/frame/update/<token_id>')
def updateImage(token_id):
    return "ok\n"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
