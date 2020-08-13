import requests
import validators
from io import BytesIO
from PIL import Image, UnidentifiedImageError


def parse_request(request):
    """ Parse and validate Vectorizer Request
    Arguments:
       [flask.request] -- [flask request for vectorisation]
    Returns:
        [None/dict,flask.request] -- [(errors if any),flask request]
    """

    error = None

    # validating the request json to be a list and to have both the required keys for vectorisation
    if isinstance(request.json, list) and \
            all([list(element.keys()) == ['text', 'image'] for element in request.json]):
        for entity in request.json:

            # validating url and text
            if all([isinstance(element, str) for element in entity.values()]) and \
                    (validators.url(entity['image']) or entity['image'] == ""):

                # validating image url
                if entity['image']:
                    try:
                        response = requests.get(entity['image'])
                        Image.open(BytesIO(response.content))
                    except UnidentifiedImageError as e:
                        error = {'error': 'Invalid Request'}
            else:
                error = {'error': 'Invalid Request'}
    else:
        error = {'error': 'Invalid Request'}
    return error, request
