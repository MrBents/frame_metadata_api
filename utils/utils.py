BASE_PATH_IMAGES_DROPBOX = '/test_dropbox/images/'
BASE_PATH_METADATA_DROPBOX = '/test_dropbox/metadata/'


def tokenIdToImagePath(token_id):
    return BASE_PATH_IMAGES_DROPBOX + 'img_' + str(token_id) + '.jpg'


def tokenIdToMetadataPath(token_id):
    return BASE_PATH_METADATA_DROPBOX + 'metadata_' + str(token_id) + '.json'


def synthetizeMetadata(img_url, x, y):
    return {
        "description": "A maleable space to display your art.",
        "image": img_url,
        "name": "Canvas Frame",
        "row": str(x),
        "column": str(y)
    }
